const fs = require('fs');
const keyGenerate = require('./keyGenerate');
const { StorageServiceFactory, StorageType } = require('./storageService');
const crypto = require('crypto');
const assert = require('assert');

const debug = false;
const keyStorageService = StorageServiceFactory.getStorageService(StorageType.FILE);

function storePublicKey(public_key, filepath) {
    if (debug) console.log("Storing public key...");

    const publicKeyPem = public_key.export({ type: 'spki', format: 'pem' });
    
    try {
        keyStorageService.store(publicKeyPem, filepath);
    } catch (e) {
        throw new Error(`Error writing public key: ${e}`);
    }
}

function storePrivateKey(private_key, filepath) {
    if (debug) console.log("Storing private key...");

    const privateKeyPem = private_key.export({ type: 'pkcs8', format: 'pem' });

    try {
        keyStorageService.store(privateKeyPem, filepath);
    } catch (e) {
        throw new Error(`Error writing private key: ${e}`);
    }
}

function loadPublicKey(filepath) {
    if (debug) console.log("Loading public key...");
    try {
        const publicKeyPem = keyStorageService.load(filepath);
        return crypto.createPublicKey(publicKeyPem);
    } catch (e) {
        throw new Error(`Error reading public key: ${e}. Please provide a valid PEM-encoded public key.`);
    }
}

function loadPrivateKey(filepath) {
    if (debug) console.log("Loading private key...");
    try {
        const privateKeyPem = keyStorageService.load(filepath);
        return crypto.createPrivateKey(privateKeyPem);
    } catch (e) {
        throw new Error(`Error reading private key: ${e}. Please provide a valid PEM-encoded private key.`);
    }
}

if (require.main === module) {
    const keyPair = keyGenerate.generateKeyPair();

    storePublicKey(keyPair.publicKey, "temp_public_key.pem");
    storePrivateKey(keyPair.privateKey, "temp_private_key.pem");

    const public_key_read = loadPublicKey("temp_public_key.pem");
    const private_key_read = loadPrivateKey("temp_private_key.pem");

    // compare the keys
    assert(keyPair.publicKey.export({ type: 'spki', format: 'pem' }) == public_key_read.export({ type: 'spki', format: 'pem' }));
    assert(keyPair.privateKey.export({ type: 'pkcs8', format: 'pem' }) == private_key_read.export({ type: 'pkcs8', format: 'pem' }));

    fs.unlinkSync("temp_public_key.pem");
    fs.unlinkSync("temp_private_key.pem");

    console.log("All tests passed.");
}

module.exports = {
    storePublicKey,
    storePrivateKey,
    loadPublicKey,
    loadPrivateKey
};
