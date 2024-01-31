import path from 'path';
import { json, fail } from '@sveltejs/kit';
import { getRestaurant } from "$lib/services/backend";
import { get } from "svelte/store";
import { user } from "$lib/stores/user";
import { decrypt, loadPrivateKey, loadPublicKey, checkHashes } from "$lib/services/security";


export async function GET({ params }) {
  try {
    const data = await getRestaurant(params.id)

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

    // console.log('vouchers', data.data.user_vouchers)

    // Decrypts the voucher data
    for (const voucher of data.data.user_vouchers) {
      try {
        const hashedData = decrypt(privateKey, publicKey, voucher.data);
        voucher.data = JSON.parse(hashedData);
      } catch (error) {
        return json({
          authenticity: false,
        })
      }
    }

    // console.log('vouchers decrypted', data.data.user_vouchers)

    return json({
      authenticity: true,
      restaurant: data.data
    })
  } catch (error) {
    throw fail(500, { message: error.message ?? 'Error fetching restaurant' })
  }
}
