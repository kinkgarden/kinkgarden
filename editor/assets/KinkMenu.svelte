<script>
    import { dbData, columns } from "./index.js";
    import Fuse from "fuse.js";
    export let selectedCategory;
    export let dragstart, dragover, drop;

    const fuse = new Fuse($dbData.kinks, {
        keys: ["name", "description"],
    });

    let searchText = "";

    let selectedKinks;
    $: {
        if (selectedCategory === null) {
            selectedKinks = $dbData.kinks;
        } else if (selectedCategory === "custom") {
            // TODO what do
            selectedKinks = [];
        } else {
            selectedKinks = $dbData.kinks.filter(
                (k) => k.category_id === selectedCategory
            );
        }
    }

    let searchedKinks;
    $: {
        if (searchText.length > 0) {
            searchedKinks = fuse.search(searchText).map((x) => x.item);
        } else {
            searchedKinks = selectedKinks;
        }
    }

    let kinkColumn;
    $: {
        kinkColumn = {};
        for (
            let columnIndex = 0;
            columnIndex < $columns.length;
            columnIndex++
        ) {
            for (let kink of $columns[columnIndex].kinks) {
                kinkColumn[kink.id] = columnIndex;
            }
        }
    }

    function toggleColumn(id, column) {
        if ($columns[column].kinks.some((k) => k.id === id)) {
            $columns[column].kinks = $columns[column].kinks.filter(
                (k) => k.id !== id
            );
        } else {
            $columns.forEach((c) => {
                c.kinks = c.kinks.filter((k) => k.id !== id);
            });
            $columns[column].kinks = [
                ...$columns[column].kinks,
                { custom: false, id },
            ];
        }
    }
</script>

<style>
    .kink-menu {
        flex: 0 1 auto;
        display: flex;
        flex-flow: column nowrap;

        width: 20em;
    }

    .kinks.menu-kinks {
        overflow-y: auto;
        flex: 1 1 0;
    }

    .kinks.menu-kinks p.description {
        display: unset;
    }

    .kink {
        position: relative;

        --icon-rows: 2;
        --icon-columns: 2;

        --icon-size: calc(28px / var(--icon-rows));
        --margin-size: 1px;

        --grid-size: calc(var(--icon-size) + 2 * var(--margin-size));
    }

    .kink p:first-child {
        padding-right: calc(var(--icon-columns) * var(--grid-size));
    }

    .kink.selected > :not(.shortcuts) {
        opacity: 0.6;
        font-weight: lighter;
    }

    .kink .shortcuts {
        position: absolute;
        top: 0;
        right: 0;

        display: grid;
        grid-template-columns: repeat(var(--icon-columns), var(--grid-size));
        grid-template-rows: repeat(var(--icon-rows), var(--grid-size));
    }

    .kink .shortcut {
        padding: 0;
        margin: 0;
        border-width: 0;
        background: none;
    }

    .kink .shortcut svg {
        box-sizing: border-box;
        padding: var(--margin-size);
        width: 100%;
        height: 100%;
    }

    .kink .shortcut:not(.selected) svg {
        background-color: var(--color);
        fill: #ffffff;
    }

    input {
        font: inherit;
    }

    @media (max-width: 90em) {
        .kink {
            --icon-rows: 1;
            --icon-columns: 4;
        }
    }
</style>

<div class="kink-menu">
    <h2>Kinks</h2>
    <input
        type="search"
        placeholder="Search kinks..."
        bind:value={searchText}
        aria-label="search kinks" />
    <div
        class="kinks menu-kinks"
        on:dragover|preventDefault={(event) => dragover(event, null)}
        on:drop|preventDefault={(event) => drop(event, null)}>
        {#each searchedKinks as kink}
            <div
                class="kink"
                class:selected={kinkColumn[kink.id] !== undefined}
                draggable={kinkColumn[kink.id] === undefined ? 'true' : 'false'}
                on:dragstart={(event) => dragstart(event, true)}
                data-id={kink.id}>
                <p title={kink.description}>{kink.name}</p>
                <p class="description">{kink.description}</p>
                <div class="shortcuts">
                    <button
                        class="shortcut"
                        class:selected={kinkColumn[kink.id] === 0}
                        data-target="0"
                        on:click={(_) => toggleColumn(kink.id, 0)}>
                        <svg class="icon heart">
                            <use xlink:href="#heart" />
                        </svg>
                    </button>
                    <button
                        class="shortcut"
                        class:selected={kinkColumn[kink.id] === 1}
                        data-target="1"
                        on:click={(_) => toggleColumn(kink.id, 1)}>
                        <svg class="icon check">
                            <use xlink:href="#check" />
                        </svg>
                    </button>
                    <button
                        class="shortcut"
                        class:selected={kinkColumn[kink.id] === 2}
                        data-target="2"
                        on:click={(_) => toggleColumn(kink.id, 2)}>
                        <svg class="icon tilde">
                            <use xlink:href="#tilde" />
                        </svg>
                    </button>
                    <button
                        class="shortcut"
                        class:selected={kinkColumn[kink.id] === 3}
                        data-target="3"
                        on:click={(_) => toggleColumn(kink.id, 3)}>
                        <svg class="icon no">
                            <use xlink:href="#no" />
                        </svg>
                    </button>
                </div>
            </div>
        {/each}
    </div>
</div>
