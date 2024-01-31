import type { BackendResponse, MenuItem, Restaurant, Reviews, Vouchers, Signature } from "$lib/types/models";
import { get } from "svelte/store";
import { user } from "$lib/stores/user";
import * as fs from 'fs';
import * as https from 'https';


const BACKEND_HOSTNAME = process.env.BACKEND_HOSTNAME || "backend";
const BACKEND_PORT = process.env.BACKEND_PORT || 8000;
const key = fs.readFileSync("/home/vagrant/client-ssl/client-key.pem");
const cert = fs.readFileSync("/home/vagrant/client-ssl/client-cert.pem");
const ca = fs.readFileSync("/home/vagrant/client-ssl/ca-backend-cert.pem");

export async function getRestaurants(): Promise<BackendResponse<Restaurant[]>> {
    const options = {
        hostname: BACKEND_HOSTNAME,
        port: BACKEND_PORT,
        path: '/v1/restaurants/',
        method: 'GET',
        headers: {
            UserId: get(user).toString()
        },
        key: key,
        cert: cert,
        ca: ca
    };
    return new Promise((resolve: (value: BackendResponse<Restaurant[]>) => void, reject: (reason: Error) => void) => {
        const req = https.request(options, (res: https.IncomingMessage) => {
            res.setEncoding('utf8');
            let responseBody = '';
            res.on('data', (chunk: string) => {
                responseBody += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseBody));
                } catch (error: any) {
                    reject(error);
                }
            });
        });
        req.on('error', (err: Error) => {
            reject(err);
        });
        req.end();
    }) as Promise<BackendResponse<Restaurant[]>>;
}

export async function getRestaurant(id: string): Promise<BackendResponse<Restaurant>> {
    const options = {
        hostname: BACKEND_HOSTNAME,
        port: BACKEND_PORT,
        path: `/v1/restaurants/${id}`,
        method: 'GET',
        headers: {
            UserId: get(user).toString()
        },
        key: key,
        cert: cert,
        ca: ca
    };
    return new Promise((resolve: (value: BackendResponse<Restaurant>) => void, reject: (reason: Error) => void) => {
        const req = https.request(options, (res: https.IncomingMessage) => {
            res.setEncoding('utf8');
            let responseBody = '';
            res.on('data', (chunk: string) => {
                responseBody += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseBody));
                } catch (error: any) {
                    reject(error);
                }
            });
        });
        req.on('error', (err: Error) => {
            reject(err);
        });
        req.end();
    }) as Promise<BackendResponse<Restaurant>>;
}

export async function getRestaurantMenu(id: string): Promise<BackendResponse<MenuItem[]>> {
    const options = {
        hostname: BACKEND_HOSTNAME,
        port: BACKEND_PORT,
        path: `/v1/restaurants/${id}/menu`,
        method: 'GET',
        headers: {
            UserId: get(user).toString()
        },
        key: key,
        cert: cert,
        ca: ca
    };
    return new Promise((resolve: (value: BackendResponse<MenuItem[]>) => void, reject: (reason: Error) => void) => {
        const req = https.request(options, (res: https.IncomingMessage) => {
            res.setEncoding('utf8');
            let responseBody = '';
            res.on('data', (chunk: string) => {
                responseBody += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseBody));
                } catch (error: any) {
                    reject(error);
                }
            });
        });
        req.on('error', (err: Error) => {
            reject(err);
        });
        req.end();
    }) as Promise<BackendResponse<MenuItem[]>>;
}

export async function getVoucher(id: string, code: string): Promise<BackendResponse<Vouchers>> {
    const options = {
        hostname: BACKEND_HOSTNAME,
        port: BACKEND_PORT,
        path: `/v1/vouchers/${id}`,
        method: 'GET',
        headers: {
            UserId: get(user).toString(),
            Code: code
        },
        key: key,
        cert: cert,
        ca: ca
    };
    return new Promise((resolve: (value: BackendResponse<Vouchers>) => void, reject: (reason: Error) => void) => {
        const req = https.request(options, (res: https.IncomingMessage) => {
            res.setEncoding('utf8');
            let responseBody = '';
            res.on('data', (chunk: string) => {
                responseBody += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseBody));
                } catch (error: any) {
                    reject(error);
                }
            });
        });
        req.on('error', (err: Error) => {
            reject(err);
        });
        req.end();
    }) as Promise<BackendResponse<Vouchers>>;
}

export async function useVoucher(code: string, signature: Signature): Promise<BackendResponse<{ is_used?: boolean, can_use_voucher?: boolean }>> {
    const options = {
        hostname: BACKEND_HOSTNAME,
        port: BACKEND_PORT,
        path: `/v1/vouchers/`,
        method: 'PUT',
        headers: {
            UserId: get(user).toString()
        },
        key: key,
        cert: cert,
        ca: ca
    };
    return new Promise((resolve: (value: BackendResponse<{ is_used?: boolean, can_use_voucher?: boolean }>) => void, reject: (reason: Error) => void) => {
        const req = https.request(options, (res: https.IncomingMessage) => {
            res.setEncoding('utf8');
            let responseBody = '';
            res.on('data', (chunk: string) => {
                responseBody += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseBody));
                } catch (error: any) {
                    reject(error);
                }
            });
        });
        req.on('error', (err: Error) => {
            reject(err);
        });
        req.write(JSON.stringify({ code, signature }));
        req.end();
    }) as Promise<BackendResponse<{ is_used?: boolean, can_use_voucher?: boolean }>>;
}

export async function giftVoucher(
    id: string, 
    code: string, 
    newOwner: string, 
    newVoucherDataIv: string,
    newVoucherDataTag: string,
    newVoucherDataCiphertext: string,
    signature: string
): Promise<BackendResponse<{ is_gifted: boolean }>> {
        const options = {
        hostname: BACKEND_HOSTNAME,
        port: BACKEND_PORT,
        path: `/v1/vouchers/${id}`,
        method: 'POST',
        headers: {
            UserId: get(user).toString(),
            "Content-Type": "application/json",
        },
        key: key,
        cert: cert,
        ca: ca
    };
    return new Promise((resolve: (value: BackendResponse<{ is_gifted: boolean }>) => void, reject: (reason: Error) => void) => {
        const req = https.request(options, (res: https.IncomingMessage) => {
            res.setEncoding('utf8');
            let responseBody = '';
            res.on('data', (chunk: string) => {
                responseBody += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseBody));
                } catch (error: any) {
                    reject(error);
                }
            });
        });
        req.on('error', (err: Error) => {
            reject(err);
        });
        req.write(JSON.stringify({ 
            code, 
            newOwner, 
            newVoucherDataIv,
            newVoucherDataTag,
            newVoucherDataCiphertext,
            signature 
        }));
        req.end();
    }) as Promise<BackendResponse<{ is_gifted: boolean }>>;
}

export async function createReview(
    restaurantId: string,
    userId: string, 
    stars: number, 
    comment: string, 
    signature: string
): Promise<BackendResponse<Reviews>> {
    const options = {
        hostname: BACKEND_HOSTNAME,
        port: BACKEND_PORT,
        path: `/v1/reviews/`,
        method: 'POST',
        headers: {
            UserId: get(user).toString(),
            "Content-Type": "application/json",
        },
        key: key,
        cert: cert,
        ca: ca
    };
    return new Promise((resolve: (value: BackendResponse<Reviews>) => void, reject: (reason: Error) => void) => {
        const req = https.request(options, (res: https.IncomingMessage) => {
            res.setEncoding('utf8');
            let responseBody = '';
            res.on('data', (chunk: string) => {
                responseBody += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseBody));
                } catch (error: any) {
                    reject(error);
                }
            });
        });
        req.on('error', (err: Error) => {
            reject(err);
        });
        req.write(JSON.stringify({ 
            restaurantId, 
            userId, 
            stars, 
            comment, 
            signature 
        }));
        req.end();
    }) as Promise<BackendResponse<Reviews>>;
}

export async function getReview(id: string): Promise<BackendResponse<Reviews>> {
    const options = {
        hostname: BACKEND_HOSTNAME,
        port: BACKEND_PORT,
        path: `/v1/reviews/${id}`,
        method: 'GET',
        headers: {
            UserId: get(user).toString()
        },
        key: key,
        cert: cert,
        ca: ca
    };
    return new Promise((resolve: (value: BackendResponse<Reviews>) => void, reject: (reason: Error) => void) => {
        const req = https.request(options, (res: https.IncomingMessage) => {
            res.setEncoding('utf8');
            let responseBody = '';
            res.on('data', (chunk: string) => {
                responseBody += chunk;
            });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(responseBody));
                } catch (error: any) {
                    reject(error);
                }
            });
        });
        req.on('error', (err: Error) => {
            reject(err);
        });
        req.end();
    }) as Promise<BackendResponse<Reviews>>;
}
