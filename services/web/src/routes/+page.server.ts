import type { Restaurant } from '$lib/types/models'

export async function load({ fetch }) {
  const response = await fetch("/api/restaurants")
  const data = await response.json()
  return {
    restaurants: data.restaurants as Restaurant[],
    authenticity: data.authenticity as boolean
  }
}
