<script>
    import CategoryMenu from "./CategoryMenu.svelte";
    import KinkMenu from "./KinkMenu.svelte";

    export let dragstart, dragover, drop;
    let selectedCategory;
</script>

<style>
    div {
        display: flex;
        flex-flow: row nowrap;
    }
</style>

<div>
    <CategoryMenu bind:selectedCategory />
    <KinkMenu {selectedCategory} {dragstart} {dragover} {drop} />
</div>
