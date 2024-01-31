export interface User {
    id: number;
    name: string;
}

export interface MenuItem {
    name: string
    category: string
    description: string
    price: number
    currency: string
}

export interface VoucherData {
    code: string
    discount: number
    description: string
}

export interface Vouchers {
    id: number;
    restaurant_id: number;
    user_id: number;
    data: Signature | VoucherData;
}

export interface Reviews {
    id: number;
    user_id: number;
    restaurant_id: number;
    review: string;
    rating: number;
    signature: string;
}

export interface Restaurant {
    id: string
    owner: string
    restaurant: string
    address: string
    genre: string[]
    menu: MenuItem[]
    user_vouchers: Vouchers[]
    reviews: Reviews[]
}

export interface Signature {
    iv: string
    tag: string
    ciphertext: string
}

export interface BackendResponse<T> {
    data: T
    signature: Signature
}
