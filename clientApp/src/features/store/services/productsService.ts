import type { Product, ProductCategory } from '../types/storeTypes'

interface ApiProduct {
  id: string
  nome: string
  categoria: ProductCategory
  descricao: string | null
  preco: number
  estoque: number
  imagem_url: string | null
  avaliacao: number
}

const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000'

export async function fetchProducts(): Promise<Product[]> {
  const response = await fetch(`${API_BASE_URL}/produtos`)

  if (!response.ok) {
    throw new Error('Nao foi possivel carregar os produtos.')
  }

  const apiProducts = (await response.json()) as ApiProduct[]

  return apiProducts.map(mapApiProductToProduct)
}

function mapApiProductToProduct(apiProduct: ApiProduct): Product {
  return {
    id: apiProduct.id,
    name: apiProduct.nome,
    category: apiProduct.categoria,
    description: apiProduct.descricao ?? '',
    price: apiProduct.preco,
    rating: apiProduct.avaliacao,
    stock: apiProduct.estoque,
    imageUrl: apiProduct.imagem_url ?? '',
  }
}
