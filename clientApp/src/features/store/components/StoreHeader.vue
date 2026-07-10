<script setup lang="ts">
import type { CustomerSession } from '../types/storeTypes'

defineProps<{
  totalCartItems: number
  customerSession: CustomerSession | null
}>()

defineEmits<{
  openCart: []
  openLogin: []
}>()
</script>

<template>
  <header class="store-header">
    <a class="brand" href="#catalogo" aria-label="Ir para o catalogo da NovaShop">
      <span class="brand-mark">N</span>
      <span>
        <strong>NovaShop</strong>
        <small>loja virtual</small>
      </span>
    </a>

    <nav class="header-actions" aria-label="Acoes da loja">
      <button class="text-button" type="button" @click="$emit('openLogin')">
        {{ customerSession ? customerSession.name : 'Entrar' }}
      </button>

      <button class="cart-button" type="button" @click="$emit('openCart')">
        Carrinho
        <span class="cart-count" aria-label="Itens no carrinho">{{ totalCartItems }}</span>
      </button>
    </nav>
  </header>
</template>

<style scoped>
.store-header {
  position: sticky;
  top: 0;
  z-index: 20;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 18px clamp(18px, 5vw, 72px);
  border-bottom: 1px solid rgba(17, 24, 39, 0.08);
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(16px);
}

.brand {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  color: #14213d;
  text-decoration: none;
}

.brand-mark {
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border-radius: 8px;
  background: #14213d;
  color: #ffffff;
  font-weight: 800;
}

.brand strong,
.brand small {
  display: block;
}

.brand strong {
  font-size: 1.08rem;
  line-height: 1.1;
}

.brand small {
  color: #5b6475;
  font-size: 0.78rem;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.text-button,
.cart-button {
  min-height: 42px;
  border: 0;
  border-radius: 8px;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.text-button {
  padding: 0 14px;
  background: transparent;
  color: #1f2937;
}

.cart-button {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 0 16px;
  background: #fca311;
  color: #111827;
}

.cart-count {
  display: grid;
  min-width: 24px;
  height: 24px;
  place-items: center;
  border-radius: 999px;
  background: #111827;
  color: #ffffff;
  font-size: 0.78rem;
}

@media (max-width: 560px) {
  .store-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .text-button,
  .cart-button {
    flex: 1;
    justify-content: center;
  }
}
</style>
