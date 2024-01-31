const crypto = require('crypto');
const keyDerivate = require('./keyDerivate.js');

const debug = false;


function encrypt(privateKeyEncryptor, publicKeyDecryptor, plaintext) {
    if (debug) console.log("Encrypting...");

    const derivedKey = keyDerivate.deriveKey(privateKeyEncryptor, publicKeyDecryptor);

    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', derivedKey, iv);
    const ciphertext = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
    const tag = cipher.getAuthTag();

    const ivBase64 = iv.toString('base64');
    const tagBase64 = tag.toString('base64');
    const ciphertextBase64 = ciphertext.toString('base64');

    return {
        iv: ivBase64,
        tag: tagBase64,
        ciphertext: ciphertextBase64
    };
}

function decrypt(privateKeyDecryptor, publicKeyEncryptor, encryptedData) {
    if (debug) console.log("Decrypting...");

    const derivedKey = keyDerivate.deriveKey(privateKeyDecryptor, publicKeyEncryptor);

    const iv = Buffer.from(encryptedData.iv, 'base64');
    const tag = Buffer.from(encryptedData.tag, 'base64');
    const ciphertext = Buffer.from(encryptedData.ciphertext, 'base64');

    const decipher = crypto.createDecipheriv('aes-256-gcm', derivedKey, iv);
    decipher.setAuthTag(tag);

    let plaintext;
    try {
        plaintext = Buffer.concat([decipher.update(ciphertext), decipher.final()]).toString('utf8');
    } catch (error) {
        throw new Error("Authentication failed. Invalid ciphertext or key.");
    }

    return plaintext;
}

if (require.main === module) {
    const keyGenerate = require('./keyGenerate');
  
    const aliceKeyPair = keyGenerate.generateKeyPair();
    const bobKeyPair = keyGenerate.generateKeyPair();

    const plaintext = "Hello World!";
    const ciphertext = encrypt(aliceKeyPair.privateKey, bobKeyPair.publicKey, plaintext);
    const decryptedPlaintext = decrypt(bobKeyPair.privateKey, aliceKeyPair.publicKey, ciphertext);

    if (debug) {
        console.log();
        console.log("plaintext:           ", plaintext);
        console.log("ciphertext:          ", ciphertext);
        console.log("decryptedPlaintext: ", decryptedPlaintext);
        console.log();
    }

    if (plaintext === decryptedPlaintext) {
        console.log("All tests passed.");
    } else {
        console.log("Test failed.");
    }
}

module.exports = {
    encrypt,
    decrypt
};
