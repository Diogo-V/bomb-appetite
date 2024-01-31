import path from 'path';
import { json, fail } from '@sveltejs/kit';
import { createReview } from "$lib/services/backend";
import { get } from "svelte/store";
import { user } from "$lib/stores/user";
import { decrypt, loadPrivateKey, loadPublicKey, checkHashes, sign } from "$lib/services/security";


export async function POST({ request }) {
  try {
    const body = await request.json()
    const { restaurantId, userId, stars, comment } = body

    // Loads user's private key and server's public key
    const privateKeyPath = path.resolve(`./src/lib/secrets/user_${get(user)}_private_key.pem`)
    const privateKey = loadPrivateKey(privateKeyPath);
    const publicKeyPath = path.resolve('./src/lib/secrets/server_public_key.pem');
    const publicKey = loadPublicKey(publicKeyPath);

    // Hash the review
    const review = JSON.stringify({ restaurantId, userId, stars, comment });
    const signature = sign(privateKey, review);

    const data = await createReview(restaurantId, userId, stars, comment, signature)

    // Decrypts the signature
    const hashedData = decrypt(privateKey, publicKey, data.signature);

    // Verifies the signature
    if (!checkHashes(JSON.stringify(data.data), hashedData)) {
      return json({
        authenticity: false,
      })
    }

    return json({
      authenticity: true,
      review: data.data,
    })
  } catch (error) {
    throw fail(500, { message: error.message ?? 'Error creating review' })
  }
}
