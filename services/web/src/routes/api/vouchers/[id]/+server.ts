import path from 'path';
import { json, fail } from '@sveltejs/kit';
import { giftVoucher, getVoucher } from "$lib/services/backend";
import { get } from "svelte/store";
import { user } from "$lib/stores/user";
import { encrypt, decrypt, loadPrivateKey, loadPublicKey, sign } from "$lib/services/security";
import { verifyServerResponseAuthenticity } from "$lib/services/authentication";


export async function POST({ params, request }) {
  try {
    const body = await request.json()

    const getResponse = await getVoucher(params.id, body.code)

    const userPrivateKeyPath = path.resolve(`./src/lib/secrets/user_${get(user)}_private_key.pem`)
    const userPrivateKey = loadPrivateKey(userPrivateKeyPath);
    const serverPublicKeyPath = path.resolve('./src/lib/secrets/server_public_key.pem')
    const serverPublicKey = loadPublicKey(serverPublicKeyPath);

    if (verifyServerResponseAuthenticity(userPrivateKey, serverPublicKey, getResponse)) {
      return json({
        authenticity: false
      })
    }

    const originalVoucher = getResponse.data

    console.log("originalVoucherData", originalVoucher.data)

    // keys loaded by original owner
    const ogOwnerPrivateKeyPath = path.resolve(`./src/lib/secrets/user_${get(user)}_private_key.pem`)
    const ogOwnerPrivateKey = loadPrivateKey(ogOwnerPrivateKeyPath);
    const newOwnerPublicKeyPath = path.resolve(`./src/lib/secrets/user_${body.newOwner}_private_key.pem`)
    const newOwnerPublicKey = loadPublicKey(newOwnerPublicKeyPath);

    /* ------------- decrypts voucher BE + OG Owner && encrypts voucher OG Owner + New Owner ------------- */
    const ogOwnerBackendPlaintextVoucherData = decrypt(ogOwnerPrivateKey, serverPublicKey, originalVoucher.data)
    const ogOwnerNewOwnerCyphertextVoucherData = encrypt(ogOwnerPrivateKey, newOwnerPublicKey, ogOwnerBackendPlaintextVoucherData)


    /* -------------------------------------------------------------------------- */
    /*       WHAT IS HAPPENING HERE IS EXCHANGE OF VOUCHERDATA BETWEEN USERS      */
    /* -------------------------------------------------------------------------- */


    // keys loaded by new owner
    const newOwnerPrivateKeyPath = path.resolve(`./src/lib/secrets/user_${body.newOwner}_private_key.pem`)
    // const newOwnerPrivateKeyPath = path.resolve(`./src/lib/secrets/user_3_private_key.pem`)
    const newOwnerPrivateKey = loadPrivateKey(newOwnerPrivateKeyPath);
    const ogOwnerPublicKeyPath = path.resolve(`./src/lib/secrets/user_${get(user)}_private_key.pem`)
    const ogOwnerPublicKey = loadPublicKey(ogOwnerPublicKeyPath);

    /* ------------- decrypts voucher OG Owner + New Owner && encrypts voucher New Owner + BE ------------ */
    const newOwnerOgOwnerPlaintextVoucherData = decrypt(newOwnerPrivateKey, ogOwnerPublicKey, ogOwnerNewOwnerCyphertextVoucherData)
    const newOwnerBackendCyphertextVoucherData = encrypt(newOwnerPrivateKey, serverPublicKey, newOwnerOgOwnerPlaintextVoucherData)

    const newVoucherData = newOwnerBackendCyphertextVoucherData

    console.log("newVoucherData", newVoucherData)

    // let signature = sign(ogOwnerPrivateKey, body.newOwner)
    // signature += Buffer.from("my evil action", "utf-8").toString('hex')

    const signature = sign(ogOwnerPrivateKey, body.newOwner)

    console.log("signature", signature.toString('hex'))

    const postResponse = await giftVoucher(params.id, body.code, body.newOwner, newVoucherData.iv, newVoucherData.tag, newVoucherData.ciphertext, signature.toString('hex'))

    if (verifyServerResponseAuthenticity(userPrivateKey, serverPublicKey, getResponse)) {
      return json({
        authenticity: false,
      })
    }

    const post_data = postResponse.data

    return json({
      authenticity: true,
      is_gifted: post_data.is_gifted
    })
  } catch (error) {
    throw fail(500, { message: error.message ?? 'Error using voucher' })
  }
}
