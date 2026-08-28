<script lang="ts">
	import { getContext } from 'svelte';
	import Modal from '$lib/components/common/Modal.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';

	const i18n = getContext('i18n');

	export let show = false;
</script>

<Modal bind:show size="lg">
	<div class="p-5">
		<div class="flex justify-between items-center mb-4">
			<div class="text-lg font-medium">{$i18n.t('Usage Guide')}</div>
			<button on:click={() => (show = false)}>
				<XMark className="size-5" />
			</button>
		</div>

		<div class="max-h-[70vh] overflow-y-auto scrollbar-hidden text-sm space-y-4 pr-1">
			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('What is LATXA?')}</h3>
				<p>
					{$i18n.t(
						'LATXA is a chat assistant based on a Basque language model. You can ask questions, generate or summarize text, translate, and much more — all in Basque.'
					)}
				</p>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('Starting a new chat')}</h3>
				<p>
					{$i18n.t(
						'Click "New Chat" in the left-hand menu, and type your question or request in the text box at the bottom. Press send or hit Enter to send the message.'
					)}
				</p>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('Switching models')}</h3>
				<p>
					{$i18n.t(
						"Using the model selector at the top, you can switch the model you're using at any point in the conversation without losing the previous history."
					)}
				</p>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('Files and knowledge bases')}</h3>
				<p>
					{$i18n.t(
						'Using the "+" button next to the message box, you can attach files, a note, or a knowledge base so the model takes them into account when answering.'
					)}
				</p>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('Translating documents')}</h3>
				<p>
					{$i18n.t(
						'Attach a Word, PowerPoint, or Excel document, turn on the "Translate Document" option in the attachments menu, and tell LATXA which language to translate it into (for example, into Basque, or from Basque into Spanish or English). You will get back a new file in the same format, with the translation applied and the original layout preserved as closely as possible.'
					)}
				</p>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('Downloading responses')}</h3>
				<p>
					{$i18n.t(
						"Every response from LATXA can be downloaded using the download icon below it, in several formats: Markdown, HTML, PDF, Word, Excel, or as source code when the response contains code."
					)}
				</p>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('Voice conversation')}</h3>
				<p>
					{$i18n.t(
						'By clicking the call icon, you can talk to the model by voice: your speech will be transcribed and the answer will be read aloud to you.'
					)}
				</p>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('Dark mode')}</h3>
				<p>
					{$i18n.t('Use the sun/moon icon in the top bar to switch between light and dark mode at any time.')}
				</p>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('Need help?')}</h3>
				<p>
					{$i18n.t('If you run into any issues or have suggestions, please contact us:')}
					<a href="mailto:latxa.hitz@ehu.eus" class="underline">latxa.hitz@ehu.eus</a>
				</p>
			</section>
		</div>
	</div>
</Modal>
