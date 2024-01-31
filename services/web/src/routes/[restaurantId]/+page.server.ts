import type { Restaurant } from '$lib/types/models'

export async function load({ fetch, params }) {
  const data = await fetch(`/api/restaurants/${params.restaurantId}`).then(r => r.json())
  return {
    restaurant: data.restaurant as Restaurant,
    authenticity: data.authenticity as boolean
  }
}
