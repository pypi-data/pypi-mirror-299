<script lang="ts">
	import { type FileData } from "@gradio/client";

	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let variant: "primary" | "secondary" | "stop" = "secondary";
	export let size: "sm" | "lg" = "lg";
	export let value: string | null = null;
	export let link: string | null = null;
	export let icon: FileData | null = null;
	export let disabled = false;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let tooltip: string = ""; // New prop for tooltip text
</script>

{#if link && link.length > 0}
	<a
		href={link}
		rel="noopener noreferrer"
		class:hidden={!visible}
		class:disabled
		aria-disabled={disabled}
		class="button-wrapper {size} {variant} {elem_classes.join(' ')}"
		style:flex-grow={scale}
		style:pointer-events={disabled ? "none" : null}
		style:width={scale === 0 ? "fit-content" : null}
		style:min-width={typeof min_width === "number"
			? `calc(min(${min_width}px, 100%))`
			: null}
		id={elem_id}
	>
		{#if icon}
			<img class="button-icon" src={icon.url} alt={`${value} icon`} />
		{/if}
		<slot />
		{#if tooltip}
			<div class="tooltip-wrapper">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="15"
					height="15"
					viewBox="0 0 15 15"
					fill="none"
					class="question-mark"
				>
					<circle
						cx="7.5"
						cy="7.5"
						r="7"
						fill="white"
						stroke="#CCCCCC"
					/>
					<path
						d="M7.88597 8.71201H6.71997V8.39301C6.71997 8.11434 6.76397 7.87601 6.85197 7.67801C6.94731 7.47267 7.06464 7.29667 7.20397 7.15001C7.35064 7.00334 7.50464 6.86767 7.66597 6.74301C7.82731 6.61834 7.97764 6.49734 8.11697 6.38001C8.26364 6.26267 8.38097 6.13434 8.46897 5.99501C8.56431 5.85567 8.61197 5.69067 8.61197 5.50001C8.61197 5.26534 8.52764 5.07467 8.35897 4.92801C8.19764 4.77401 7.93364 4.69701 7.56697 4.69701C7.24431 4.69701 6.95831 4.77034 6.70897 4.91701C6.45964 5.05634 6.27264 5.27267 6.14797 5.56601C6.03064 5.85934 6.00131 6.22967 6.05997 6.67701L5.01497 5.92901C4.96364 5.45967 5.04431 5.04534 5.25697 4.68601C5.47697 4.32667 5.79231 4.04434 6.20297 3.83901C6.62097 3.63367 7.10497 3.53101 7.65497 3.53101C8.35897 3.53101 8.91631 3.68134 9.32697 3.98201C9.74497 4.28267 9.95397 4.74834 9.95397 5.37901C9.95397 5.65767 9.90264 5.89967 9.79997 6.10501C9.70464 6.30301 9.57631 6.47901 9.41497 6.63301C9.26097 6.78701 9.09597 6.93001 8.91997 7.06201C8.74397 7.18667 8.57531 7.31867 8.41397 7.45801C8.25997 7.59001 8.13164 7.74034 8.02897 7.90901C7.93364 8.07034 7.88597 8.26467 7.88597 8.49201V8.71201ZM7.99597 11H6.58797V9.43801H7.99597V11Z"
						fill="#CCCCCC"
					/>
				</svg>
				<span class="tooltip">{tooltip}</span>
			</div>
		{/if}
	</a>
{:else}
	<button
		on:click
		class:hidden={!visible}
		class="button-wrapper {size} {variant} {elem_classes.join(' ')}"
		style:flex-grow={scale}
		style:width={scale === 0 ? "fit-content" : null}
		style:min-width={typeof min_width === "number"
			? `calc(min(${min_width}px, 100%))`
			: null}
		id={elem_id}
		{disabled}
	>
		{#if icon}
			<img class="button-icon" src={icon.url} alt={`${value} icon`} />
		{/if}
		<slot />
		{#if tooltip}
			<div class="tooltip-wrapper">
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="15"
					height="15"
					viewBox="0 0 15 15"
					fill="none"
					class="question-mark"
				>
					<circle
						cx="7.5"
						cy="7.5"
						r="7"
						fill="white"
						stroke="#CCCCCC"
					/>
					<path
						d="M7.88597 8.71201H6.71997V8.39301C6.71997 8.11434 6.76397 7.87601 6.85197 7.67801C6.94731 7.47267 7.06464 7.29667 7.20397 7.15001C7.35064 7.00334 7.50464 6.86767 7.66597 6.74301C7.82731 6.61834 7.97764 6.49734 8.11697 6.38001C8.26364 6.26267 8.38097 6.13434 8.46897 5.99501C8.56431 5.85567 8.61197 5.69067 8.61197 5.50001C8.61197 5.26534 8.52764 5.07467 8.35897 4.92801C8.19764 4.77401 7.93364 4.69701 7.56697 4.69701C7.24431 4.69701 6.95831 4.77034 6.70897 4.91701C6.45964 5.05634 6.27264 5.27267 6.14797 5.56601C6.03064 5.85934 6.00131 6.22967 6.05997 6.67701L5.01497 5.92901C4.96364 5.45967 5.04431 5.04534 5.25697 4.68601C5.47697 4.32667 5.79231 4.04434 6.20297 3.83901C6.62097 3.63367 7.10497 3.53101 7.65497 3.53101C8.35897 3.53101 8.91631 3.68134 9.32697 3.98201C9.74497 4.28267 9.95397 4.74834 9.95397 5.37901C9.95397 5.65767 9.90264 5.89967 9.79997 6.10501C9.70464 6.30301 9.57631 6.47901 9.41497 6.63301C9.26097 6.78701 9.09597 6.93001 8.91997 7.06201C8.74397 7.18667 8.57531 7.31867 8.41397 7.45801C8.25997 7.59001 8.13164 7.74034 8.02897 7.90901C7.93364 8.07034 7.88597 8.26467 7.88597 8.49201V8.71201ZM7.99597 11H6.58797V9.43801H7.99597V11Z"
						fill="#CCCCCC"
					/>
				</svg>
				<span class="tooltip">{tooltip}</span>
			</div>
		{/if}
	</button>
{/if}

<style>
	.button-wrapper {
		position: relative;
		display: inline-flex;
		justify-content: center;
		align-items: center;
	}

	.tooltip-wrapper {
		position: absolute;
		top: -16px;
		right: -16px;
	}

	.question-mark {
		cursor: help;
	}

	.tooltip {
		visibility: hidden;
		position: absolute;
		top: 100%;
		right: 0;
		margin-top: 5px;
		padding: 8px 12px;
		border-radius: 10px;
		border: 1px solid var(--Light-Orange, #ff9a57);
		background: var(--White, #fff);
		color: #333;
		font-size: 12px;
		white-space: nowrap;
		z-index: 1;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.tooltip-wrapper:hover .tooltip {
		visibility: visible;
	}
	button,
	a {
		display: inline-flex;

		justify-content: center;

		align-items: center;

		transition: var(--button-transition);

		box-shadow: var(--button-shadow);

		padding: var(--size-0-5) var(--size-2);

		text-align: center;
	}

	button:hover,
	button[disabled],
	a:hover,
	a.disabled {
		box-shadow: var(--button-shadow-hover);
	}

	button:active,
	a:active {
		box-shadow: var(--button-shadow-active);
	}

	button[disabled],
	a.disabled {
		opacity: 0.5;

		filter: grayscale(30%);

		cursor: not-allowed;
	}

	.hidden {
		display: none;
	}

	.primary {
		border: var(--button-border-width) solid
			var(--button-primary-border-color);

		background: var(--button-primary-background-fill);

		color: var(--button-primary-text-color);
	}

	.primary:hover,
	.primary[disabled] {
		border-color: var(--button-primary-border-color-hover);

		background: var(--button-primary-background-fill-hover);

		color: var(--button-primary-text-color-hover);
	}

	.secondary {
		border: var(--button-border-width) solid
			var(--button-secondary-border-color);

		background: var(--button-secondary-background-fill);

		color: var(--button-secondary-text-color);
	}

	.secondary:hover,
	.secondary[disabled] {
		border-color: var(--button-secondary-border-color-hover);

		background: var(--button-secondary-background-fill-hover);

		color: var(--button-secondary-text-color-hover);
	}

	.stop {
		border: var(--button-border-width) solid
			var(--button-cancel-border-color);

		background: var(--button-cancel-background-fill);

		color: var(--button-cancel-text-color);
	}

	.stop:hover,
	.stop[disabled] {
		border-color: var(--button-cancel-border-color-hover);

		background: var(--button-cancel-background-fill-hover);

		color: var(--button-cancel-text-color-hover);
	}

	.sm {
		border-radius: var(--button-small-radius);

		padding: var(--button-small-padding);

		font-weight: var(--button-small-text-weight);

		font-size: var(--button-small-text-size);
	}

	.lg {
		border-radius: var(--button-large-radius);

		padding: var(--button-large-padding);

		font-weight: var(--button-large-text-weight);

		font-size: var(--button-large-text-size);
	}

	.button-icon {
		width: var(--text-xl);

		height: var(--text-xl);

		margin-right: var(--spacing-xl);
	}
</style>
