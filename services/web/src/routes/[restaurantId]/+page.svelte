<script lang="ts">
  import { user } from "$lib/stores/user";
  import type { Restaurant, Vouchers, Reviews } from "$lib/types/models";
  import { goto } from '$app/navigation';
  import ReviewModal from "./ReviewModal.svelte";

  export let data;
  let restaurant = data.restaurant as Restaurant;
  let authenticity = data.authenticity as boolean;
  let vouchers = data.restaurant.user_vouchers as Vouchers[];
  let reviews = data.restaurant.reviews as Reviews[];

  let user_ids: number[] = [1, 2, 3, 4]
  let user_id_to_gift_voucher = user_ids.find(id => id !== $user);

  let voucherCode = "";

  let showModal = false;

  async function useVoucher() {
    const res = await fetch(`/api/vouchers/`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code: voucherCode
      }),
    });

    if (res.ok) {
      const json = await res.json();
      console.log(json);

      // Used to catch unauthenticity
      if (json.can_use_voucher !== undefined && !json.can_use_voucher) {
        alert("You can't use that voucher!")
        voucherCode = "";
        return
      }

      // If was used, remove from list
      if (json.is_used) {
        const index = vouchers.findIndex((voucher) => voucher.code === voucherCode);
        vouchers.splice(index, 1);
        vouchers = vouchers  // Necessary to re-render
      } else {
        alert("Voucher not found!")
      }

      voucherCode = "";
    }
  }

async function giftVoucher(id: string, code: string, newOwner: string) {
  const res = await fetch(`/api/vouchers/${id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      code: code,
      newOwner: newOwner
    }),
  });

  if (res.ok) {
    const json = await res.json();
    console.log(json);

    const isGifted = json.is_gifted;
    if (isGifted) {
      alert("Voucher gifted!")
    } else {
      alert("Voucher not gifted!")
    }
  } else {
    console.error(res.statusText ?? 'Failed to gift voucher')
    alert("Voucher not gifted!")
  }
}

  async function createReview(stars: number, description: string) {
    const res = await fetch(`/api/reviews`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        restaurantId: restaurant.id,
        stars: stars,
        comment: description,
        userId: $user
      }),
    });

    if (res.ok) {
      const json = await res.json();
      authenticity = json.authenticity;
      reviews = [...reviews, json.review]
      showModal = false;
    } else {
      console.error(res.statusText ?? 'Failed to create review')
    }
  }

  async function verifyReview(id: number) {
    const res = await fetch(`/api/reviews/${id}`, {
      method: "PUT",
    });

    if (res.ok) {
      const json = await res.json();
      authenticity = json.authenticity;

      const isValid = json.is_valid;
      if (isValid) {
        alert("Review is valid!")
      } else {
        alert("Review is not valid!")
      }

    } else {
      console.error(res.statusText ?? 'Failed to verify review')
    }
  }
</script>


{#if authenticity}
  {#if showModal}
    <div class="overlay"></div>
    <div class="review-modal">
      <ReviewModal bind:showModal={showModal} handleSubmit={createReview} />
    </div>
  {/if}

  <a class="back-arrow" on:click={() => goto("/")}>
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
    </svg>
  </a>

  <div class="restaurant-info">
    <h1>{restaurant.restaurant}</h1>
    <p>{restaurant.genre}</p>
    <img src="/banner.jpg" alt={restaurant.restaurant} style="" />
  </div>

  <h2>Menu</h2>
  <div class="menu">
    {#each restaurant.menu as item (item.name)}
      <div class="menu-item">
        <h3>{item.name}</h3>
        <p>{item.price}</p>
      </div>
    {/each}
  </div>

  <h2>Vouchers</h2>
  <div class="vouchers">
    <div>
      <span>Enter your code: </span>
      <input type="text" bind:value={voucherCode} />
      <button on:click={useVoucher}>Submit</button>
    </div>
    <div>
      <h3>Your vouchers:</h3>
      {#each vouchers as voucher (voucher.id)}
        <div class="voucher">
          <h4>{voucher.data.code}</h4>
          <p>{voucher.data.description}</p>
          <div class="gift-voucher">
            <select class="user-dropdown" bind:value={user_id_to_gift_voucher}>
              {#each user_ids as user_id (user_id)}
                {#if user_id !== $user}
                  <option value={user_id}>User {user_id}</option>
                {/if}
              {/each}
            </select>
            <button on:click={() => giftVoucher(voucher.id, voucher.data.code, String(user_id_to_gift_voucher))}>Gift</button>
          </div>
        </div>
      {/each}
    </div>
  </div>

  <div style="display: flex; align-items: center;">
    <h2>Reviews</h2>
    <button style="margin-left: 10px" on:click={() => showModal = true}>+</button>
  </div>
  <div class="reviews">
    {#each reviews as review (review.id)}
      <div class="review">
        <h4>User {review.user_id}: {review.rating}/5</h4>
        <p>{review.review}</p>
        <button on:click={() => verifyReview(review.id)}>Verify</button>
      </div>
    {/each}
  </div>
{:else}
  <div>
    <h1>The data has been tampered with</h1>
  </div>
{/if}
  

<style>
  .back-arrow {
    position: absolute;
    top: 10px;
    left: 10px;
    cursor: pointer;
  }

  .back-arrow svg {
    width: 24px;
    height: 24px;
  }

  .restaurant-info {
    text-align: center;
  }
  
  .menu {
    list-style-type: none;
    padding: 0;
  }
  
  .menu-item {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
    margin-bottom: 10px;
  }

  .vouchers {
    list-style-type: none;
    padding: 0;
  }
  
  .voucher {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
    margin-bottom: 10px;
  }

  .reviews {
    list-style-type: none;
    padding: 0;
  }
  
  .review {
    border: 1px solid #ccc;
    padding: 10px;
    text-align: center;
    margin-bottom: 10px;
  }

  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* Semi-transparent black */
    backdrop-filter: blur(10px);
    z-index: 9998; /* Sit below the modal */
  }

  .review-modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    z-index: 9999; /* Ensure the modal sits on top of other elements */
  }
</style>
