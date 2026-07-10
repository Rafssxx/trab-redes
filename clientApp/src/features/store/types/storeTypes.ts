export type ProductCategory = 'Eletronicos' | 'Casa' | 'Moda' | 'Esporte'

export interface Product {
  id: number
  name: string
  category: ProductCategory
  description: string
  price: number
  rating: number
  stock: number
  imageUrl: string
}

export interface CartLine {
  product: Product
  quantity: number
}

export interface LoginPayload {
  email: string
  password: string
}

export interface CustomerSession {
  name: string
  email: string
}
