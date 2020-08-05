<script>
    export let selectedKinks;
    export let columns;
    export let dragstart, dragover, drop;
    export let toggleColumn;

    let kinkColumn;
    $: {
        kinkColumn = {};
        for (let columnIndex = 0; columnIndex < columns.length; columnIndex++) {
            for (let kink of columns[columnIndex].kinks) {
                kinkColumn[kink[2]] = columnIndex;
            }
        }
    }
</script>

<div class="kink-menu">
    <h2>Kinks</h2>
    <div class="kinks menu-kinks" on:dragover|preventDefault={event => dragover(event, null)} on:drop|preventDefault={event => drop(event, null)}>
        {#each selectedKinks as kink}
        <div class="kink" class:selected={kinkColumn[kink.id] !== undefined} draggable={kinkColumn[kink.id] === undefined ? 'true' : 'false'} on:dragstart={event => dragstart(event, true)} data-id={kink.id}>
            <p title={kink.description}>{kink.name}</p>
            <p class="description">{kink.description}</p>
            <div class="shortcuts">
                <button class="shortcut" class:selected={kinkColumn[kink.id] === 0} data-target="0" on:click={_ => toggleColumn(kink.id, 0)}>
                    <svg class="icon heart"><use xlink:href="#heart"></use></svg>
                </button>
                <button class="shortcut" class:selected={kinkColumn[kink.id] === 1} data-target="1" on:click={_ => toggleColumn(kink.id, 1)}>
                    <svg class="icon check"><use xlink:href="#check"></use></svg>
                </button>
                <button class="shortcut" class:selected={kinkColumn[kink.id] === 2} data-target="2" on:click={_ => toggleColumn(kink.id, 2)}>
                    <svg class="icon tilde"><use xlink:href="#tilde"></use></svg>
                </button>
                <button class="shortcut" class:selected={kinkColumn[kink.id] === 3} data-target="3" on:click={_ => toggleColumn(kink.id, 3)}>
                    <svg class="icon no"><use xlink:href="#no"></use></svg>
                </button>
            </div>
        </div>
        {/each}
    </div>
</div>
