<script>
    export let options;

    let selectedIndex = 0;
    let open = true;

    let selection;
    $: selection = options[selectedIndex].component;

    function click(index) {
        selectedIndex = index;
        open = true;
    }
</script>

<aside>
    <svelte:component this={selection} {...$$restProps} />
    <nav>
        {#each options as option, i}
            <button type="button" disabled={selectedIndex === i} on:click={() => click(i)}>{option.label}</button>
        {/each}
    </nav>
</aside>

<style>
    aside {
        flex: 2 0 0;
        display: flex;
        flex-flow: row nowrap;
        justify-content: space-between;
        align-items: stretch;
        height: 100%;
    }

    aside nav {
        flex: 0;
    }
</style>
