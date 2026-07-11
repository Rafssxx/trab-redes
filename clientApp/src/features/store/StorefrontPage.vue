<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import CartDrawer from './components/CartDrawer.vue'
import LoginPanel from './components/LoginPanel.vue'
import ProductCard from './components/ProductCard.vue'
import ProductFilters from './components/ProductFilters.vue'
import StoreHeader from './components/StoreHeader.vue'
import { useCustomerSession } from './composables/useCustomerSession'
import { useShoppingCart } from './composables/useShoppingCart'
import { fetchProducts } from './services/productsService'
import type { LoginPayload, Product, ProductCategory } from './types/storeTypes'

const selectedCategory = ref<ProductCategory | 'Todos'>('Todos')
const searchTerm = ref('')
const isCartOpen = ref(false)
const isLoginOpen = ref(false)
const checkoutFeedback = ref('')
const loginNotice = ref('')
const products = ref<Product[]>([])
const isLoadingProducts = ref(true)
const productsError = ref('')

const {
  cartLines,
  totalItems,
  subtotal,
  addProduct,
  updateQuantity,
  removeProduct,
  clearCart,
} = useShoppingCart()

const { customerSession, loginError, login, logout } = useCustomerSession()

const categories = computed<ProductCategory[]>(() => {
  return Array.from(new Set(products.value.map((product) => product.category)))
})

const filteredProducts = computed(() => {
  const normalizedSearchTerm = searchTerm.value.trim().toLowerCase()

  return products.value.filter((product) => {
    const matchesCategory =
      selectedCategory.value === 'Todos' || product.category === selectedCategory.value

    const matchesSearch =
      !normalizedSearchTerm ||
      product.name.toLowerCase().includes(normalizedSearchTerm) ||
      product.description.toLowerCase().includes(normalizedSearchTerm)

    return matchesCategory && matchesSearch
  })
})

const featuredProduct = computed(() => {
  return products.value.find((product) => product.id === 'smartwatch-core-fit') ?? products.value[0]
})

onMounted(loadProducts)

async function loadProducts() {
  isLoadingProducts.value = true
  productsError.value = ''

  try {
    products.value = await fetchProducts()
  } catch {
    productsError.value = 'Nao foi possivel carregar os produtos. Verifique se a API esta rodando.'
  } finally {
    isLoadingProducts.value = false
  }
}

function addProductToCart(productId: string) {
  const product = products.value.find((availableProduct) => availableProduct.id === productId)

  if (!product) {
    return
  }

  addProduct(product)
  isCartOpen.value = true
  checkoutFeedback.value = ''
  loginNotice.value = ''
}

function increaseProductQuantity(productId: string, currentQuantity: number) {
  updateQuantity(productId, currentQuantity + 1)
}

function decreaseProductQuantity(productId: string, currentQuantity: number) {
  updateQuantity(productId, currentQuantity - 1)
}

function submitLogin(payload: LoginPayload) {
  const isLoggedIn = login(payload)

  if (isLoggedIn) {
    isLoginOpen.value = false
    loginNotice.value = ''
  }
}

function checkout() {
  if (!customerSession.value) {
    isCartOpen.value = false
    isLoginOpen.value = true
    loginNotice.value = 'Entre na sua conta para finalizar a compra.'
    return
  }

  clearCart()
  isCartOpen.value = false
  checkoutFeedback.value = 'Pedido recebido. Enviamos os detalhes para o seu e-mail.'
}

function openLoginPanel() {
  loginNotice.value = ''
  isLoginOpen.value = true
}

function closeLoginPanel() {
  loginNotice.value = ''
  isLoginOpen.value = false
}
</script>

<template>
  <div class="store-page">
    <StoreHeader
      :total-cart-items="totalItems"
      :customer-session="customerSession"
      @open-cart="isCartOpen = true"
      @open-login="openLoginPanel"
    />

    <main>
      <section class="hero-section" aria-labelledby="store-title">
        <div class="hero-content">
          <p class="eyebrow">colecao selecionada</p>
          <h1 id="store-title">Produtos para uma rotina mais simples</h1>
          <p class="hero-copy">
            Explore itens de tecnologia, casa, moda e esporte com compra rapida e carrinho
            integrado.
          </p>
          <a href="#catalogo">Ver produtos</a>
        </div>

        <div v-if="featuredProduct" class="hero-showcase" aria-label="Produto em destaque">
          <img
            :src="featuredProduct.imageUrl"
            :alt="`${featuredProduct.name} em destaque`"
          />
          <div class="showcase-price">
            <span>Destaque</span>
            <strong>{{ featuredProduct.name }}</strong>
          </div>
        </div>
      </section>

      <section id="catalogo" class="catalog-section" aria-labelledby="catalog-title">
        <div class="section-heading">
          <div>
            <p class="eyebrow">catalogo</p>
            <h2 id="catalog-title">Produtos disponiveis</h2>
          </div>
          <p>{{ filteredProducts.length }} produtos encontrados</p>
        </div>

        <ProductFilters
          :categories="categories"
          :selected-category="selectedCategory"
          :search-term="searchTerm"
          @select-category="selectedCategory = $event"
          @search="searchTerm = $event"
        />

        <p v-if="checkoutFeedback" class="feedback-message" role="status">{{ checkoutFeedback }}</p>
        <p v-if="productsError" class="error-message" role="alert">{{ productsError }}</p>
        <p v-else-if="isLoadingProducts" class="loading-message" role="status">
          Carregando produtos...
        </p>

        <div v-if="filteredProducts.length" class="product-grid">
          <ProductCard
            v-for="product in filteredProducts"
            :key="product.id"
            :product="product"
            @add-to-cart="addProductToCart($event.id)"
          />
        </div>

        <div v-else-if="!isLoadingProducts && !productsError" class="empty-products">
          <h3>Nenhum produto encontrado</h3>
          <p>Ajuste a busca ou escolha outra categoria.</p>
        </div>
      </section>
    </main>

    <CartDrawer
      :is-open="isCartOpen"
      :cart-lines="cartLines"
      :total-items="totalItems"
      :subtotal="subtotal"
      @close="isCartOpen = false"
      @increase="increaseProductQuantity"
      @decrease="decreaseProductQuantity"
      @remove="removeProduct"
      @checkout="checkout"
    />

    <LoginPanel
      :is-open="isLoginOpen"
      :customer-session="customerSession"
      :login-error="loginError"
      :login-notice="loginNotice"
      @close="closeLoginPanel"
      @login="submitLogin"
      @logout="logout"
    />
  </div>
</template>

<style scoped>
.store-page {
  min-height: 100vh;
  background: #f7f8fb;
  color: #111827;
}

main {
  display: grid;
  gap: 42px;
  padding-bottom: 56px;
}

.hero-section {
  display: grid;
  grid-template-columns: minmax(0, 0.92fr) minmax(320px, 1.08fr);
  gap: clamp(24px, 5vw, 64px);
  align-items: center;
  padding: clamp(32px, 6vw, 72px) clamp(18px, 5vw, 72px) 28px;
}

.hero-content {
  display: grid;
  gap: 18px;
  align-content: center;
}

.eyebrow,
.hero-copy,
.section-heading p,
.empty-products p,
.loading-message,
.error-message {
  margin: 0;
}

.eyebrow {
  color: #d97706;
  font-size: 0.78rem;
  font-weight: 900;
  text-transform: uppercase;
}

h1,
h2,
h3 {
  margin: 0;
  color: #111827;
}

h1 {
  max-width: 760px;
  font-size: clamp(2.2rem, 5vw, 4.7rem);
  line-height: 0.96;
}

.hero-copy {
  max-width: 560px;
  color: #4b5563;
  font-size: 1.08rem;
  line-height: 1.65;
}

.hero-content a {
  display: inline-grid;
  width: fit-content;
  min-height: 48px;
  place-items: center;
  border-radius: 8px;
  padding: 0 18px;
  background: #14213d;
  color: #ffffff;
  font-weight: 800;
  text-decoration: none;
}

.hero-showcase {
  position: relative;
  overflow: hidden;
  min-height: 360px;
  border-radius: 8px;
  box-shadow: 0 28px 70px rgba(20, 33, 61, 0.18);
}

.hero-showcase img {
  width: 100%;
  height: 100%;
  min-height: 360px;
  object-fit: cover;
}

.showcase-price {
  position: absolute;
  right: 18px;
  bottom: 18px;
  display: grid;
  gap: 4px;
  max-width: min(270px, calc(100% - 36px));
  border-radius: 8px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 14px 36px rgba(17, 24, 39, 0.16);
}

.showcase-price span {
  color: #d97706;
  font-size: 0.76rem;
  font-weight: 900;
  text-transform: uppercase;
}

.showcase-price strong {
  color: #111827;
}

.catalog-section {
  display: grid;
  gap: 24px;
  padding: 0 clamp(18px, 5vw, 72px);
}

.section-heading {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 18px;
}

.section-heading h2 {
  margin-top: 6px;
  font-size: clamp(1.8rem, 3vw, 2.5rem);
}

.section-heading > p {
  color: #5b6475;
  font-weight: 700;
}

.feedback-message {
  margin: 0;
  border-radius: 8px;
  padding: 12px 14px;
  background: #ecfdf3;
  color: #027a48;
  font-weight: 700;
}

.loading-message,
.error-message {
  border-radius: 8px;
  padding: 12px 14px;
  font-weight: 700;
}

.loading-message {
  background: #eef4ff;
  color: #1d4ed8;
}

.error-message {
  background: #fef2f2;
  color: #b91c1c;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 22px;
}

.empty-products {
  display: grid;
  gap: 8px;
  border: 1px dashed #c6ccd6;
  border-radius: 8px;
  padding: 32px;
  background: #ffffff;
  text-align: center;
}

.empty-products p {
  color: #5b6475;
}

@media (max-width: 860px) {
  .hero-section {
    grid-template-columns: 1fr;
  }

  h1 {
    line-height: 1.02;
  }
}

@media (max-width: 620px) {
  .section-heading {
    align-items: flex-start;
    flex-direction: column;
  }

  .hero-showcase,
  .hero-showcase img {
    min-height: 280px;
  }
}
</style>
