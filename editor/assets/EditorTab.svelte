<script>
    import CategoryMenu from './CategoryMenu.svelte';
    import KinkMenu from './KinkMenu.svelte';

    export let dragstart, dragover, drop;
    let selectedCategory;
</script>

<div>
    <CategoryMenu bind:selectedCategory={selectedCategory} />
    <KinkMenu {selectedCategory} {dragstart} {dragover} {drop}  />
</div>

<style>
    div {
        display: flex;
        flex-flow: row nowrap;
    }
</style>
