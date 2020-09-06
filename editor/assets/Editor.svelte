<script>
    import TabSelector from "./TabSelector.svelte";
    import EditorTab from "./EditorTab.svelte";
    import CustomTab from "./CustomTab.svelte";
    import SaveTab from "./SaveTab.svelte";
    import { dbData, columns, customData } from "./index.js";

    function fetchKink(kink, kinkData) {
        let { name, description, id } = kinkData.find((k) => k.id === kink.id);
        return { custom: kink.custom, name, description, id };
    }

    export let action = "";

    let full_columns;
    $: {
        full_columns = $columns.map((column) => ({
            name: column.name,
            kinks: column.kinks.map((x) =>
                fetchKink(x, x.custom ? $customData : dbData.kinks)
            ),
        }));
    }

    let viewPassword = "";
    let editPassword = "";

    function dragstart(event, fromMenu) {
        if (fromMenu) {
            event.dataTransfer.effectAllowed = "copy";
        } else {
            event.dataTransfer.effectAllowed = "move";
        }
        let kink = {
            id: parseInt(event.target.dataset.id),
            custom: event.target.dataset.custom === "true",
        };
        event.dataTransfer.setData("application/json", JSON.stringify(kink));
    }

    function dragover(event, column) {
        // can't reject illegitimate drags because we can't get the data out of the drag event 😔
        event.dataTransfer.dropEffect = event.dataTransfer.effectAllowed;
    }

    function drop(event, column) {
        if (column !== null) {
            const data = event.dataTransfer;
            let { id, custom } = JSON.parse(data.getData("application/json"));
            // must defer so that if we drag to ourself we add after we remove
            // (there are almost certainly better ways to handle this)
            setTimeout(() => {
                $columns[column].kinks = [
                    ...$columns[column].kinks,
                    { custom, id },
                ];
            });
        }
    }

    function dragend(event, column) {
        const data = event.dataTransfer;
        if (data.dropEffect === "move" && column !== null) {
            let id = parseInt(event.target.dataset.id);
            let custom = event.target.dataset.custom === "true";
            $columns[column].kinks = $columns[column].kinks.filter(
                (k) => k.id !== id || k.custom !== custom
            );
        }
    }
</script>

<article>
    <TabSelector
        options={[{ component: EditorTab, label: 'Editor' }, { component: CustomTab, label: 'Custom' }, { component: SaveTab, label: 'Save' }]}
        {dragstart}
        {dragover}
        {drop}
        saveFormAction={action}
        {fetchKink} />
    {#each full_columns as column, i}
        <div
            class="column"
            on:dragover|preventDefault={(event) => dragover(event, i)}
            on:drop|preventDefault={(event) => drop(event, i)}>
            <h2>
                <svg class="icon {column.name}">
                    <use xlink:href="#{column.name}" />
                </svg>
            </h2>
            <div class="kinks" data-kink-column={i}>
                {#each column.kinks as kink}
                    <div
                        class="kink"
                        draggable="true"
                        on:dragstart={(event) => dragstart(event, false)}
                        on:dragend={(event) => dragend(event, i)}
                        data-id={kink.id}
                        data-custom={kink.custom}>
                        <p title={kink.description}>{kink.name}</p>
                        <p class="description">{kink.description}</p>
                    </div>
                {/each}
            </div>
        </div>
    {/each}
</article>
