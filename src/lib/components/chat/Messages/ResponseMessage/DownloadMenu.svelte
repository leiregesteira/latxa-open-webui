<script lang="ts">
	import { getContext } from 'svelte';
	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;
	import { marked } from 'marked';

	import Dropdown from '$lib/components/common/Dropdown.svelte';

	const i18n = getContext('i18n');

	export let content = '';
	export let filename = 'response';
	export let onClose: Function = () => {};

	let show = false;

	const LANGUAGE_EXTENSIONS: Record<string, string> = {
		javascript: 'js',
		js: 'js',
		jsx: 'jsx',
		typescript: 'ts',
		ts: 'ts',
		tsx: 'tsx',
		python: 'py',
		py: 'py',
		java: 'java',
		c: 'c',
		cpp: 'cpp',
		'c++': 'cpp',
		csharp: 'cs',
		cs: 'cs',
		go: 'go',
		golang: 'go',
		ruby: 'rb',
		rb: 'rb',
		php: 'php',
		html: 'html',
		css: 'css',
		scss: 'scss',
		json: 'json',
		bash: 'sh',
		sh: 'sh',
		shell: 'sh',
		zsh: 'sh',
		sql: 'sql',
		yaml: 'yaml',
		yml: 'yaml',
		xml: 'xml',
		rust: 'rs',
		rs: 'rs',
		kotlin: 'kt',
		kt: 'kt',
		swift: 'swift',
		markdown: 'md',
		md: 'md'
	};

	// Ordered by how distinctive the pattern is (unique syntax first) so common keywords
	// like "def " or "end" don't cause cross-language false positives.
	const LANGUAGE_HEURISTICS: { ext: string; patterns: RegExp[] }[] = [
		{ ext: 'php', patterns: [/<\?php/] },
		{ ext: 'py', patterns: [/^\s*def\s+\w+\s*\(.*\)\s*:/m, /^\s*import\s+\w+/m, /^\s*from\s+\w+\s+import\s+/m, /\bprint\(/, /^\s*elif\s+.*:/m, /^\s*self\./m] },
		{ ext: 'go', patterns: [/^\s*package\s+main/m, /^\s*func\s+main\s*\(/m, /\bfmt\.(Println|Printf)\(/] },
		{ ext: 'rs', patterns: [/^\s*fn\s+main\s*\(/m, /\bprintln!\(/, /^\s*let\s+mut\s+/m] },
		{ ext: 'cs', patterns: [/\busing\s+System;/, /\bConsole\.WriteLine\(/, /^\s*namespace\s+\w+/m] },
		{ ext: 'java', patterns: [/\bpublic\s+class\s+\w+/, /\bpublic\s+static\s+void\s+main\s*\(/, /\bSystem\.out\.println\(/] },
		{ ext: 'cpp', patterns: [/#include\s*<\w+>/, /\bstd::/, /\bint\s+main\s*\(/] },
		{ ext: 'sql', patterns: [/^\s*SELECT\s+.+\s+FROM\s+/im, /^\s*INSERT\s+INTO\s+/im, /^\s*CREATE\s+TABLE\s+/im, /^\s*UPDATE\s+.+\s+SET\s+/im] },
		{ ext: 'html', patterns: [/<!DOCTYPE html>/i, /<\/?(html|body|head|div)[\s>]/i] },
		{ ext: 'sh', patterns: [/^#!\/bin\/(ba)?sh/, /^#!\/usr\/bin\/env\s+(ba)?sh/, /^\s*sudo\s+/m] },
		{ ext: 'yaml', patterns: [/^---\s*$/m, /^\s*[\w-]+:\s*$/m] },
		{
			ext: 'js',
			patterns: [
				/\bconsole\.log\(/,
				/^\s*(const|let|var)\s+\w+\s*=/m,
				/=>\s*\{?/,
				/\brequire\(['"]/,
				/^\s*import\s+.+\s+from\s+['"]/m,
				/^\s*export\s+(default\s+)?/m,
				/^\s*function\s+\w+\s*\(/m
			]
		}
	];

	const guessLanguage = (code: string): string | null => {
		let best: { ext: string; score: number } | null = null;
		for (const { ext, patterns } of LANGUAGE_HEURISTICS) {
			const score = patterns.reduce((acc, p) => acc + (p.test(code) ? 1 : 0), 0);
			if (score > 0 && (!best || score > best.score)) {
				best = { ext, score };
			}
		}
		if (best) return best.ext;

		try {
			const trimmed = code.trim();
			if ((trimmed.startsWith('{') || trimmed.startsWith('[')) && JSON.parse(trimmed)) return 'json';
		} catch (e) {
			// not valid JSON, fall through
		}

		return null;
	};

	const getCodeExtension = (lang: string | undefined, code: string) => {
		if (lang) {
			const key = lang.trim().toLowerCase().split(' ')[0];
			if (key) return LANGUAGE_EXTENSIONS[key] ?? key;
		}
		return guessLanguage(code) ?? 'txt';
	};

	const getTokens = () => {
		try {
			return marked.lexer(content) as any[];
		} catch (e) {
			return [];
		}
	};

	$: codeBlocks = getTokens().filter((t) => t.type === 'code' && (t.text ?? '').trim() !== '');
	$: tables = getTokens().filter((t) => t.type === 'table');

	const downloadMarkdown = () => {
		const blob = new Blob([content], { type: 'text/markdown' });
		saveAs(blob, `${filename}.md`);
		show = false;
	};

	const downloadHtml = () => {
		const htmlContent = marked.parse(content);

		const fullHtml = `<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>${filename}</title>
<style>
	body { font-family: -apple-system, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 16px; }
	pre { background-color: #f6f8fa; border-radius: 6px; padding: 16px; overflow: auto; }
	code { font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace; font-size: 14px; }
	table { border-collapse: collapse; width: 100%; margin-bottom: 16px; }
	table, th, td { border: 1px solid #dfe2e5; }
	th, td { padding: 8px 12px; }
	th { background-color: #f6f8fa; }
	blockquote { border-left: 4px solid #dfe2e5; padding-left: 16px; color: #6a737d; margin-left: 0; }
</style>
</head>
<body>
${htmlContent}
</body>
</html>`;

		const blob = new Blob([fullHtml], { type: 'text/html' });
		saveAs(blob, `${filename}.html`);
		show = false;
	};

	// Table cell text (unlike paragraphs/lists) is used raw rather than walked through
	// inlineToSegments/inlineToRuns, so leftover **bold**/`code` markers must be stripped
	// manually for the PDF and XLSX exporters. A cell fully wrapped in ** (the common
	// "bold label" case) is rendered bold; partial inline bold within a cell is unwrapped.
	const stripInlineMarkdown = (text: string) =>
		text.replace(/\*\*(.+?)\*\*/g, '$1').replace(/__(.+?)__/g, '$1').replace(/`(.+?)`/g, '$1');
	const isFullyBoldCell = (text: string) => /^\*\*[\s\S]+\*\*$/.test(text.trim());

	// marked HTML-escapes leaf inline tokens (" -> &quot;, ' -> &#39;, etc.) since its normal
	// output target is HTML. Decode those entities back to literal characters.
	const decodeEntities = (str: string): string => {
		if (typeof document === 'undefined') return str;
		const el = document.createElement('textarea');
		el.innerHTML = str;
		return el.value;
	};

	// Flattens marked's inline token tree into plain {text, bold, italics, code, ...} segments,
	// shared by both the PDF (canvas-drawn) and future renderers that need styled runs.
	const inlineToSegments = (
		inlineTokens: any[] = [],
		style: Record<string, boolean> = {}
	): { text: string; bold?: boolean; italics?: boolean; code?: boolean; strike?: boolean }[] => {
		const segments: any[] = [];
		for (const t of inlineTokens) {
			const nested = t.tokens ?? [{ type: 'text', text: t.text ?? '' }];
			switch (t.type) {
				case 'strong':
					segments.push(...inlineToSegments(nested, { ...style, bold: true }));
					break;
				case 'em':
					segments.push(...inlineToSegments(nested, { ...style, italics: true }));
					break;
				case 'del':
					segments.push(...inlineToSegments(nested, { ...style, strike: true }));
					break;
				case 'codespan':
					segments.push({ text: decodeEntities(t.text ?? ''), ...style, code: true });
					break;
				case 'link':
					segments.push(...inlineToSegments(nested, style));
					break;
				case 'br':
					segments.push({ text: '\n', ...style });
					break;
				case 'text':
				case 'escape':
				case 'html':
					segments.push({ text: decodeEntities(t.text ?? ''), ...style });
					break;
				default:
					if (t.text) segments.push({ text: decodeEntities(t.text), ...style });
			}
		}
		return segments;
	};

	const downloadPdf = async () => {
		const { default: jsPDF } = await import('jspdf');

		const doc = new jsPDF();

		const left = 15;
		const top = 20;
		const bottom = 20;
		const baseFontSize = 10;

		const pageWidth = doc.internal.pageSize.getWidth();
		const pageHeight = doc.internal.pageSize.getHeight();
		const usableWidth = pageWidth - left - left;

		let y = top;

		const setSegmentFont = (fontSize: number, segment: { bold?: boolean; italics?: boolean; code?: boolean }) => {
			doc.setFontSize(fontSize);
			if (segment.code) {
				doc.setFont('courier', segment.bold ? 'bold' : 'normal');
				return;
			}
			let style = 'normal';
			if (segment.bold && segment.italics) style = 'bolditalic';
			else if (segment.bold) style = 'bold';
			else if (segment.italics) style = 'italic';
			doc.setFont('helvetica', style);
		};

		// Word-wraps a run of styled segments (mixed bold/italic/code within one paragraph)
		// starting at (x, y), returning the y position after the last line drawn.
		const renderSegments = (
			segments: { text: string; bold?: boolean; italics?: boolean; code?: boolean }[],
			startX: number,
			startY: number,
			maxWidth: number,
			fontSize: number
		) => {
			const lineHeight = fontSize * 0.5;
			let cursorX = startX;
			let cursorY = startY;

			const newLine = () => {
				cursorX = startX;
				cursorY += lineHeight;
				if (cursorY + lineHeight > pageHeight - bottom) {
					doc.addPage();
					cursorY = top;
				}
			};

			for (const segment of segments) {
				if (segment.text === '\n') {
					newLine();
					continue;
				}
				setSegmentFont(fontSize, segment);
				const words = segment.text.split(/(\s+)/).filter((w) => w !== '');
				for (const word of words) {
					const isSpace = /^\s+$/.test(word);
					const wordWidth = doc.getTextWidth(word);
					if (!isSpace && cursorX + wordWidth > startX + maxWidth) {
						newLine();
					}
					if (isSpace && cursorX === startX) continue; // drop leading space after a wrap
					doc.text(word, cursorX, cursorY);
					cursorX += wordWidth;
				}
			}

			return cursorY;
		};

		const ensureSpace = (needed: number) => {
			if (y + needed > pageHeight - bottom) {
				doc.addPage();
				y = top;
			}
		};

		const HEADING_SIZES = [18, 16, 14, 12, 11, 10];

		const renderTokens = (tokens: any[], indent = 0) => {
			for (const token of tokens) {
				if (token.type === 'heading') {
					const fontSize = HEADING_SIZES[Math.min((token.depth ?? 1) - 1, 5)];
					ensureSpace(fontSize * 0.6);
					y = renderSegments(
						inlineToSegments(token.tokens, { bold: true }),
						left + indent,
						y,
						usableWidth - indent,
						fontSize
					);
					y += fontSize * 0.5;
				} else if (token.type === 'paragraph') {
					y = renderSegments(inlineToSegments(token.tokens), left + indent, y, usableWidth - indent, baseFontSize);
					y += baseFontSize * 0.5;
				} else if (token.type === 'code') {
					const lines = (token.text ?? '').split('\n');
					doc.setFont('courier', 'normal');
					doc.setFontSize(baseFontSize - 1);
					for (const line of lines) {
						const wrapped = doc.splitTextToSize(line, usableWidth - indent);
						for (const wLine of wrapped) {
							ensureSpace(baseFontSize * 0.5);
							doc.text(wLine, left + indent, y);
							y += baseFontSize * 0.5;
						}
					}
					y += baseFontSize * 0.5;
				} else if (token.type === 'list') {
					(token.items ?? []).forEach((item: any, idx: number) => {
						const bullet = token.ordered ? `${(token.start || 1) + idx}. ` : '• ';
						ensureSpace(baseFontSize * 0.5);
						doc.setFont('helvetica', 'normal');
						doc.setFontSize(baseFontSize);
						doc.text(bullet, left + indent, y);
						const bulletWidth = doc.getTextWidth(bullet);

						let itemTokens: any[] = [];
						for (const sub of item.tokens ?? []) {
							if (sub.tokens) itemTokens = sub.tokens;
						}
						y = renderSegments(
							inlineToSegments(itemTokens.length ? itemTokens : [{ type: 'text', text: item.text ?? '' }]),
							left + indent + bulletWidth,
							y,
							usableWidth - indent - bulletWidth,
							baseFontSize
						);
						y += baseFontSize * 0.5;
					});
				} else if (token.type === 'blockquote') {
					renderTokens(token.tokens ?? [], indent + 6);
				} else if (token.type === 'table') {
					const header = (token.header ?? []).map((cell: any) => decodeEntities(cell.text ?? ''));
					const rows = (token.rows ?? []).map((row: any[]) =>
						row.map((cell: any) => decodeEntities(cell.text ?? ''))
					);
					const colCount = Math.max(header.length, 1);
					const colWidth = (usableWidth - indent) / colCount;

					const rowLineHeight = baseFontSize * 0.5;

					const renderRow = (cells: string[], headerBold: boolean) => {
						doc.setFontSize(baseFontSize);
						const prepared = cells.map((raw) => {
							const trimmed = raw.trim();
							const isBold = headerBold || isFullyBoldCell(trimmed);
							return { text: stripInlineMarkdown(trimmed), isBold };
						});
						const wrappedCells = prepared.map(({ text, isBold }) => {
							doc.setFont('helvetica', isBold ? 'bold' : 'normal');
							return { lines: doc.splitTextToSize(text, colWidth - 4), isBold };
						});
						const lineCount = Math.max(1, ...wrappedCells.map(({ lines }) => lines.length));
						ensureSpace(lineCount * rowLineHeight);
						for (let lineIdx = 0; lineIdx < lineCount; lineIdx++) {
							wrappedCells.forEach(({ lines, isBold }, colIdx) => {
								if (lines[lineIdx]) {
									doc.setFont('helvetica', isBold ? 'bold' : 'normal');
									doc.text(lines[lineIdx], left + indent + colIdx * colWidth, y + lineIdx * rowLineHeight);
								}
							});
						}
						y += lineCount * rowLineHeight;
					};

					renderRow(header, true);
					for (const row of rows) renderRow(row, false);
					y += baseFontSize * 0.5;
				} else if (token.type === 'space') {
					continue;
				} else if (token.text) {
					y = renderSegments([{ text: token.text }], left + indent, y, usableWidth - indent, baseFontSize);
					y += baseFontSize * 0.5;
				}
			}
		};

		let tokens: any[] = [];
		try {
			tokens = marked.lexer(content) as any[];
		} catch (e) {
			tokens = [];
		}

		if (tokens.length > 0) {
			renderTokens(tokens);
		} else {
			doc.setFont('helvetica', 'normal');
			doc.setFontSize(baseFontSize);
			renderSegments([{ text: content }], left, y, usableWidth, baseFontSize);
		}

		doc.save(`${filename}.pdf`);
		show = false;
	};

	const downloadCode = () => {
		if (codeBlocks.length === 0) return;

		codeBlocks.forEach((block, idx) => {
			const ext = getCodeExtension(block.lang, block.text ?? '');
			const name = codeBlocks.length > 1 ? `${filename}-${idx + 1}.${ext}` : `${filename}.${ext}`;
			const blob = new Blob([block.text], { type: 'text/plain' });
			saveAs(blob, name);
		});

		show = false;
	};

	const downloadDocx = async () => {
		const { Document, Packer, Paragraph, HeadingLevel, TextRun, Table, TableRow, TableCell, WidthType } =
			await import('docx');

		const HEADING_LEVELS = [
			HeadingLevel.HEADING_1,
			HeadingLevel.HEADING_2,
			HeadingLevel.HEADING_3,
			HeadingLevel.HEADING_4,
			HeadingLevel.HEADING_5,
			HeadingLevel.HEADING_6
		];

		// Walks marked's inline token tree so bold/italic/code/links survive as real Word formatting
		// instead of being flattened to literal markdown syntax (**, `, etc.).
		const inlineToRuns = (inlineTokens: any[] = [], style: Record<string, any> = {}): any[] => {
			const runs: any[] = [];
			for (const t of inlineTokens) {
				const nested = t.tokens ?? [{ type: 'text', text: t.text ?? '' }];
				switch (t.type) {
					case 'strong':
						runs.push(...inlineToRuns(nested, { ...style, bold: true }));
						break;
					case 'em':
						runs.push(...inlineToRuns(nested, { ...style, italics: true }));
						break;
					case 'del':
						runs.push(...inlineToRuns(nested, { ...style, strike: true }));
						break;
					case 'codespan':
						runs.push(
							new TextRun({ text: decodeEntities(t.text ?? ''), font: 'Courier New', ...style })
						);
						break;
					case 'link':
						runs.push(...inlineToRuns(nested, { ...style, color: '2563EB', underline: {} }));
						break;
					case 'br':
						runs.push(new TextRun({ text: '', break: 1 }));
						break;
					case 'text':
					case 'escape':
					case 'html':
						runs.push(new TextRun({ text: decodeEntities(t.text ?? ''), ...style }));
						break;
					default:
						if (t.text) runs.push(new TextRun({ text: decodeEntities(t.text), ...style }));
				}
			}
			return runs;
		};

		// List item content comes as nested block tokens; pull the inline tokens out of them.
		const listItemRuns = (item: any): any[] => {
			for (const sub of item.tokens ?? []) {
				if (sub.tokens) return inlineToRuns(sub.tokens);
			}
			return [new TextRun({ text: item.text ?? '' })];
		};

		const tokensToChildren = (tokens: any[]): any[] => {
			const children: any[] = [];

			for (const token of tokens) {
				if (token.type === 'heading') {
					children.push(
						new Paragraph({
							children: inlineToRuns(token.tokens),
							heading: HEADING_LEVELS[Math.min((token.depth ?? 1) - 1, 5)]
						})
					);
				} else if (token.type === 'code') {
					const lines = (token.text ?? '').split('\n');
					for (const line of lines) {
						children.push(
							new Paragraph({
								children: [new TextRun({ text: line, font: 'Courier New' })]
							})
						);
					}
				} else if (token.type === 'list') {
					(token.items ?? []).forEach((item: any, idx: number) => {
						const runs = listItemRuns(item);
						if (token.ordered) {
							children.push(
								new Paragraph({
									children: [
										new TextRun({ text: `${(token.start || 1) + idx}. ` }),
										...runs
									]
								})
							);
						} else {
							children.push(new Paragraph({ children: runs, bullet: { level: 0 } }));
						}
					});
				} else if (token.type === 'blockquote') {
					children.push(...tokensToChildren(token.tokens ?? []));
				} else if (token.type === 'table') {
					const headerRow = new TableRow({
						children: (token.header ?? []).map(
							(cell: any) =>
								new TableCell({
									children: [new Paragraph({ children: inlineToRuns(cell.tokens, { bold: true }) })]
								})
						)
					});
					const bodyRows = (token.rows ?? []).map(
						(row: any[]) =>
							new TableRow({
								children: row.map(
									(cell: any) =>
										new TableCell({
											children: [new Paragraph({ children: inlineToRuns(cell.tokens) })]
										})
								)
							})
					);
					children.push(
						new Table({
							width: { size: 100, type: WidthType.PERCENTAGE },
							rows: [headerRow, ...bodyRows]
						})
					);
				} else if (token.type === 'paragraph') {
					children.push(new Paragraph({ children: inlineToRuns(token.tokens) }));
				} else if (token.type === 'space') {
					continue;
				} else if (token.text) {
					children.push(new Paragraph({ text: token.text }));
				}
			}

			return children;
		};

		const children = tokensToChildren(getTokens());

		const doc = new Document({
			sections: [
				{
					children: children.length > 0 ? children : [new Paragraph({ text: content })]
				}
			]
		});

		const blob = await Packer.toBlob(doc);
		saveAs(blob, `${filename}.docx`);
		show = false;
	};

	const downloadXlsx = async () => {
		if (tables.length === 0) return;

		// xlsx (SheetJS community build) can't write cell styles — only exceljs
		// (also MIT-licensed) supports bold/formatting on write, needed to keep
		// header rows bold like the DOCX export already does.
		const ExcelJS = (await import('exceljs')).default;
		const workbook = new ExcelJS.Workbook();

		tables.forEach((table, idx) => {
			const header = (table.header ?? []).map((cell: any) => stripInlineMarkdown((cell.text ?? '').trim()));
			const rows = (table.rows ?? []).map((row: any[]) =>
				row.map((cell: any) => (cell.text ?? '').trim())
			);
			const worksheet = workbook.addWorksheet(`Tabla ${idx + 1}`);

			if (header.length > 0) {
				const headerRow = worksheet.addRow(header);
				headerRow.eachCell((cell) => {
					cell.font = { bold: true };
				});
			}
			rows.forEach((row) => {
				const dataRow = worksheet.addRow(row.map((cellText) => stripInlineMarkdown(cellText)));
				row.forEach((cellText, colIdx) => {
					if (isFullyBoldCell(cellText)) {
						dataRow.getCell(colIdx + 1).font = { bold: true };
					}
				});
			});

			worksheet.columns.forEach((column) => {
				let maxLength = 10;
				column.eachCell?.({ includeEmpty: true }, (cell) => {
					maxLength = Math.max(maxLength, String(cell.value ?? '').length);
				});
				column.width = Math.min(maxLength + 2, 60);
			});
		});

		const arrayBuffer = await workbook.xlsx.writeBuffer();
		const blob = new Blob([arrayBuffer], {
			type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		});
		saveAs(blob, `${filename}.xlsx`);
		show = false;
	};
</script>

<Dropdown
	bind:show
	onOpenChange={(state) => {
		if (state === false) {
			onClose();
		}
	}}
	align="start"
	sideOffset={-2}
>
	<slot></slot>

	<div slot="content">
		<div
			class="max-w-[200px] rounded-2xl px-1 py-1 border border-gray-100 dark:border-gray-800 z-50 bg-white dark:bg-gray-850 dark:text-white shadow-lg transition"
		>
			<button
				class="select-none flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-xl w-full"
				on:click={downloadMarkdown}
			>
				<div class="flex items-center line-clamp-1">{$i18n.t('Markdown (.md)')}</div>
			</button>

			<button
				class="select-none flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-xl w-full"
				on:click={downloadHtml}
			>
				<div class="flex items-center line-clamp-1">{$i18n.t('HTML (.html)')}</div>
			</button>

			<button
				class="select-none flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-xl w-full"
				on:click={downloadPdf}
			>
				<div class="flex items-center line-clamp-1">{$i18n.t('PDF (.pdf)')}</div>
			</button>

			<button
				class="select-none flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-xl w-full"
				on:click={downloadDocx}
			>
				<div class="flex items-center line-clamp-1">{$i18n.t('Word (.docx)')}</div>
			</button>

			{#if tables.length > 0}
				<button
					class="select-none flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-xl w-full"
					on:click={downloadXlsx}
				>
					<div class="flex items-center line-clamp-1">{$i18n.t('Excel (.xlsx)')}</div>
				</button>
			{/if}

			{#if codeBlocks.length > 0}
				<button
					class="select-none flex gap-2 items-center px-3 py-1.5 text-sm cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-800 rounded-xl w-full"
					on:click={downloadCode}
				>
					<div class="flex items-center line-clamp-1">{$i18n.t('Source Code')}</div>
				</button>
			{/if}
		</div>
	</div>
</Dropdown>
