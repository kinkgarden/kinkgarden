<script>
    import { customData, columns } from "./index.js";

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
        let newID = Math.max(0, ...$customData.map((x) => x.id)) + 1;
        let newCustom = {
            id: newID,
            name: "",
            description: "",
        };
        editing = newCustom;
        $customData = [...$customData, newCustom];
    }

    function deleteEditing() {
        $columns = $columns.map(({ name, kinks }) => ({
            name,
            kinks: kinks.filter((k) => !k.custom || k.id !== editing.id),
        }));
        $customData = $customData.filter((x) => x.id !== editing.id);
        editing = undefined;
    }
</script>

<style>
    p {
        margin: 0;
    }

    div:not(.custom) {
        display: flex;
        flex-flow: column;
        overflow-y: auto;
    }

    button.add {
        padding: 1em 0;
    }

    div.custom {
        display: grid;
        grid-template-rows: 2em 4em;
        grid-template-columns: auto 4em;
        grid-template-areas:
            "name        actions    "
            "description description";
    }

    div.custom .name {
        grid-area: name;
    }

    div.custom .description {
        grid-area: description;
        overflow-y: auto;
    }

    div.custom .actions {
        grid-area: actions;
        display: flex;
        flex-flow: column;
    }

    div.custom .actions > * {
        flex: 1;
    }

    div.editing {
        grid-template-rows: 2em 2em 2em 4em;
        grid-template-areas:
            "namelabel   actions    "
            "name        actions    "
            "desclabel   desclabel  "
            "description description";
    }

    div.editing label.name {
        grid-area: namelabel;
    }

    div.editing label.description {
        grid-area: desclabel;
    }

    textarea,
    input {
        font-family: inherit;
        font-size: 90%;
    }

    textarea {
        resize: none;
    }

    p {
        overflow-wrap: anywhere;
    }
</style>

<div>
    {#each $customData as custom}
        {#if editing && editing.id === custom.id}
            <div class="custom editing">
                <label for="custom-name" class="name">Name</label>
                <input
                    id="custom-name"
                    class="name"
                    type="text"
                    maxlength="200"
                    bind:value={editing.name} />
                <label for="custom-description" class="description">
                    Description
                </label>
                <textarea
                    id="custom-description"
                    class="description"
                    maxlength="1000"
                    bind:value={editing.description} />
                <span class="actions">
                    <button
                        type="button"
                        on:click={() => (editing = undefined)}>
                        Save
                    </button>
                    <button type="button" on:click={deleteEditing}>
                        Delete
                    </button>
                </span>
            </div>
        {:else}
            <div class="custom">
                <p class="name">{custom.name}</p>
                <p class="description">{custom.description}</p>
                <span class="actions">
                    <button type="button" on:click={() => (editing = custom)}>
                        Edit
                    </button>
                </span>
            </div>
        {/if}
    {/each}
    {#if editing === undefined}
        <button type="button" class="add" on:click={addNew}>Add</button>
    {/if}
</div>
