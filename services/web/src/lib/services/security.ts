import crypto, { Hash } from 'crypto';
import fs from 'fs';


export function deriveKey(privateKey, publicKey) {

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

export function loadPublicKey(filepath: string) {
    const data = fs.readFileSync(filepath);
    return crypto.createPublicKey(data);
}

export function loadPrivateKey(filepath: string) {
  const data = fs.readFileSync(filepath);
  return crypto.createPrivateKey(data);
}

export function encrypt(privateKeyEncryptor, publicKeyDecryptor, plaintext) {
    const derivedKey = deriveKey(privateKeyEncryptor, publicKeyDecryptor);

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

export function decrypt(privateKeyDecryptor, publicKeyEncryptor, encryptedData) {
    const derivedKey = deriveKey(privateKeyDecryptor, publicKeyEncryptor);

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

export function checkHashes(data: string, signature: string): boolean {
  const hash = crypto.createHash('sha256');

  // Convert data to bytes
  let utf8Encode = new TextEncoder();
  const dataBytes = utf8Encode.encode(data);

  // Hash data
  hash.update(dataBytes);
  const hashedData = hash.digest('hex');

  // Does a safe comparison of the hashed data and the signature
  const signatureBuffer = Buffer.from(signature, 'hex');
  const hashedDataBuffer = Buffer.from(hashedData, 'hex');
  return crypto.timingSafeEqual(hashedDataBuffer, signatureBuffer);
}

export function hash(data: string): string {
  const hash = crypto.createHash('sha256');
  hash.update(data);
  return hash.digest('hex');
}

export function sign(privateKey: crypto.KeyLike, data: string): string {
  const sign = crypto.createSign('SHA256');
  sign.update(data);
  return sign.sign(privateKey, 'hex');
}

export function verify(publicKey: crypto.KeyLike, data: string, signature: string): boolean {
  const verify = crypto.createVerify('SHA256');
  verify.update(data);
  return verify.verify(publicKey, signature, 'hex');
}
