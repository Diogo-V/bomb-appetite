<script lang="ts">
  import type { Restaurant } from "$lib/types/models";
  import { goto } from '$app/navigation';
  import Card from '$lib/components/Card.svelte';
  import { user } from "$lib/stores/user";

  export let data;
  let restaurants = data.restaurants as Restaurant[];
  let authenticity = data.authenticity as boolean;

  let user_ids: number[] = [1, 2, 3, 4]

  async function changeUser(e: Event) {
    const user_id = (e.target as HTMLSelectElement).value;

    const result = await fetch("/api/auth", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ userId: user_id })
    });

    if (result.ok) {
      user.set(Number(user_id));
    } else {
      alert("Could not change user");
    }
  }
</script>

{#if authenticity}
  <div class="header">
    <div class="logo" on:click={() => goto("/")}>
      <h1>BombAppetit</h1>
    </div>

    <select class="user-dropdown" on:change={changeUser}>
      {#each user_ids as user_id (user_id)}
        <option value={user_id} selected={$user === user_id}>User {user_id}</option>
      {/each}
    </select>
  </div>
  <div class="grid">
    {#each restaurants as restaurant (restaurant.id)}
      <div on:click={() => goto(`/${restaurant.id}`)}>
        <Card restaurant={restaurant} />
      </div>
    {/each}
  </div>
{:else}
  <div>
    <h1>The data has been tampered with</h1>
  </div>
{/if}




<style>
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin: 0 10vw;
  }

  .user-dropdown {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #ccc;
    border-radius: 4px;
    background-color: #f8f8f8;
    transition: all 0.3s ease;
  }

  .user-dropdown:hover {
    border-color: #888;
  }

  .logo h1 {
    cursor: pointer;
  }
  
  .grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);

    gap: 20px;
  }

  .grid div {
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }
</style>