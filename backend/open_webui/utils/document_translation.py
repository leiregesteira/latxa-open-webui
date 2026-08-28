"""
Document translation helpers: extract translatable text fragments from a
DOCX/PPTX/XLSX file, translate them in batches via the configured chat
model, and write the translation back into a new file of the same format.
"""

import asyncio
import io
import logging

from open_webui.utils.chat import generate_chat_completion

log = logging.getLogger(__name__)

SEGMENT_SEPARATOR = '\n<<<SEG>>>\n'
MAX_FRAGMENTS_PER_BATCH = 20
MAX_CHARS_PER_BATCH = 4000

DOCUMENT_TRANSLATION_CONTENT_TYPES = {
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
}


def _chunk_fragments(fragments: list[str]) -> list[list[str]]:
    batches = []
    current: list[str] = []
    current_len = 0
    for frag in fragments:
        if current and (len(current) >= MAX_FRAGMENTS_PER_BATCH or current_len + len(frag) > MAX_CHARS_PER_BATCH):
            batches.append(current)
            current, current_len = [], 0
        current.append(frag)
        current_len += len(frag)
    if current:
        batches.append(current)
    return batches


MAX_ATTEMPTS_PER_BATCH = 3
RETRY_BACKOFF_SECONDS = 2.0


async def _call_model_once(fragments: list[str], target_language: str, request, model_id: str, user) -> str:
    prompt = SEGMENT_SEPARATOR.join(fragments)
    system_prompt = (
        f'You are a professional document translator. Translate the following text segments into {target_language}. '
        f"Segments are separated by the exact marker '{SEGMENT_SEPARATOR.strip()}'. "
        'Return exactly the same number of segments, in the same order, separated by the same marker. '
        'Do not add numbering, explanations, or extra commentary — only the translated segments.'
    )

    response = await generate_chat_completion(
        request,
        {
            'model': model_id,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt},
            ],
            'stream': False,
        },
        user,
    )

    if isinstance(response, dict):
        return response.get('choices', [{}])[0].get('message', {}).get('content') or ''
    return ''


async def _translate_batch(fragments: list[str], target_language: str, request, model_id: str, user) -> list[str] | None:
    """Try translating a batch as one LLM call, retrying with backoff on
    failure/rate-limiting. Returns None (never blank/garbled text) if every
    attempt fails or the model doesn't return the expected segment count."""
    if not fragments:
        return []

    for attempt in range(MAX_ATTEMPTS_PER_BATCH):
        try:
            content = await _call_model_once(fragments, target_language, request, model_id, user)
        except Exception as e:
            log.warning(f'_translate_batch attempt {attempt + 1}/{MAX_ATTEMPTS_PER_BATCH} failed: {e}')
            content = ''

        if content:
            translated = [seg.strip() for seg in content.split(SEGMENT_SEPARATOR.strip())]
            if len(translated) == len(fragments):
                return translated
            log.warning(
                '_translate_batch: segment count mismatch (got %d, expected %d) on attempt %d',
                len(translated),
                len(fragments),
                attempt + 1,
            )

        if attempt < MAX_ATTEMPTS_PER_BATCH - 1:
            await asyncio.sleep(RETRY_BACKOFF_SECONDS * (attempt + 1))

    return None


async def translate_texts(fragments: list[str], target_language: str, request, model_id: str, user) -> tuple[list[str], bool]:
    """
    Translate a list of text fragments via batched LLM calls, preserving
    order. Empty/blank fragments are passed through unchanged. If a batch
    still fails after all retries, it keeps its original text instead of
    being left blank. Returns (translated_fragments, had_failures) so callers
    can warn the user that some content stayed in the original language.
    """
    results: list[str | None] = [None] * len(fragments)
    indices = [i for i, f in enumerate(fragments) if f and f.strip()]
    non_empty = [fragments[i] for i in indices]

    had_failures = False
    cursor = 0
    for batch in _chunk_fragments(non_empty):
        translated = await _translate_batch(batch, target_language, request, model_id, user)
        if translated is None:
            log.warning('translate_texts: giving up on a batch of %d fragment(s), keeping original text', len(batch))
            translated = batch
            had_failures = True

        for offset, value in enumerate(translated):
            results[indices[cursor + offset]] = value
        cursor += len(batch)

    final = [results[i] if results[i] is not None else fragments[i] for i in range(len(fragments))]
    return final, had_failures


def _apply_translated_paragraph(paragraph, new_text: str) -> None:
    """Write translated text into a python-docx/python-pptx paragraph's runs.
    A paragraph is often split into several runs with different formatting
    (e.g. a title run in a large bold font followed by a differently-styled
    continuation) — collapsing everything into one run would drop that
    per-run formatting. Instead, distribute the translated words across the
    existing runs proportionally to each run's original share of the text,
    so each run keeps its own bold/color/size and only its own words change."""
    runs = paragraph.runs
    if not runs or not paragraph.text.strip():
        return

    if len(runs) == 1:
        runs[0].text = new_text
        return

    words = new_text.split(' ')
    total_len = sum(len(r.text) for r in runs) or 1
    remaining_words = len(words)
    word_counts = []
    for i, run in enumerate(runs):
        if i == len(runs) - 1:
            word_counts.append(remaining_words)
        else:
            share = min(round(len(run.text) / total_len * len(words)), remaining_words)
            word_counts.append(share)
            remaining_words -= share

    cursor = 0
    for run, count in zip(runs, word_counts):
        run.text = ' '.join(words[cursor : cursor + count])
        cursor += count


async def translate_docx_bytes(path: str, target_language: str, request, model_id: str, user) -> tuple[bytes, bool]:
    from docx import Document

    doc = Document(path)

    def iter_paragraphs():
        yield from doc.paragraphs
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    yield from cell.paragraphs

    paragraphs = list(iter_paragraphs())
    fragments = [p.text for p in paragraphs]
    translated, had_failures = await translate_texts(fragments, target_language, request, model_id, user)

    for paragraph, new_text in zip(paragraphs, translated):
        _apply_translated_paragraph(paragraph, new_text)

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue(), had_failures


async def translate_pptx_bytes(path: str, target_language: str, request, model_id: str, user) -> tuple[bytes, bool]:
    from pptx import Presentation

    prs = Presentation(path)

    def iter_paragraphs():
        for slide in prs.slides:
            for shape in slide.shapes:
                if shape.has_text_frame:
                    yield from shape.text_frame.paragraphs
                if shape.has_table:
                    for row in shape.table.rows:
                        for cell in row.cells:
                            yield from cell.text_frame.paragraphs

    paragraphs = list(iter_paragraphs())
    fragments = [p.text for p in paragraphs]
    translated, had_failures = await translate_texts(fragments, target_language, request, model_id, user)

    for paragraph, new_text in zip(paragraphs, translated):
        _apply_translated_paragraph(paragraph, new_text)

    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue(), had_failures


async def translate_xlsx_bytes(path: str, target_language: str, request, model_id: str, user) -> tuple[bytes, bool]:
    from openpyxl import load_workbook

    wb = load_workbook(path)

    cells = [
        cell
        for ws in wb.worksheets
        for row in ws.iter_rows()
        for cell in row
        if isinstance(cell.value, str) and cell.value.strip()
    ]
    fragments = [cell.value for cell in cells]
    translated, had_failures = await translate_texts(fragments, target_language, request, model_id, user)

    for cell, new_text in zip(cells, translated):
        cell.value = new_text

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue(), had_failures


TRANSLATORS = {
    'docx': translate_docx_bytes,
    'pptx': translate_pptx_bytes,
    'xlsx': translate_xlsx_bytes,
}


async def persist_translated_file(user, original_filename: str, extension: str, translated_bytes: bytes) -> dict:
    """
    Save translated document bytes as a new file (same storage/DB path uploaded
    files use) and return a chat-message file entry ready for
    `chat:message:files` / `Chats.add_message_files_by_id_and_message_id`.
    """
    import hashlib
    import io as _io
    import os
    import uuid

    from open_webui.models.files import Files, FileForm
    from open_webui.storage.provider import Storage

    new_id = str(uuid.uuid4())
    base_name, _ = os.path.splitext(original_filename)
    new_name = f'{base_name} (translated).{extension}'
    storage_filename = f'{new_id}_{new_name}'
    tags = {
        'OpenWebUI-User-Email': user.email,
        'OpenWebUI-User-Id': user.id,
        'OpenWebUI-User-Name': user.name,
        'OpenWebUI-File-Id': new_id,
    }

    contents, file_path = await asyncio.to_thread(
        Storage.upload_file, _io.BytesIO(translated_bytes), storage_filename, tags
    )
    file_hash = hashlib.sha256(contents).hexdigest()

    new_file = await Files.insert_new_file(
        user.id,
        FileForm(
            id=new_id,
            filename=new_name,
            path=file_path,
            hash=file_hash,
            meta={
                'name': new_name,
                'content_type': DOCUMENT_TRANSLATION_CONTENT_TYPES.get(extension),
                'size': len(contents),
                'file_hash': file_hash,
            },
        ),
    )

    return {
        'type': 'file',
        'id': new_file.id,
        'url': new_file.id,
        'name': new_name,
        'size': len(contents),
        'content_type': DOCUMENT_TRANSLATION_CONTENT_TYPES.get(extension),
    }
