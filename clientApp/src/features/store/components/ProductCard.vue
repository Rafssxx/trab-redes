<script setup lang="ts">
import type { Product } from '../types/storeTypes'

defineProps<{
  product: Product
}>()

defineEmits<{
  addToCart: [product: Product]
}>()

const currencyFormatter = new Intl.NumberFormat('pt-BR', {
  style: 'currency',
  currency: 'BRL',
})
</script>

<template>
  <article class="product-card">
    <img
      v-if="product.imageUrl"
      class="product-image"
      :src="product.imageUrl"
      :alt="product.name"
      loading="lazy"
    />
    <div v-else class="product-image product-image-placeholder" aria-hidden="true">
      {{ product.category }}
    </div>

    <div class="product-content">
      <div>
        <p class="category">{{ product.category }}</p>
        <h3>{{ product.name }}</h3>
        <p class="description">{{ product.description }}</p>
      </div>

      <div class="product-meta">
        <span>{{ product.rating.toFixed(1) }} avaliacao</span>
        <span>{{ product.stock }} em estoque</span>
      </div>

      <div class="buy-row">
        <strong>{{ currencyFormatter.format(product.price) }}</strong>
        <button type="button" @click="$emit('addToCart', product)">Adicionar</button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.product-card {
  display: grid;
  overflow: hidden;
  min-height: 100%;
  border: 1px solid rgba(17, 24, 39, 0.08);
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 14px 36px rgba(20, 33, 61, 0.08);
}

.product-image {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  background: #eef0f4;
}

.product-image-placeholder {
  display: grid;
  place-items: center;
  color: #5b6475;
  font-size: 0.82rem;
  font-weight: 800;
  text-transform: uppercase;
}

.product-content {
  display: grid;
  gap: 18px;
  padding: 18px;
}

.category,
.description {
  margin: 0;
}

.category {
  color: #d97706;
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
}

h3 {
  margin: 6px 0 10px;
  color: #111827;
  font-size: 1.05rem;
  line-height: 1.25;
}

.description {
  color: #5b6475;
  font-size: 0.92rem;
  line-height: 1.5;
}

.product-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  color: #4b5563;
  font-size: 0.82rem;
}

.product-meta span {
  border-radius: 999px;
  padding: 6px 10px;
  background: #f4f6f8;
}

.buy-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.buy-row strong {
  color: #14213d;
  font-size: 1.12rem;
}

.buy-row button {
  min-height: 42px;
  border: 0;
  border-radius: 8px;
  padding: 0 14px;
  background: #14213d;
  color: #ffffff;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}
</style>
