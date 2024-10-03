<script lang="ts">
  import { Block } from "@gradio/atoms";
  import Column from "@gradio/column";
  import { Gradio } from "@gradio/utils";
  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = false;
  export let allow_user_close: boolean = false;
  export let close_on_esc: boolean;
  export let close_outer_click: boolean;
  export let close_message: string;
  export let bg_blur: number;
  export let width: number;
  export let height: number;
  export let gradio: Gradio<{
    blur: never;
  }>;

  let element: HTMLElement | null = null;
  let inner_element: HTMLElement | null = null;
  let showConfirmation = false;

  const close = () => {
    if (close_message) {
      showConfirmation = true;
    } else {
      closeModal();
    }
  };

  const closeModal = () => {
    visible = false;
    showConfirmation = false;
    gradio.dispatch("blur");
  };

  const cancelClose = () => {
    showConfirmation = false;
  };

  document.addEventListener("keydown", (evt: KeyboardEvent) => {
    if (close_on_esc && evt.key === "Escape") {
      close();
    }
  });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<!-- svelte-ignore a11y-no-static-element-interactions -->
<div
  class="modal {elem_classes.join(' ')}"
  bind:this={element}
  class:hide={!visible}
  id={elem_id}
  style="backdrop-filter: blur({bg_blur});"
  on:click={(evt) => {
    if (
      close_outer_click &&
      (evt.target === element || evt.target === inner_element)
    ) {
      close();
    }
  }}
>
  <div class="modal-container" bind:this={inner_element}>
    <Block allow_overflow={false} elem_classes={["modal-block"]}>
      {#if allow_user_close}
        <div
          class="close"
          on:click={close}
        >
          <svg
            width="10"
            height="10"
            viewBox="0 0 10 10"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M1 1L9 9"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
            <path
              d="M9 1L1 9"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </div>
      {/if}
      <div class="modal-content" style="width: {width}px; height: {height}px;">
        <Column>
          <slot />
        </Column>
      </div>
    </Block>
  </div>
  {#if showConfirmation}
    <div class="confirmation-modal">
      <div class="confirmation-content">
        <h3>{close_message}</h3>
        <br />
        <div class="confirmation-buttons">
          <button class="yes-button" on:click={closeModal}>Yes</button>
          <button class="no-button" on:click={cancelClose}>No</button>
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  @media (min-width: 640px) {
    .modal-container {
      max-width: 640px;
    }
  }

  @media (min-width: 768px) {
    .modal-container {
      max-width: 768px;
    }
  }

  @media (min-width: 1024px) {
    .modal-container {
      max-width: 1024px;
    }
  }

  @media (min-width: 1280px) {
    .modal-container {
      max-width: 1280px;
    }
  }

  @media (min-width: 1536px) {
    .modal-container {
      max-width: 1536px;
    }
  }

  .modal {
    position: fixed;
    z-index: 500;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(4px);
  }
  .modal-container {
    position: relative;
    padding: 0 var(--size-8);
    margin: var(--size-8) auto;
    height: 100%;
    max-height: calc(100% - var(--size-16));
    overflow-y: hidden;
  }
  .close {
    position: absolute;
    top: var(--block-label-margin);
    right: var(--block-label-margin);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: var(--shadow-drop);
    border: 1px solid var(--border-color-primary);
    border-top: none;
    border-right: none;
    border-radius: var(--block-label-right-radius);
    background: var(--block-label-background-fill);
    padding: 6px;
    width: 24px;
    height: 24px;
    color: var(--block-label-text-color);
    font: var(--font);
    font-size: var(--button-small-text-size);
    cursor: pointer;
    z-index: 2;
  }
  .modal-content {
    padding-top: calc(24px + var(--block-label-margin) * 2);
    margin: 10px;
  }
  .modal :global(.modal-block) {
    max-height: 100%;
    overflow-y: auto !important;
  }

  .hide {
    display: none;
  }

  .confirmation-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 600;
  }

  .confirmation-content {
    background-color: var(--background-fill-primary);
    color: var(--body-text-color);
    padding: 2rem;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-drop-lg);
    text-align: center;
    width: 90%;
    max-width: 400px;
  }

  .confirmation-content h3 {
    margin-top: 0;
    font-size: var(--text-lg);
    font-weight: var(--weight-medium);
  }

  .confirmation-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
  }

  .confirmation-buttons button {
    padding: 0.5rem 1.5rem;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: var(--text-sm);
    font-weight: var(--weight-medium);
    transition: background-color 0.3s ease;
  }

  .confirmation-buttons .yes-button {
    background-color: var(--primary-500);
    color: white;
    box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.1);
  }

  .confirmation-buttons .yes-button:hover {
    background-color: var(--primary-600);
  }

  .confirmation-buttons .no-button {
    background-color: gray;
    color: white;
    box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.1);
  }

  .confirmation-buttons .no-button:hover {
    background-color: darkgray;
  }
</style>
