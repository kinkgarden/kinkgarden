<script>
    import { dbData } from "./index.js";

    let categories = $dbData.categories;
    export let selectedCategory = null;
</script>

<style>
    .category-menu {
        flex: 0 0 12em;
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
        background-color: #b347cc;
        color: #ffffff;
    }

    .category-menu .category.selected {
        background-color: #743582;
        color: #ffecff;
    }
</style>

<div class="category-menu">
    <h2>Categories</h2>
    <div class="categories">
        <div
            class="category"
            class:selected={selectedCategory === null}
            on:click={(_) => (selectedCategory = null)}>
            All Kinks
        </div>
        {#each categories as category}
            <div
                class="category"
                class:selected={selectedCategory === category.id}
                on:click={(_) => (selectedCategory = category.id)}>
                {category.name}
            </div>
        {/each}
    </div>
</div>
