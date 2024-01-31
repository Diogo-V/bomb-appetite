const crypto = require('crypto');

function generateKeyPair() {
  const { privateKey, publicKey } = crypto.generateKeyPairSync('ec', {
    namedCurve: 'secp256k1',
    publicKeyEncoding: {
      type: 'spki',
      format: 'pem'
    },
    privateKeyEncoding: {
      type: 'pkcs8',
      format: 'pem'
    }
  });


  const importPrivateKey = crypto.createPrivateKey({ key: privateKey, format: 'pem', type: 'pkcs8' });
  const importPublicKey = crypto.createPublicKey({ key: publicKey, format: 'pem', type: 'spki' });
  return { privateKey: importPrivateKey, publicKey: importPublicKey };
}
module.exports = { generateKeyPair };

if (require.main === module) {
  const { privateKey, publicKey } = generateKeyPair();
  console.log(privateKey);
  console.log(publicKey);
}
