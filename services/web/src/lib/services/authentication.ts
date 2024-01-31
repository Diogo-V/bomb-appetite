import { decrypt, checkHashes } from "$lib/services/security";
import type { BackendResponse } from "$lib/types/models";

export function verifyServerResponseAuthenticity(privateKey: string, publicKey: string, response: BackendResponse): boolean {
    // Decrypts the signature
    const hashedData = decrypt(privateKey, publicKey, response.signature);

    // Verifies the signature
    return !checkHashes(JSON.stringify(response.data), hashedData);
}
