import path from 'path';
import { json, fail } from '@sveltejs/kit';
import { getRestaurants } from "$lib/services/backend";
import { get } from "svelte/store";
import { user } from "$lib/stores/user";
import { decrypt, loadPrivateKey, loadPublicKey, checkHashes } from "$lib/services/security";


export async function GET() {
  try {
    const data = await getRestaurants()

    // Loads user's private key and server's public key
    const privateKeyPath = path.resolve(`./src/lib/secrets/user_${get(user)}_private_key.pem`)
    const privateKey = loadPrivateKey(privateKeyPath);
    const publicKeyPath = path.resolve('./src/lib/secrets/server_public_key.pem');
    const publicKey = loadPublicKey(publicKeyPath);

    // Decrypts the signature
    const hashedData = decrypt(privateKey, publicKey, data.signature);

    // console.log('data', data.data)
    // console.log('hashedData', hashedData)

    // Verifies the signature
    // FIXME: DEMO
    if (!checkHashes(JSON.stringify(data.data), hashedData)) {
    // if (!checkHashes(JSON.stringify(data.data) + "evil action", hashedData)) {
      console.log('isValid', !checkHashes(JSON.stringify(data.data), hashedData))
      return json({
        authenticity: false,
      })
    }

    // console.log('isValid', !checkHashes(JSON.stringify(data.data), hashedData))

    return json({
      authenticity: true,
      restaurants: data.data
    })
  } catch (error) {
    throw fail(500, { message: error.message ?? 'Error fetching restaurants' })
  }
}
