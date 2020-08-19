<script>
    import { dbData } from './index.js';

    let categories = $dbData.categories;
    export let selectedCategory = null;
</script>

<div class="category-menu">
    <h2>Categories</h2>
    <ul>
        <li class:selected={selectedCategory === null} on:click={_ => selectedCategory = null}>all kinks</li>
        <li class:selected={selectedCategory === 'custom'} on:click={_ => selectedCategory = 'custom'}>custom kinks</li>
    {#each categories as category}
        <li class:selected={selectedCategory === category.id} on:click={_ => selectedCategory = category.id}>{category.name}</li>
    {/each}
    </ul>
</div>

<style>
    .category-menu {
        flex: 1 0 0;
        display: flex;
        flex-flow: column nowrap;
    }

    .category-menu ul {
        list-style: none;
        padding-left: 0;
    }

    .category-menu ul li {
        padding: 0.5em;
        cursor: pointer;
    }

    .category-menu ul li:hover {
        background-color: #B347CC;
        color: #ffffff;
    }

    .category-menu ul li.selected {
        background-color: #743582;
        color: #FFECFF;
    }
</style>
