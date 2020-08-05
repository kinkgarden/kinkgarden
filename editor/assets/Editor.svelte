<div class="link-box-wrapper">
    <input type="text" disabled value={listUrl}>
</div>
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

<script>
    import CategoryMenu from './CategoryMenu.svelte';
    import KinkMenu from './KinkMenu.svelte';

    function decode_one(data) {
        let header = data.slice(0, 2);
        let column = header[0] >> 6;
        let type = header[0] >> 5 & 0b1;
        let intensity = header[0] >> 3 & 0b11;
        let rest = (header[0] & 0b111) << 8 | header[1];
        if (type === 0) {
            return [column, false, intensity, rest, data.slice(2)];
        } else {
            let text = data.slice(2, 2 + rest);
            const decoder = new TextDecoder('utf-8');
            text = decoder.decode(text);
            return [column, true, intensity, text, data.slice(2 + rest)];
        }
    }

    function encode_one([column, custom, intensity, value]) {
        let length = 2 + (custom ? value.length : 0);
        let result = new Uint8Array(length);
        if (custom) {
            const encoder = new TextEncoder('utf-8');
            let text = encoder.encode(value);
            result.set(text, 2);
            value = value.length;
        }
        let type = custom ? 1 : 0;
        result[0] = (column << 6 | type << 5 | intensity << 3 | ((value >> 8) & 0b111));
        result[1] = value & 0b11111111;
        return result;
    }

    function decode_all(data) {
        let result = [];
        while (data.length > 0) {
            let [column, custom, intensity, value, new_data] = decode_one(data);
            data = new_data;
            result.push([column, custom, intensity, value]);
        }
        return result;
    }

    function encode_all(kinks) {
        let pieces = kinks.map(encode_one);
        let total_length = pieces.map(x => x.length).reduce((a, b) => a + b, 0);
        let data = new Uint8Array(total_length);
        let position = 0;
        for (let piece of pieces) {
            data.set(piece, position);
            position += piece.length;
        }
        return data;
    }

    function hydrate(data) {
        let decoded = decode_all(data);
        let columns = [
            {name: "heart", kinks: []},
            {name: "check", kinks: []},
            {name: "tilde", kinks: []},
            {name: "no", kinks: []}
        ];
        for (let [column, custom, intensity, value] of decoded) {
            columns[column].kinks.push([custom, intensity, value]);
        }
        return columns;
    }

    function dehydrate(columns) {
        let data = [];
        for (let i = 0; i < columns.length; i++) {
            for (let [custom, intensity, value] of columns[i].kinks) {
                if (custom) {
                    // TODO figure out custom kinks
                }
                data.push([i, custom, intensity, value]);
            }
        }
        return encode_all(data);
    }

    function deserialize(hash) {
        hash = hash.replace(/!/g, '=');
        let string_data = atob(hash);
        let data = new Uint8Array(string_data.length);
        data.forEach((_, i) => data[i] = string_data.charCodeAt(i));
        return hydrate(data);
    }

    function serialize(columns) {
        let data = dehydrate(columns);
        let string_data = String.fromCharCode(...data);
        let b64 = btoa(string_data);
        return b64.replace(/=/g, '!');
    }

    function fetchKink(kink, dbData) {
        let [custom, intensity, value] = kink;
        if (custom) {
            let [name, description] = value.split('\n', 1);
            return {custom, intensity, name, description};
        } else {
            let {name, description} = dbData.kinks.find(k => k.id === value);
            return {custom, intensity, name, description, id: value};
        }
    }

    let columns = [
        {name: "heart", kinks: []},
        {name: "check", kinks: []},
        {name: "tilde", kinks: []},
        {name: "no", kinks: []}
    ];
    if (location.hash.startsWith('#')) {
        let hash = location.hash.substring(1);
        columns = deserialize(hash);
        console.log('Restoring', columns);
    }
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
        return columns.some(({kinks}) => kinks.some(k => k[2] === kink.id));
    }
    function isKinkUnused(kink) {
        return columns.every(({kinks}) => kinks.every(k => k[2] !== kink.id));
    }
    function isKinkInColumn(kink, column) {
        let kinks = columns[column].kinks;
        return kinks.some(k => k[2] === kink.id);
    }
    let full_columns;
    $: {
        full_columns =  columns.map(column => ({
            name: column.name,
            kinks: column.kinks.map(x => fetchKink(x, dbData)),
        }))
    }
    let urlInfo;
    $: {
        urlInfo = serialize(columns);
        history.replaceState(null, "", "#" + urlInfo);
    }
    let listUrl;
    $: {
        const urlInfo = serialize(columns);
        const url = new URL('/', location.href);
        url.search = urlInfo;
        url.hash = '';
        listUrl = url.href;
    }

    function select_category(category) {
        selectedCategory = category;
    }

    function toggleColumn(id, column) {
        if (columns[column].kinks.some(k => k[2] === id)) {
            columns[column].kinks = columns[column].kinks.filter(k => k[2] !== id);
        } else {
            columns.forEach(c => {
                c.kinks = c.kinks.filter(k => k[2] !== id)
            });
            columns[column].kinks.push([false, 0, id]);
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
                columns[column].kinks = [...columns[column].kinks, [false, 0, id]];
                columns = columns;
            });
        }
    }

    function dragend(event, column) {
        const data = event.dataTransfer;
        if (data.dropEffect === "move" && column !== null) {
            let id = parseInt(event.target.dataset.id);
            columns[column].kinks = columns[column].kinks.filter(k => k[2] !== id);
            columns = columns;
        }
    }
</script>
