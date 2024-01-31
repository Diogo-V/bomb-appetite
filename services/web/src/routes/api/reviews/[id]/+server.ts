import path from 'path';
import { json, fail } from '@sveltejs/kit';
import { getReview } from "$lib/services/backend";
import { get } from "svelte/store";
import { user } from "$lib/stores/user";
import { decrypt, loadPrivateKey, loadPublicKey, checkHashes, verify } from "$lib/services/security";


export async function PUT({ params }) {
  try {
    // Fetches the review again from the backend
    const data = await getReview(params.id)

    // Loads user's private key and server's public key
    const privateKeyPath = path.resolve(`./src/lib/secrets/user_${get(user)}_private_key.pem`)
    const privateKey = loadPrivateKey(privateKeyPath);
    const publicKeyPath = path.resolve('./src/lib/secrets/server_public_key.pem');
    const publicKey = loadPublicKey(publicKeyPath);

    // Decrypts the signature
    const hashedData = decrypt(privateKey, publicKey, data.signature);

    // Verifies the signature
    if (!checkHashes(JSON.stringify(data.data), hashedData)) {
      return json({
        authenticity: false,
      })
    }

    // Uses the public key from the user that entered the review to verify the signature
    const userPublicKeyPath = path.resolve(`./src/lib/secrets/user_${data.data.user_id}_public_key.pem`)
    const userPublicKey = loadPublicKey(userPublicKeyPath);

    // Verifies the signature
    const reviewData = JSON.stringify({ 
        restaurantId: data.data.restaurant_id, 
        userId: data.data.user_id,
        stars: data.data.rating, 
        comment: data.data.review 
    });

    // FIXME: DEMO
    const isValid = verify(userPublicKey, reviewData, data.data.signature);
    // const isValid = verify(userPublicKey, reviewData + "evil action", data.data.signature);

    console.log('data', data.data)
    console.log('isValid', isValid)

    return json({
      authenticity: true,
      is_valid: isValid,
    })
  } catch (error) {
    throw fail(500, { message: error.message ?? 'Error validating review' })
  }
}
