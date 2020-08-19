<script>
    import { dbData } from './index.js';

    let categories = $dbData.categories;
    export let selectedCategory = null;
</script>

<div class="category-menu">
    <h2>Categories</h2>
    <div class="categories">
        <div class="category" class:selected={selectedCategory === null} on:click={_ => selectedCategory = null}>all kinks</div>
        <div class="category" class:selected={selectedCategory === 'custom'} on:click={_ => selectedCategory = 'custom'}>custom kinks</div>
    {#each categories as category}
        <div class="category" class:selected={selectedCategory === category.id} on:click={_ => selectedCategory = category.id}>{category.name}</div>
    {/each}
    </div>
</div>

<style>
    .category-menu {
        flex: 1 0 0;
        display: flex;
        flex-flow: column nowrap;
    }

    .category-menu .categories {
        overflow-y: scroll;
        flex: 1 1 0;
    }

    .category-menu .category {
        padding: 0.5em;
        cursor: pointer;
    }

    .category-menu .category:hover {
        background-color: #B347CC;
        color: #ffffff;
    }

    .category-menu .category.selected {
        background-color: #743582;
        color: #FFECFF;
    }
</style>
