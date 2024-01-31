import crypto from 'crypto';
import fs from 'fs';


export function loadPublicKey(filepath: string) {
    const data = fs.readFileSync(filepath);
    return crypto.createPublicKey(data);
}

export function loadPrivateKey(filepath: string) {
  const data = fs.readFileSync(filepath);
  return crypto.createPrivateKey(data);
}

export function sign(privateKey: crypto.KeyObject, data: string): Buffer {
    const sign = crypto.createSign('SHA256');
    sign.update(data);
    return sign.sign(privateKey);
}

export function verify(publicKey: crypto.KeyObject, data: string, signature: Buffer): boolean {
    const verify = crypto.createVerify('SHA256');
    verify.update(data);
    return verify.verify(publicKey, signature);
}


const privateKey = loadPrivateKey('../../copies_of_keys/user_1_private_key.pem');
const publicKey = loadPublicKey('../../copies_of_keys/user_1_public_key.pem');

const data = 'Hello World';

const signature = sign(privateKey, data);

console.log('Signature: ', signature.toString('hex'));

const authenticity = verify(publicKey, data, signature);

console.log('Authenticity: ', authenticity);
