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
			<div class="text-lg font-medium">{$i18n.t('Terms')}</div>
			<button on:click={() => (show = false)}>
				<XMark className="size-5" />
			</button>
		</div>

		<div class="text-sm text-gray-500 dark:text-gray-400 border border-dashed border-gray-300 dark:border-gray-700 rounded-xl p-4">
			{$i18n.t('TODO: replace this text with the real terms of use.')}
		</div>
	</div>
</Modal>
