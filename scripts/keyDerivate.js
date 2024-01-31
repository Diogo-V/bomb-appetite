const crypto = require('crypto');

const debug = false;

function deriveKey(privateKey, publicKey) {

  const sharedSecret = crypto.diffieHellman({
    privateKey,
    publicKey,
    privateKeyEncoding: {
      format: 'pem',
      type: 'pkcs8'
    },
    publicKeyEncoding: {
      format: 'pem',
      type: 'spki'
    }
  });

  return sharedSecret;
}
module.exports = { deriveKey };

if (require.main === module) {
  const keyGenerate = require('./keyGenerate');

  const aliceKeyPair = keyGenerate.generateKeyPair();
  const bobKeyPair = keyGenerate.generateKeyPair();

  if (debug) {
    console.log('Alice private key: ', aliceKeyPair.privateKey);
    console.log('Alice public key: ', aliceKeyPair.publicKey);
    console.log('Bob private key: ', bobKeyPair.privateKey);
    console.log('Bob public key: ', bobKeyPair.publicKey);
    console.log()
  }

  const sharedSecret1 = deriveKey(aliceKeyPair.privateKey, bobKeyPair.publicKey);
  const sharedSecret2 = deriveKey(bobKeyPair.privateKey, aliceKeyPair.publicKey);

  if (debug) {
    console.log('Shared secret 1: ', sharedSecret1);
    console.log('Shared secret 2: ', sharedSecret2);
  }

  console.assert(sharedSecret1, sharedSecret2);

  console.log("All tests passed!");
}


