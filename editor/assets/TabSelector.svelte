<script>
    export let options;

    let selectedIndex = 0;
    let open = true;

    let selection;
    $: selection = open ? options[selectedIndex].component : undefined;

    function click(index) {
        selectedIndex = index;
        open = true;
    }
</script>

<style>
    aside {
        display: flex;
        flex-flow: row nowrap;
        justify-content: stretch;
        align-items: stretch;
        height: 100%;
        flex: 0 1 content;
    }

    aside.open {
        flex-basis: 35em;
    }

    button {
        display: block;
    }

    button:not(:disabled) {
        cursor: pointer;
    }

    .tab-content {
        flex: 1 1 auto;
        position: relative;
        border: 1px solid currentColor;
    }

    .tab-content > :global(*) {
        width: 100%;
        height: 100%;
    }

    aside nav {
        flex: 0 0 content;
        display: flex;
        flex-flow: column;
        row-gap: 1em;
        position: relative;
        left: -1px;
    }

    nav button {
        font: inherit;
        color: inherit;
        background-color: inherit;
        border: 1px solid currentColor;
        border-top-right-radius: 0.5em;
        border-bottom-right-radius: 0.5em;
    }

    nav button:disabled {
        border-left-color: #2d1d2d;
    }
</style>

<aside class:open>
    {#if open}
        <div class="tab-content">
            <svelte:component this={selection} {...$$restProps} />
        </div>
    {/if}
    <nav>
        {#each options as option, i}
            <button
                type="button"
                disabled={selectedIndex === i && open}
                on:click={() => click(i)}>
                {option.label}
            </button>
        {/each}
        <button type="button" on:click={() => (open = !open)}>
            {open ? '←' : '→'}
        </button>
    </nav>
</aside>
