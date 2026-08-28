<script lang="ts">
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import Modal from '$lib/components/common/Modal.svelte';
	import Spinner from '$lib/components/common/Spinner.svelte';
	import XMark from '$lib/components/icons/XMark.svelte';
	import { models } from '$lib/stores';
	import { getPricing, updatePricing } from '$lib/apis/analytics';

	const i18n = getContext('i18n');

	export let show = false;
	export let onSave: () => void = () => {};

	type PriceEntry = { input_price_per_million: number; output_price_per_million: number };

	let pricing: Record<string, PriceEntry> = {};
	let loading = false;
	let saving = false;

	const load = async () => {
		loading = true;
		try {
			const res = await getPricing(localStorage.token);
			const loaded: Record<string, PriceEntry> = {};
			for (const model of $models) {
				loaded[model.id] = {
					input_price_per_million: res?.[model.id]?.input_price_per_million ?? 0,
					output_price_per_million: res?.[model.id]?.output_price_per_million ?? 0
				};
			}
			pricing = loaded;
		} catch (err) {
			console.error('Failed to load pricing:', err);
			toast.error($i18n.t('Failed to load pricing'));
		}
		loading = false;
	};

	$: if (show) {
		load();
	}

	const save = async () => {
		saving = true;
		try {
			// Only persist models with a non-zero price, keeps the config compact.
			const toSave = Object.fromEntries(
				Object.entries(pricing).filter(
					([, p]) => p.input_price_per_million > 0 || p.output_price_per_million > 0
				)
			);
			await updatePricing(localStorage.token, toSave);
			toast.success($i18n.t('Pricing saved'));
			onSave();
			show = false;
		} catch (err) {
			console.error('Failed to save pricing:', err);
			toast.error($i18n.t('Failed to save pricing'));
		}
		saving = false;
	};
</script>

<Modal bind:show size="md">
	<div class="p-4">
		<div class="flex justify-between items-center mb-3">
			<div class="text-lg font-medium">{$i18n.t('Token Pricing')}</div>
			<button on:click={() => (show = false)}>
				<XMark className="size-5" />
			</button>
		</div>

		<div class="text-xs text-gray-500 dark:text-gray-400 mb-3">
			{$i18n.t(
				'Set the price per 1 million tokens for each model to estimate cost in the analytics dashboard. Leave at 0 to exclude a model from cost estimates.'
			)}
		</div>

		{#if loading}
			<div class="my-8 flex justify-center">
				<Spinner className="size-5" />
			</div>
		{:else}
			<div class="max-h-96 overflow-y-auto scrollbar-hidden">
				<table class="w-full text-sm text-left">
					<thead class="text-xs text-gray-500 dark:text-gray-400">
						<tr>
							<th class="py-1 pr-2">{$i18n.t('Model')}</th>
							<th class="py-1 px-2 text-right">{$i18n.t('Input $/1M')}</th>
							<th class="py-1 pl-2 text-right">{$i18n.t('Output $/1M')}</th>
						</tr>
					</thead>
					<tbody>
						{#each $models as model (model.id)}
							<tr class="border-t border-gray-100 dark:border-gray-800">
								<td class="py-1.5 pr-2 truncate max-w-[140px]" title={model.id}
									>{model.name || model.id}</td
								>
								<td class="py-1.5 px-2">
									<input
										type="number"
										min="0"
										step="0.01"
										bind:value={pricing[model.id].input_price_per_million}
										class="w-full text-right bg-transparent outline-hidden border border-gray-200 dark:border-gray-700 rounded-lg px-2 py-1"
									/>
								</td>
								<td class="py-1.5 pl-2">
									<input
										type="number"
										min="0"
										step="0.01"
										bind:value={pricing[model.id].output_price_per_million}
										class="w-full text-right bg-transparent outline-hidden border border-gray-200 dark:border-gray-700 rounded-lg px-2 py-1"
									/>
								</td>
							</tr>
						{/each}
						{#if $models.length === 0}
							<tr><td colspan="3" class="py-3 text-center text-gray-400">{$i18n.t('No models')}</td></tr>
						{/if}
					</tbody>
				</table>
			</div>

			<div class="flex justify-end mt-4">
				<button
					class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 rounded-full disabled:opacity-50"
					disabled={saving}
					on:click={save}
				>
					{saving ? $i18n.t('Saving...') : $i18n.t('Save')}
				</button>
			</div>
		{/if}
	</div>
</Modal>
