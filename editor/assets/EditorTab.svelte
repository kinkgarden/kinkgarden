<script>
    import CategoryMenu from './CategoryMenu.svelte';
    import KinkMenu from './KinkMenu.svelte';

    export let dragstart, dragover, drop;
    let selectedCategory;
</script>

<CategoryMenu bind:selectedCategory={selectedCategory} />
<KinkMenu {selectedCategory} {dragstart} {dragover} {drop}  />
