<script>
    export let categories;
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
