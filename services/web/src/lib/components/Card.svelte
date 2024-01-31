<script lang="ts">
  import type { Restaurant } from "$lib/types/models";
  export let restaurant: Restaurant;
</script>


<div class="card">
  <img src="/restaurant.avif" alt={restaurant.restaurant} />
  <h2>{restaurant.restaurant}</h2>
  <p>{restaurant.address}</p>
</div>


<style>
  .card {
    width: 300px;
    border: 1px solid #ddd;
    border-radius: 5px;
    overflow: hidden;
    margin: 10px;
    padding: 10px;
  }
  .card img {
    width: 100%;
    height: 200px;
    object-fit: cover;
  }
  .card h2, .card p {
    margin: 0 0 10px 0;
  }
</style>