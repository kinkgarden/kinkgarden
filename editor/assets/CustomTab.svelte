<script>
    import { customData } from "./index.js";

    let editing = undefined;

    $: {
        if (editing !== undefined) {
            $customData = $customData.map((x) => {
                if (x.id === editing.id) {
                    return editing;
                } else {
                    return x;
                }
            });
        }
    }

    function addNew() {
        let newID = Math.max(...$customData.map((x) => x.id)) + 1;
        let newCustom = {
            id: newID,
            name: "",
            description: "",
        };
        editing = newCustom;
        $customData = [...$customData, newCustom];
        console.log($customData, editing);
    }
</script>

<style>
    div:not(.custom) {
        display: flex;
        flex-flow: column;
    }
</style>

<div>
    {#each $customData as custom}
        <div class="custom">
            {#if editing && editing.id === custom.id}
                <input type="text" bind:value={editing.name} />
                <input type="text" bind:value={editing.description} />
                <button type="button" on:click={() => (editing = undefined)}>
                    Save
                </button>
            {:else}
                <p>{custom.name}</p>
                <p>{custom.description}</p>
                <button type="button" on:click={() => (editing = custom)}>
                    Edit
                </button>
            {/if}
        </div>
    {/each}
    <button type="button" on:click={addNew}>Add</button>
</div>
