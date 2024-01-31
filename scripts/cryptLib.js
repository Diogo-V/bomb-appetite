const keyStorage = require('./keyStorage');
const keyGenerate = require('./keyGenerate');
const jsonStorage = require('./jsonStorage');
const storageService = require('./storageService');
const { encrypt, decrypt } = require('./encryptEllipticCurve');
const readline = require('readline');

const debug = false;

const storageServicePlaintext = storageService.StorageServiceFactory.getStorageService(storageService.StorageType.FILE);

function protect(inputFilepath, outputFilepath, privateKeyFilepath, publicKeyFilepath) {
    if (debug) console.log('Protecting file...');

    const plaintext = storageServicePlaintext.load(inputFilepath);

    const privatekeyEncryptor = keyStorage.loadPrivateKey(privateKeyFilepath);
    const publicKeyDecryptor = keyStorage.loadPublicKey(publicKeyFilepath);

    const ciphertext = encrypt(privatekeyEncryptor, publicKeyDecryptor, plaintext);

    jsonStorage.storeJson(ciphertext, outputFilepath);

    return ciphertext;
}

function check(inputFilepath, privateKeyFilepath, publicKeyFilepath) {
    if (debug) console.log('Checking file...');

    const ciphertext = jsonStorage.loadJson(inputFilepath);

    const privateKeyDecryptor = keyStorage.loadPrivateKey(privateKeyFilepath);
    const publicKeyEncryptor = keyStorage.loadPublicKey(publicKeyFilepath);

    decrypt(privateKeyDecryptor, publicKeyEncryptor, ciphertext);
}

function unprotect(inputFilepath, outputFilepath, privateKeyFilepath, publicKeyFilepath) {
    if (debug) console.log('Unprotecting file...');

    const ciphertext = jsonStorage.loadJson(inputFilepath);

    const privateKeyDecryptor = keyStorage.loadPrivateKey(privateKeyFilepath);
    const publicKeyEncryptor = keyStorage.loadPublicKey(publicKeyFilepath);

    const plaintext = decrypt(privateKeyDecryptor, publicKeyEncryptor, ciphertext);

    storageServicePlaintext.store(plaintext, outputFilepath);

    return plaintext;
}

function generateKeyPair(privateKeyFilepath, publicKeyFilepath) {
    if (debug) console.log('Generating a new key pair...');

    const { privateKey, publicKey } = keyGenerate.generateKeyPair();

    keyStorage.storePrivateKey(privateKey, privateKeyFilepath);
    keyStorage.storePublicKey(publicKey, publicKeyFilepath);
}

function printHelp() {
    console.log('Available functions:');
    console.log('- protect <inputFilepath> <outputFilepath> <privateKeyFilepath> <publicKeyFilepath>');
    console.log('- check <inputFilepath> <privateKeyFilepath> <publicKeyFilepath>');
    console.log('- unprotect <inputFilepath> <outputFilepath> <privateKeyFilepath> <publicKeyFilepath>');
    console.log('- generateKeyPair <privateKeyFilepath> <publicKeyFilepath>');
    console.log('Usage: node crypt_lib.js <function> [arguments]');
}

if (require.main === module) {
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    const args = process.argv.slice(2);
    const functionName = args[0];

    let inputFilepath;
    let outputFilepath;
    let privateKeyFilepath;
    let publicKeyFilepath;

    switch (functionName) {
        case 'protect':
            inputFilepath = args[1];
            outputFilepath = args[2];
            privateKeyFilepath = args[3];
            publicKeyFilepath = args[4];
            
            if (inputFilepath === undefined || outputFilepath === undefined || privateKeyFilepath === undefined || publicKeyFilepath === undefined) {
                console.log('Missing arguments.');
                printHelp();
                break;
            }
            protect(inputFilepath, outputFilepath, privateKeyFilepath, publicKeyFilepath);
            break;
        case 'check':
            inputFilepath = args[1];
            privateKeyFilepath = args[2];
            publicKeyFilepath = args[3];
            
            if (inputFilepath === undefined || privateKeyFilepath === undefined || publicKeyFilepath === undefined) {
                console.log('Missing arguments.');
                printHelp();
                break;
            }
            try {
                check(inputFilepath, privateKeyFilepath, publicKeyFilepath);
                console.log("Document security check passed!")
            } catch (e) {
                console.log("Document security check failed: " + e);
            }
            break;
        case 'unprotect':
            inputFilepath = args[1];
            outputFilepath = args[2];
            privateKeyFilepath = args[3];
            publicKeyFilepath = args[4];
            
            if (inputFilepath === undefined || outputFilepath === undefined || privateKeyFilepath === undefined || publicKeyFilepath === undefined) {
                console.log('Missing arguments.');
                printHelp();
                break;
            }
            unprotect(inputFilepath, outputFilepath, privateKeyFilepath, publicKeyFilepath);
            break;
        case 'generate-key-pair':
            privateKeyFilepath = args[1];
            publicKeyFilepath = args[2];

            if (privateKeyFilepath === undefined || publicKeyFilepath === undefined) {
                console.log('Missing arguments.');
                printHelp();
                break;
            }
            generateKeyPair(privateKeyFilepath, publicKeyFilepath);
            break;
        case 'help':
            printHelp();
            break;
        default:
            console.log('Invalid function name.');
            printHelp();
            break;
    }

    rl.close();
}
