<script setup lang="ts">
import type { ProductCategory } from '../types/storeTypes'

defineProps<{
  categories: ProductCategory[]
  selectedCategory: ProductCategory | 'Todos'
  searchTerm: string
}>()

defineEmits<{
  selectCategory: [category: ProductCategory | 'Todos']
  search: [searchTerm: string]
}>()
</script>

<template>
  <section class="filters" aria-label="Filtros de produtos">
    <label class="search-field">
      <span>Buscar produto</span>
      <input
        :value="searchTerm"
        type="search"
        placeholder="Headphone, mochila, tenis..."
        @input="$emit('search', ($event.target as HTMLInputElement).value)"
      />
    </label>

    <div class="category-list" role="list" aria-label="Categorias">
      <button
        class="category-button"
        :class="{ active: selectedCategory === 'Todos' }"
        type="button"
        @click="$emit('selectCategory', 'Todos')"
      >
        Todos
      </button>

      <button
        v-for="category in categories"
        :key="category"
        class="category-button"
        :class="{ active: selectedCategory === category }"
        type="button"
        @click="$emit('selectCategory', category)"
      >
        {{ category }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.filters {
  display: grid;
  grid-template-columns: minmax(260px, 420px) 1fr;
  gap: 18px;
  align-items: end;
}

.search-field {
  display: grid;
  gap: 8px;
}

.search-field span {
  color: #4b5563;
  font-size: 0.86rem;
  font-weight: 700;
}

.search-field input {
  width: 100%;
  min-height: 46px;
  border: 1px solid #d6dae2;
  border-radius: 8px;
  padding: 0 14px;
  background: #ffffff;
  color: #111827;
  font: inherit;
}

.category-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: flex-end;
}

.category-button {
  min-height: 42px;
  border: 1px solid #d6dae2;
  border-radius: 8px;
  padding: 0 14px;
  background: #ffffff;
  color: #1f2937;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.category-button.active {
  border-color: #14213d;
  background: #14213d;
  color: #ffffff;
}

@media (max-width: 760px) {
  .filters {
    grid-template-columns: 1fr;
  }

  .category-list {
    justify-content: flex-start;
  }
}
</style>
