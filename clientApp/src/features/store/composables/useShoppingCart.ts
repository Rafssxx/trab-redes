import { computed, ref } from 'vue'
import type { CartLine, Product } from '../types/storeTypes'

export function useShoppingCart() {
  const cartLines = ref<CartLine[]>([])

  const totalItems = computed(() =>
    cartLines.value.reduce((quantitySum, cartLine) => quantitySum + cartLine.quantity, 0),
  )

  const subtotal = computed(() =>
    cartLines.value.reduce(
      (priceSum, cartLine) => priceSum + cartLine.product.price * cartLine.quantity,
      0,
    ),
  )

  function addProduct(product: Product) {
    const existingCartLine = cartLines.value.find((cartLine) => cartLine.product.id === product.id)

    if (existingCartLine) {
      existingCartLine.quantity += 1
      return
    }

    cartLines.value.push({ product, quantity: 1 })
  }

  function updateQuantity(productId: number, nextQuantity: number) {
    if (nextQuantity <= 0) {
      removeProduct(productId)
      return
    }

    const cartLine = cartLines.value.find((line) => line.product.id === productId)

    if (!cartLine) {
      return
    }

    cartLine.quantity = nextQuantity
  }

  function removeProduct(productId: number) {
    cartLines.value = cartLines.value.filter((cartLine) => cartLine.product.id !== productId)
  }

  function clearCart() {
    cartLines.value = []
  }

  return {
    cartLines,
    totalItems,
    subtotal,
    addProduct,
    updateQuantity,
    removeProduct,
    clearCart,
  }
}
