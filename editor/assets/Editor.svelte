<article>
    <aside>
        <CategoryMenu {categories} bind:selectedCategory={selectedCategory} />
        <KinkMenu {selectedKinks} {columns} {toggleColumn} {dragstart} {dragover} {drop}  />
    </aside>
    {#each full_columns as column, i}
    <div class="column" on:dragover|preventDefault={event => dragover(event, i)} on:drop|preventDefault={event => drop(event, i)}>
        <h2><svg class="icon {column.name}"><use xlink:href="#{column.name}"></use></svg></h2>
        <div class="kinks" data-kink-column={i}>
            {#each column.kinks as kink}
            <div class="kink" draggable="true" on:dragstart={event => dragstart(event, false)} on:dragend={event => dragend(event, i)} data-id={kink.id}>
                <p title={kink.description}>{kink.name}</p>
                <p class="description">{kink.description}</p>
            </div>
            {/each}
        </div>
    </div>
    {/each}
</article>
<form method="post" action={action} on:submit={submitForm}>
    <input type="hidden" name="kink-list-data" value="">
    <input type="hidden" name="csrfmiddlewaretoken" value="">
    <fieldset>
        <label>
            View Password
            <input type="password" name="view-password">
        </label>
        <p>If set, will require anyone who wants to view this kink list to first enter this password, even if they have the URL. For the truly secretive.</p>
    </fieldset>
    <fieldset>
        <label>
            Edit Password
            <input type="password" name="edit-password">
        </label>
        <p>If set, will let you come back and use the same password to edit the list without making a new one.</p>
    </fieldset>
    <input type="submit" value="Save">
</form>

<script>
    import CategoryMenu from './CategoryMenu.svelte';
    import KinkMenu from './KinkMenu.svelte';
    import Cookies from 'js-cookie';

    function fetchKink(kink, dbData) {
        if (kink.custom) {
            return kink;
        } else {
            let {name, description, id} = dbData.kinks.find(k => k.id === kink.id);
            return {custom: false, name, description, id};
        }
    }

    export let initData = {
        columns: [
            {name: "heart", kinks: []},
            {name: "check", kinks: []},
            {name: "tilde", kinks: []},
            {name: "no", kinks: []}
        ],
        action: '',
    };
    let columns = initData.columns;
    const action = initData.action;
    console.log(columns, action);
    export let dbData;
    let selectedCategory = null;

    const categories = dbData.categories;
    let selectedKinks;
    $: {
        if (selectedCategory === null) {
            selectedKinks = dbData.kinks;
        } else if (selectedCategory === 'custom') {
            // TODO what do
            selectedKinks = [];
        } else {
            selectedKinks = dbData.kinks.filter(k => k.category_id === selectedCategory);
        }
    }
    function isSelected(c) {
        return selectedCategory === c;
    }
    function isKinkUsed(kink) {
        return columns.some(({kinks}) => kinks.some(k => k.id === kink.id));
    }
    function isKinkUnused(kink) {
        return columns.every(({kinks}) => kinks.every(k => k.id !== kink.id));
    }
    function isKinkInColumn(kink, column) {
        let kinks = columns[column].kinks;
        return kinks.some(k => k.id === kink.id);
    }
    let full_columns;
    $: {
        full_columns =  columns.map(column => ({
            name: column.name,
            kinks: column.kinks.map(x => fetchKink(x, dbData)),
        }))
    }

    let viewPassword = '';
    let editPassword = '';

    function select_category(category) {
        selectedCategory = category;
    }

    function toggleColumn(id, column) {
        if (columns[column].kinks.some(k => k.id === id)) {
            columns[column].kinks = columns[column].kinks.filter(k => k.id !== id);
        } else {
            columns.forEach(c => {
                c.kinks = c.kinks.filter(k => k.id !== id)
            });
            columns[column].kinks.push({custom: false, id});
        }
        columns = columns;
    }

    function dragstart(event, fromMenu) {
        if (fromMenu) {
            event.dataTransfer.effectAllowed = "copy";
        } else {
            event.dataTransfer.effectAllowed = "move";
        }
        let id = event.target.dataset.id;
        event.dataTransfer.setData("text/plain", id);
    }

    function dragover(event, column) {
        // can't reject illegitimate drags because we can't get the data out of the drag event 😔
        event.dataTransfer.dropEffect = event.dataTransfer.effectAllowed;
    }

    function drop(event, column) {
        if (column !== null) {
            const data = event.dataTransfer;
            let id = parseInt(data.getData("text/plain"));
            // must defer so that if we drag to ourself we add after we remove
            // (there are almost certainly better ways to handle this)
            setTimeout(() => {
                columns[column].kinks = [...columns[column].kinks, {custom: false, id}];
                columns = columns;
            });
        }
    }

    function dragend(event, column) {
        const data = event.dataTransfer;
        if (data.dropEffect === "move" && column !== null) {
            let id = parseInt(event.target.dataset.id);
            columns[column].kinks = columns[column].kinks.filter(k => k.id !== id);
            columns = columns;
        }
    }

    function submitForm(event) {
        const form = event.currentTarget;
        form.elements['kink-list-data'].value = JSON.stringify(columns);
        form.elements['csrfmiddlewaretoken'].value = Cookies.get('csrftoken');
    }
</script>
