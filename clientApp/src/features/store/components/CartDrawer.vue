<script setup lang="ts">
import type { CartLine } from '../types/storeTypes'

defineProps<{
  isOpen: boolean
  cartLines: CartLine[]
  totalItems: number
  subtotal: number
}>()

defineEmits<{
  close: []
  increase: [productId: string, currentQuantity: number]
  decrease: [productId: string, currentQuantity: number]
  remove: [productId: string]
  checkout: []
}>()

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="drawer-shell" role="presentation">
      <button class="drawer-backdrop" type="button" aria-label="Fechar carrinho" @click="$emit('close')" />

      <aside class="cart-drawer" aria-label="Carrinho de compras">
        <header class="drawer-header">
          <div>
            <p>Carrinho</p>
            <h2>{{ totalItems }} {{ totalItems === 1 ? 'item' : 'itens' }}</h2>
          </div>
          <button class="icon-button" type="button" aria-label="Fechar carrinho" @click="$emit('close')">
            X
          </button>
        </header>

        <div v-if="cartLines.length" class="cart-list">
          <article v-for="cartLine in cartLines" :key="cartLine.product.id" class="cart-line">
            <img
              v-if="cartLine.product.imageUrl"
              :src="cartLine.product.imageUrl"
              :alt="cartLine.product.name"
            />
            <div v-else class="cart-line-image-placeholder" aria-hidden="true"></div>

            <div class="cart-line-content">
              <div>
                <h3>{{ cartLine.product.name }}</h3>
                <p>{{ currencyFormatter.format(cartLine.product.price) }}</p>
              </div>

              <div class="quantity-row">
                <button
                  type="button"
                  aria-label="Diminuir quantidade"
                  @click="$emit('decrease', cartLine.product.id, cartLine.quantity)"
                >
                  -
                </button>
                <span>{{ cartLine.quantity }}</span>
                <button
                  type="button"
                  aria-label="Aumentar quantidade"
                  @click="$emit('increase', cartLine.product.id, cartLine.quantity)"
                >
                  +
                </button>
                <button
                  class="remove-button"
                  type="button"
                  @click="$emit('remove', cartLine.product.id)"
                >
                  Remover
                </button>
              </div>
            </div>
          </article>
        </div>

        <div v-else class="empty-state">
          <h3>Seu carrinho esta vazio</h3>
          <p>Adicione produtos da vitrine para continuar a compra.</p>
        </div>

        <footer class="cart-footer">
          <div class="total-row">
            <span>Subtotal</span>
            <strong>{{ currencyFormatter.format(subtotal) }}</strong>
          </div>
          <button class="checkout-button" type="button" :disabled="!cartLines.length" @click="$emit('checkout')">
            Finalizar compra
          </button>
        </footer>
      </aside>
    </div>
  </Teleport>
</template>

<style scoped>
.drawer-shell {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: grid;
  grid-template-columns: 1fr minmax(320px, 420px);
}

.drawer-backdrop {
  border: 0;
  background: rgba(15, 23, 42, 0.38);
  cursor: pointer;
}

.cart-drawer {
  display: grid;
  grid-template-rows: auto 1fr auto;
  overflow: hidden;
  background: #ffffff;
  box-shadow: -18px 0 48px rgba(17, 24, 39, 0.16);
}

.drawer-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 22px;
  border-bottom: 1px solid #e5e7eb;
}

.drawer-header p,
.drawer-header h2,
.cart-line h3,
.cart-line p,
.empty-state h3,
.empty-state p {
  margin: 0;
}

.drawer-header p {
  color: #d97706;
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
}

.drawer-header h2 {
  color: #111827;
  font-size: 1.25rem;
}

.icon-button {
  width: 38px;
  height: 38px;
  border: 1px solid #d6dae2;
  border-radius: 8px;
  background: #ffffff;
  color: #111827;
  cursor: pointer;
}

.cart-list {
  display: grid;
  align-content: start;
  gap: 14px;
  overflow: auto;
  padding: 18px;
}

.cart-line {
  display: grid;
  grid-template-columns: 84px 1fr;
  gap: 12px;
  border: 1px solid #edf0f3;
  border-radius: 8px;
  padding: 10px;
}

.cart-line img {
  width: 84px;
  height: 84px;
  border-radius: 6px;
  object-fit: cover;
}

.cart-line-image-placeholder {
  width: 84px;
  height: 84px;
  border-radius: 6px;
  background: #eef0f4;
}

.cart-line-content {
  display: grid;
  gap: 12px;
}

.cart-line h3 {
  color: #111827;
  font-size: 0.94rem;
}

.cart-line p {
  color: #5b6475;
  font-size: 0.86rem;
}

.quantity-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.quantity-row button,
.quantity-row span {
  min-width: 32px;
  height: 32px;
  border-radius: 8px;
}

.quantity-row button {
  border: 1px solid #d6dae2;
  background: #ffffff;
  color: #111827;
  cursor: pointer;
}

.quantity-row span {
  display: grid;
  place-items: center;
  background: #f4f6f8;
  color: #111827;
  font-weight: 800;
}

.quantity-row .remove-button {
  width: auto;
  padding: 0 10px;
  color: #b42318;
}

.empty-state {
  display: grid;
  align-content: center;
  gap: 8px;
  padding: 32px;
  text-align: center;
}

.empty-state h3 {
  color: #111827;
}

.empty-state p {
  color: #5b6475;
}

.cart-footer {
  display: grid;
  gap: 14px;
  padding: 20px;
  border-top: 1px solid #e5e7eb;
}

.total-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  color: #111827;
}

.checkout-button {
  min-height: 48px;
  border: 0;
  border-radius: 8px;
  background: #14213d;
  color: #ffffff;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}

.checkout-button:disabled {
  background: #a3aab7;
  cursor: not-allowed;
}

@media (max-width: 620px) {
  .drawer-shell {
    grid-template-columns: 1fr;
  }

  .drawer-backdrop {
    display: none;
  }
}
</style>
