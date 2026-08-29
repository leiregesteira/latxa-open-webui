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

		<div class="max-h-[70vh] overflow-y-auto scrollbar-hidden text-sm space-y-5 pr-1">
			<!-- 1. What you should know before you start -->
			<section>
				<h2 class="text-base font-semibold mb-2">
					{$i18n.t('1. What you should know before you start')}
				</h2>

				<h3 class="font-semibold mb-1">{$i18n.t('1.1 What Latxa can and cannot do')}</h3>
				<p class="mb-2">
					{$i18n.t(
						'Latxa is an artificial intelligence tool designed to understand and answer questions in natural language. It can be very useful for many everyday tasks, but it is important to understand clearly what it can and cannot do.'
					)}
				</p>

				<h4 class="font-medium mb-1">{$i18n.t('What can it help with?')}</h4>
				<ul class="list-disc pl-5 space-y-0.5 mb-2">
					<li>
						<strong>{$i18n.t('Answering questions:')}</strong>
						{$i18n.t('it can provide explanations on many topics, both basic and advanced.')}
					</li>
					<li>
						<strong>{$i18n.t('Writing text:')}</strong>
						{$i18n.t('it helps write emails, reports, stories, or summaries.')}
					</li>
					<li>
						<strong>{$i18n.t('Explaining concepts:')}</strong>
						{$i18n.t('it is useful for understanding complex topics in a simple way.')}
					</li>
					<li>
						<strong>{$i18n.t('Suggesting ideas:')}</strong>
						{$i18n.t('it can help with brainstorming or creative processes.')}
					</li>
					<li>
						<strong>{$i18n.t('Providing technical help:')}</strong>
						{$i18n.t('it gives instructions on programming or digital tools.')}
					</li>
					<li>
						<strong>{$i18n.t('Processing PDFs:')}</strong>
						{$i18n.t(
							'it can automatically extract text from PDF documents and use it to answer questions.'
						)}
					</li>
					<li>
						<strong>{$i18n.t('Searching the web:')}</strong>
						{$i18n.t(
							'when you turn on the web search option in the chat, it can look up current information from the internet in real time.'
						)}
					</li>
				</ul>

				<div
					class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-850/60 px-3 py-2 mb-2"
				>
					💬
					{$i18n.t(
						'You can take advantage of all these capabilities in multiple languages. Although Latxa is optimized for Basque, it also handles other languages well, such as Spanish, English, or French. This makes it easy to translate or work with text in different languages.'
					)}
				</div>

				<h4 class="font-medium mb-1">{$i18n.t('What are its limitations?')}</h4>
				<ul class="list-disc pl-5 space-y-0.5">
					<li>
						<strong>{$i18n.t('It does not always give the correct answer:')}</strong>
						{$i18n.t(
							'it can sometimes provide incorrect, made-up, or incomplete information (known as "hallucinations").'
						)}
					</li>
					<li>
						<strong>{$i18n.t('Its base knowledge has a cutoff date:')}</strong>
						{$i18n.t(
							"without the web search option turned on, Latxa's own training knowledge does not include very recent events. Turn on web search in the chat whenever you need up-to-date information."
						)}
					</li>
					<li>
						<strong>{$i18n.t('It has limitations with Basque dialects:')}</strong>
						{$i18n.t(
							'it is mainly designed for Standard Basque (Euskara Batua). Although it understands dialects fairly well, it can make mistakes when trying to write in them. For more reliable results, we recommend using Standard Basque.'
						)}
					</li>
					<li>
						<strong>{$i18n.t('It does not replace an expert:')}</strong>
						{$i18n.t(
							'for sensitive topics (health, law, finance), it is always better to consult a professional.'
						)}
					</li>
				</ul>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('1.2 What to use Latxa for')}</h3>
				<p class="mb-2">
					{$i18n.t(
						'Latxa is a chatbot with functionality and capabilities similar to other artificial intelligences. As a very versatile tool for helping with everyday tasks, here are some examples of its most practical uses:'
					)}
				</p>

				<h4 class="font-medium mb-1">✍️ {$i18n.t('Writing')}</h4>
				<p class="mb-1">{$i18n.t('Latxa can help you create and improve texts:')}</p>
				<ul class="list-disc pl-5 space-y-0.5 mb-2">
					<li>{$i18n.t('Writing professional emails, letters, or messages.')}</li>
					<li>{$i18n.t('Preparing essays, articles, or reports.')}</li>
					<li>{$i18n.t('Translating, summarizing, or rewriting texts.')}</li>
					<li>{$i18n.t('Adapting the tone (more formal, informal, easier to understand...).')}</li>
				</ul>

				<h4 class="font-medium mb-1">📚 {$i18n.t('Learning')}</h4>
				<p class="mb-1">{$i18n.t('As a study companion:')}</p>
				<ul class="list-disc pl-5 space-y-0.5 mb-2">
					<li>{$i18n.t('Explains complex concepts in an understandable way.')}</li>
					<li>{$i18n.t('Provides examples and additional explanations.')}</li>
					<li>{$i18n.t('Creates questions to prepare for exams or self-assess.')}</li>
					<li>{$i18n.t('Helps understand any topic step by step.')}</li>
				</ul>

				<h4 class="font-medium mb-1">💡 {$i18n.t('Idea generation')}</h4>
				<p class="mb-1">{$i18n.t('It is also useful for boosting creative processes:')}</p>
				<ul class="list-disc pl-5 space-y-0.5 mb-2">
					<li>{$i18n.t('Suggests new ideas.')}</li>
					<li>{$i18n.t('Helps prepare the structure or outline of content.')}</li>
					<li>{$i18n.t('Offers starting points for new projects.')}</li>
				</ul>

				<h4 class="font-medium mb-1">💻 {$i18n.t('Programming and technical help')}</h4>
				<p class="mb-1">{$i18n.t('It also performs well in technical areas:')}</p>
				<ul class="list-disc pl-5 space-y-0.5">
					<li>{$i18n.t('Helps write or understand code.')}</li>
					<li>{$i18n.t('Can help identify and fix bugs.')}</li>
					<li>{$i18n.t('Provides instructions on specific tools or technologies.')}</li>
				</ul>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('1.3 Privacy and responsible use')}</h3>
				<p class="mb-2">
					{$i18n.t(
						'Using Latxa responsibly is essential. Remember that when interacting with chatbots like Latxa, you should carefully handle the information you provide and the responses you receive. Protecting your data should be a priority:'
					)}
				</p>
				<ul class="list-disc pl-5 space-y-0.5 mb-2">
					<li>
						{$i18n.t('Do not share sensitive personal data (ID number, address, phone number, passwords...).')}
					</li>
					<li>{$i18n.t('Be careful with confidential information (for example, work documents).')}</li>
					<li>{$i18n.t('If in doubt, it is better to share less information.')}</li>
				</ul>
				<p class="mb-2">
					{$i18n.t(
						'Additionally, Latxa should not be used for harmful or unethical purposes, and the privacy of others must be respected. For sensitive topics (health, law, or finance), Latxa should only be used as complementary help, never as the sole basis for making decisions.'
					)}
				</p>
				<p>
					{$i18n.t(
						'Finally, although Latxa provides quick and convenient information, it is not always completely reliable. Do not take what it says as absolute truth. It is advisable to verify important information through other sources, especially before making important decisions.'
					)}
				</p>
			</section>

			<!-- 2. Best practices -->
			<section>
				<h2 class="text-base font-semibold mb-2">{$i18n.t('2. Best practices')}</h2>
				<p class="mb-2">
					{$i18n.t(
						"Latxa's responses will depend on your request. The explanations you provide and the precision of your questions directly influence the response you receive. Here are the keys to getting the most out of it:"
					)}
				</p>

				<h3 class="font-semibold mb-1">{$i18n.t('2.1 Writing clear and effective prompts')}</h3>
				<p class="mb-2">
					{$i18n.t(
						'The key to getting the most out of Latxa is writing clear and precise prompts or requests. The better you explain what you want, the more valuable the response you will receive. When making a request, think of it as assigning a task to someone: you need to provide enough information, but in an organized way.'
					)}
				</p>

				<p class="mb-1">
					{$i18n.t(
						'First, it is important to be specific. Generic requests lead to vague answers; specific requests, on the other hand, give useful results:'
					)}
				</p>
				<div class="rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden mb-2 text-xs">
					<div class="flex gap-2 px-3 py-1.5 bg-red-50 dark:bg-red-950/30">
						<span>❌</span><span>{$i18n.t('"Explain the causes of climate change."')}</span>
					</div>
					<div class="flex gap-2 px-3 py-1.5 bg-green-50 dark:bg-green-950/30">
						<span>✅</span>
						<span
							>{$i18n.t(
								'"Explain the main causes of ocean warming and acidification related to human activity."'
							)}</span
						>
					</div>
				</div>

				<p class="mb-1">
					{$i18n.t(
						'Second, it is a good idea to provide context. Latxa does not know why you need the information; you have to explain it. It is often useful to ask Latxa to take on a role (for example, that of an expert):'
					)}
				</p>
				<div class="rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden mb-2 text-xs">
					<div class="flex gap-2 px-3 py-1.5 bg-red-50 dark:bg-red-950/30">
						<span>❌</span><span>{$i18n.t('"Explain the causes of climate change."')}</span>
					</div>
					<div class="flex gap-2 px-3 py-1.5 bg-green-50 dark:bg-green-950/30">
						<span>✅</span>
						<span
							>{$i18n.t(
								'"As if you were an expert in environmental science, explain the main causes of ocean warming and acidification since the 20th century. The explanation is for a first-year Philosophy student."'
							)}</span
						>
					</div>
				</div>

				<p class="mb-1">
					{$i18n.t(
						'Similarly, it is useful to specify constraints or conditions. To better guide the result, tell it how you want the information to be (length, format, language...):'
					)}
				</p>
				<div class="rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden mb-2 text-xs">
					<div class="flex gap-2 px-3 py-1.5 bg-red-50 dark:bg-red-950/30">
						<span>❌</span><span>{$i18n.t('"Explain the causes of climate change."')}</span>
					</div>
					<div class="flex gap-2 px-3 py-1.5 bg-green-50 dark:bg-green-950/30">
						<span>✅</span>
						<span
							>{$i18n.t(
								'"Explain the causes of ocean warming as an environmental expert. Use a list format: for each point, include a short label (2-3 words) and an explanation."'
							)}</span
						>
					</div>
				</div>

				<p class="mb-2">
					{$i18n.t(
						'Finally, try to make individual, well-structured requests. Confusing or overly long requests can lead to incorrect responses.'
					)}
				</p>

				<div
					class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-850/60 px-3 py-2"
				>
					💡
					{$i18n.t(
						'In summary, a good request has three characteristics: it is clear, it is specific, and it provides context. With these foundations, Latxa will help you much better.'
					)}
				</div>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('2.2 Structuring requests for better results')}</h3>
				<p class="mb-2">
					{$i18n.t(
						'In a good request, it is not just what you say that matters, but also how you organize it. If the request is well structured, Latxa will more easily understand its task and provide more accurate results.'
					)}
				</p>

				<h4 class="font-medium mb-1">{$i18n.t('Separate instructions and content')}</h4>
				<p class="mb-1">
					{$i18n.t(
						'In complex requests, it is a good idea to clearly separate the instruction from the input information (text, data...). This is very useful when requesting translations, summaries, or corrections. Use markers (such as dashes or quotation marks) to isolate the text:'
					)}
				</p>
				<div class="rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden mb-2 text-xs">
					<div class="flex gap-2 px-3 py-1.5 bg-red-50 dark:bg-red-950/30">
						<span>❌</span>
						<span
							>{$i18n.t(
								'"Hi Latxa. Tomorrow\'s meeting is cancelled. Sorry! Rewrite this message in a more formal tone."'
							)}</span
						>
					</div>
					<div class="flex gap-2 px-3 py-1.5 bg-green-50 dark:bg-green-950/30 whitespace-pre-line">
						<span>✅</span>
						<span
							>{$i18n.t(
								'"Hi Latxa. Rewrite the following message in a more formal tone.\n\n---\nTomorrow\'s meeting is cancelled. Sorry!\n---"'
							)}</span
						>
					</div>
				</div>

				<h4 class="font-medium mb-1">{$i18n.t('Provide examples')}</h4>
				<p class="mb-1">
					{$i18n.t(
						'Sometimes, explaining what you want to achieve with words alone can be difficult. In these cases, providing one or more examples is the easiest way for Latxa to understand what you want.'
					)}
				</p>
				<ul class="list-disc pl-5 space-y-1 mb-2">
					<li class="whitespace-pre-line">
						{$i18n.t(
							'"Create three new ideas for the project for me, in the following format:\n\n- Idea 1: [Name] + [Short description]\n- Idea 2: [Name] + [Short description]"'
						)}
					</li>
					<li>
						{$i18n.t(
							'"Write a reply to this customer using the following template: \'Hello, we have received your message and are working on...\'."'
						)}
					</li>
				</ul>

				<h4 class="font-medium mb-1">{$i18n.t('Break tasks into steps')}</h4>
				<p class="mb-1">
					{$i18n.t(
						'When the request is complex, it is better to break the task into steps rather than asking for everything at once. This way, Latxa will follow a clearer sequence and the result will be more organized.'
					)}
				</p>
				<div class="rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden text-xs">
					<div class="flex gap-2 px-3 py-1.5 bg-red-50 dark:bg-red-950/30">
						<span>❌</span>
						<span
							>{$i18n.t('"I want your opinion on a text. Explain what it is about and summarize it."')}</span
						>
					</div>
					<div class="flex gap-2 px-3 py-1.5 bg-green-50 dark:bg-green-950/30 whitespace-pre-line">
						<span>✅</span>
						<span
							>{$i18n.t(
								'"Do the following, in order:\n1. Explain the main idea of the text.\n2. Then, summarize it in three points.\n3. Finally, give a brief opinion as a conclusion."'
							)}</span
						>
					</div>
				</div>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('2.3 Refining and improving responses')}</h3>
				<p class="mb-2">
					{$i18n.t(
						'When working with Latxa, you do not have to settle for the first response. In fact, the best results are often achieved through dialogue, gradually adjusting and refining the request.'
					)}
				</p>

				<h4 class="font-medium mb-1">{$i18n.t('Continue the conversation')}</h4>
				<p class="mb-1">
					{$i18n.t(
						'The first response is just a starting point. From there, you can ask new questions or make new requests to get closer to the result you want:'
					)}
				</p>
				<ul class="list-disc pl-5 space-y-0.5 mb-2">
					<li>{$i18n.t('"That is fine, but can you make it shorter?"')}</li>
					<li>{$i18n.t('"Add an example to make it easier to understand."')}</li>
					<li>{$i18n.t('"Go into a bit more depth on this point."')}</li>
				</ul>

				<h4 class="font-medium mb-1">{$i18n.t('Ask for specific changes')}</h4>
				<p class="mb-1">
					{$i18n.t(
						'The more specific your follow-up request is, the easier it will be for Latxa to adapt the response:'
					)}
				</p>
				<div class="rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden mb-2 text-xs">
					<div class="flex gap-2 px-3 py-1.5 bg-red-50 dark:bg-red-950/30">
						<span>❌</span><span>{$i18n.t('"I do not like this."')}</span>
					</div>
					<div class="flex gap-2 px-3 py-1.5 bg-green-50 dark:bg-green-950/30">
						<span>✅</span>
						<span>{$i18n.t('"Make the text more formal and summarize the last paragraph, please."')}</span>
					</div>
				</div>

				<h4 class="font-medium mb-1">{$i18n.t('Try several versions')}</h4>
				<p class="mb-1">
					{$i18n.t(
						'Sometimes it is best to ask for different options and then choose the one you like best or combine versions. For example:'
					)}
				</p>
				<ul class="list-disc pl-5 space-y-0.5 mb-2">
					<li>{$i18n.t('"Give me two versions: one formal and one more informal."')}</li>
					<li>{$i18n.t('"Suggest three different titles for this article."')}</li>
				</ul>

				<h4 class="font-medium mb-1">{$i18n.t('Build step by step')}</h4>
				<p class="mb-1">
					{$i18n.t(
						'Working on long or complex tasks in small chunks is an excellent strategy. This way, you will have better control over the process and the result will be more accurate. For example:'
					)}
				</p>
				<ul class="list-disc pl-5 space-y-0.5">
					<li>{$i18n.t('"Design the structure or outline of the text."')}</li>
					<li>{$i18n.t('"Develop the first section in detail."')}</li>
					<li>{$i18n.t('"Review the whole text and improve the style."')}</li>
				</ul>
			</section>

			<section>
				<h3 class="font-semibold mb-1">{$i18n.t('2.4 Common mistakes and how to avoid them')}</h3>
				<p class="mb-2">
					{$i18n.t(
						'Taking into account what you have learned in this guide, here are the main mistakes people make when using applications like Latxa:'
					)}
				</p>
				<ul class="list-disc pl-5 space-y-0.5">
					<li>
						<strong>{$i18n.t('Being too generic:')}</strong>
						{$i18n.t('remember that specific requests lead to precise responses.')}
					</li>
					<li>
						<strong>{$i18n.t('Not providing context:')}</strong>
						{$i18n.t('Latxa does not know why you need the information; explain it (role, audience, goal...).')}
					</li>
					<li>
						<strong>{$i18n.t('Blindly trusting the results:')}</strong>
						{$i18n.t('do not take responses as absolute truths; verify important data.')}
					</li>
					<li>
						<strong>{$i18n.t('Settling for the first response:')}</strong>
						{$i18n.t('remember that the conversation can continue to refine or improve the result.')}
					</li>
					<li>
						<strong>{$i18n.t('Sharing personal data:')}</strong>
						{$i18n.t('never provide sensitive information (passwords, ID numbers, or confidential data).')}
					</li>
					<li>
						<strong>{$i18n.t('Using a confusing structure:')}</strong>
						{$i18n.t('clearly separating instructions and content prevents many errors.')}
					</li>
				</ul>
			</section>

			<!-- 3. LATXA-specific features (kept from the previous quick guide, now with try-it examples) -->
			<section>
				<h2 class="text-base font-semibold mb-3">{$i18n.t('3. LATXA features')}</h2>

				<div class="grid gap-2.5">
					<div
						class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50/70 dark:bg-gray-850/40 p-3"
					>
						<h3 class="font-semibold mb-1 flex items-center gap-1.5">
							<span>💬</span>{$i18n.t('Starting a new chat')}
						</h3>
						<p class="mb-2">
							{$i18n.t(
								'Click "New Chat" in the left-hand menu, and type your question or request in the text box at the bottom. Press send or hit Enter to send the message.'
							)}
						</p>
						<div
							class="rounded-lg bg-white dark:bg-gray-900/60 border border-gray-200 dark:border-gray-700 px-2.5 py-1.5 text-xs"
						>
							<span class="font-medium">{$i18n.t('Try it:')}</span>
							{$i18n.t('Type "Zer da fotosintesia?" and press Enter to see your first response.')}
						</div>
					</div>

					<div
						class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50/70 dark:bg-gray-850/40 p-3"
					>
						<h3 class="font-semibold mb-1 flex items-center gap-1.5">
							<span>🔀</span>{$i18n.t('Switching models')}
						</h3>
						<p class="mb-2">
							{$i18n.t(
								"Using the model selector at the top, you can switch the model you're using at any point in the conversation without losing the previous history."
							)}
						</p>
						<div
							class="rounded-lg bg-white dark:bg-gray-900/60 border border-gray-200 dark:border-gray-700 px-2.5 py-1.5 text-xs"
						>
							<span class="font-medium">{$i18n.t('Try it:')}</span>
							{$i18n.t(
								'Ask a question in Spanish or English, then switch models mid-conversation without losing your chat history.'
							)}
						</div>
					</div>

					<div
						class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50/70 dark:bg-gray-850/40 p-3"
					>
						<h3 class="font-semibold mb-1 flex items-center gap-1.5">
							<span>📎</span>{$i18n.t('Files and knowledge bases')}
						</h3>
						<p class="mb-2">
							{$i18n.t(
								'Using the "+" button next to the message box, you can attach files, a note, or a knowledge base so the model takes them into account when answering.'
							)}
						</p>
						<div
							class="rounded-lg bg-white dark:bg-gray-900/60 border border-gray-200 dark:border-gray-700 px-2.5 py-1.5 text-xs"
						>
							<span class="font-medium">{$i18n.t('Try it:')}</span>
							{$i18n.t(
								'Attach a PDF and ask "Laburtu dokumentu hau hiru puntutan" (summarize this document in three points).'
							)}
						</div>
					</div>

					<div
						class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50/70 dark:bg-gray-850/40 p-3"
					>
						<h3 class="font-semibold mb-1 flex items-center gap-1.5">
							<span>🌐</span>{$i18n.t('Translating documents')}
						</h3>
						<p class="mb-2">
							{$i18n.t(
								'Attach a Word, PowerPoint, or Excel document, turn on the "Translate Document" option in the attachments menu, and tell LATXA which language to translate it into (for example, into Basque, or from Basque into Spanish or English). You will get back a new file in the same format, with the translation applied and the original layout preserved as closely as possible.'
							)}
						</p>
						<div
							class="rounded-lg bg-white dark:bg-gray-900/60 border border-gray-200 dark:border-gray-700 px-2.5 py-1.5 text-xs"
						>
							<span class="font-medium">{$i18n.t('Try it:')}</span>
							{$i18n.t(
								'Attach a Word document, turn on "Translate Document", and type "Itzuli euskerara" (translate it into Basque).'
							)}
						</div>
					</div>

					<div
						class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50/70 dark:bg-gray-850/40 p-3"
					>
						<h3 class="font-semibold mb-1 flex items-center gap-1.5">
							<span>⬇️</span>{$i18n.t('Downloading responses')}
						</h3>
						<p class="mb-2">
							{$i18n.t(
								'Every response from LATXA can be downloaded using the download icon below it, in several formats: Markdown, HTML, PDF, Word, Excel, or as source code when the response contains code.'
							)}
						</p>
						<div
							class="rounded-lg bg-white dark:bg-gray-900/60 border border-gray-200 dark:border-gray-700 px-2.5 py-1.5 text-xs"
						>
							<span class="font-medium">{$i18n.t('Try it:')}</span>
							{$i18n.t(
								'Ask Latxa to create a table, then download it as an Excel file using the download icon below the response.'
							)}
						</div>
					</div>

					<div
						class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50/70 dark:bg-gray-850/40 p-3"
					>
						<h3 class="font-semibold mb-1 flex items-center gap-1.5">
							<span>🎙️</span>{$i18n.t('Voice conversation')}
						</h3>
						<p class="mb-2">
							{$i18n.t(
								'By clicking the call icon, you can talk to the model by voice: your speech will be transcribed and the answer will be read aloud to you.'
							)}
						</p>
						<div
							class="rounded-lg bg-white dark:bg-gray-900/60 border border-gray-200 dark:border-gray-700 px-2.5 py-1.5 text-xs"
						>
							<span class="font-medium">{$i18n.t('Try it:')}</span>
							{$i18n.t('Click the call icon and say "Kaixo, zer moduz zaude?" out loud.')}
						</div>
					</div>

					<div
						class="rounded-xl border border-gray-200 dark:border-gray-800 bg-gray-50/70 dark:bg-gray-850/40 p-3"
					>
						<h3 class="font-semibold mb-1 flex items-center gap-1.5">
							<span>🌓</span>{$i18n.t('Dark mode')}
						</h3>
						<p class="mb-2">
							{$i18n.t('Use the sun/moon icon in the top bar to switch between light and dark mode at any time.')}
						</p>
						<div
							class="rounded-lg bg-white dark:bg-gray-900/60 border border-gray-200 dark:border-gray-700 px-2.5 py-1.5 text-xs"
						>
							<span class="font-medium">{$i18n.t('Try it:')}</span>
							{$i18n.t('Click the sun/moon icon at any time, even in the middle of a conversation.')}
						</div>
					</div>
				</div>
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
