import { json, fail } from '@sveltejs/kit';
import { user } from '$lib/stores/user'


export async function POST({ request }) {
    try {
        const body = await request.json()
        const { userId } = body

        // Sets userId for the entire app <- This is just for demo purposes
        user.set(userId)

        return json({ userId })
    } catch (error) {
        throw fail(500, { message: error.message ?? 'Could not change the logged in user' })
    }
}
