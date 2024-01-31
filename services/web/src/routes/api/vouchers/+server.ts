import path from 'path';
import { json, fail } from '@sveltejs/kit';
import { useVoucher } from "$lib/services/backend";
import { get } from "svelte/store";
import { user } from "$lib/stores/user";
import { decrypt, loadPrivateKey, loadPublicKey, checkHashes, encrypt, hash } from "$lib/services/security";


export async function PUT({ request }) {
  try {
    const body = await request.json()

    // Loads user's private key and server's public key
    const privateKeyPath = path.resolve(`./src/lib/secrets/user_${get(user)}_private_key.pem`)
    const privateKey = loadPrivateKey(privateKeyPath);
    const publicKeyPath = path.resolve('./src/lib/secrets/server_public_key.pem');
    const publicKey = loadPublicKey(publicKeyPath);

    const hashedVoucherData = hash(JSON.stringify({ 
      code: body.code
    }))
    const signature = encrypt(privateKey, publicKey, hashedVoucherData);
    const data = await useVoucher(body.code, signature)

    // Decrypts the signature
    const hashedData = decrypt(privateKey, publicKey, data.signature);

    // Verifies the signature
    if (!checkHashes(JSON.stringify(data.data), hashedData)) {
      return json({
        authenticity: false,
      })
    }

    // Checks if the user could use the voucher
    if (data.data.can_use_voucher !== undefined && !data.data.can_use_voucher) {
      return json({
        authenticity: true,
        can_use_voucher: false
      })
    }

    return json({
      authenticity: true,
      is_used: data.data.is_used
    })
  } catch (error) {
    throw fail(500, { message: error.message ?? 'Error using voucher' })
  }
}
