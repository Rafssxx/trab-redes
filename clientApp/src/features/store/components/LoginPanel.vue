<script setup lang="ts">
import { reactive } from 'vue'
import type { CustomerSession, LoginPayload } from '../types/storeTypes'

defineProps<{
  isOpen: boolean
  customerSession: CustomerSession | null
  loginError: string
  loginNotice: string
}>()

const emit = defineEmits<{
  close: []
  login: [payload: LoginPayload]
  logout: []
}>()

const formState = reactive<LoginPayload>({
  email: '',
  password: '',
})

function submitLogin() {
  emit('login', {
    email: formState.email,
    password: formState.password,
  })
}
</script>

<template>
  <Teleport to="body">
    <div v-if="isOpen" class="login-shell" role="presentation">
      <button class="login-backdrop" type="button" aria-label="Fechar login" @click="$emit('close')" />

      <section class="login-panel" aria-label="Login do cliente">
        <header class="login-header">
          <div>
            <p>Minha conta</p>
            <h2>{{ customerSession ? 'Cliente conectado' : 'Entrar na loja' }}</h2>
          </div>
          <button type="button" aria-label="Fechar login" @click="$emit('close')">X</button>
        </header>

        <div v-if="customerSession" class="session-box">
          <p>Voce esta conectado como</p>
          <strong>{{ customerSession.name }}</strong>
          <span>{{ customerSession.email }}</span>
          <button type="button" @click="$emit('logout')">Sair</button>
        </div>

        <form v-else class="login-form" @submit.prevent="submitLogin">
          <label>
            <span>E-mail</span>
            <input v-model="formState.email" type="email" autocomplete="email" placeholder="cliente@email.com" />
          </label>

          <label>
            <span>Senha</span>
            <input
              v-model="formState.password"
              type="password"
              autocomplete="current-password"
              placeholder="minimo 4 caracteres"
            />
          </label>

          <p v-if="loginNotice" class="notice-message" role="status">{{ loginNotice }}</p>
          <p v-if="loginError" class="error-message" role="alert">{{ loginError }}</p>

          <button type="submit">Entrar</button>
        </form>
      </section>
    </div>
  </Teleport>
</template>

<style scoped>
.login-shell {
  position: fixed;
  inset: 0;
  z-index: 60;
  display: grid;
  place-items: center;
  padding: 20px;
}

.login-backdrop {
  position: absolute;
  inset: 0;
  border: 0;
  background: rgba(15, 23, 42, 0.44);
  cursor: pointer;
}

.login-panel {
  position: relative;
  z-index: 1;
  width: min(100%, 420px);
  overflow: hidden;
  border-radius: 8px;
  background: #ffffff;
  box-shadow: 0 24px 60px rgba(17, 24, 39, 0.24);
}

.login-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 22px;
  border-bottom: 1px solid #e5e7eb;
}

.login-header p,
.login-header h2,
.session-box p {
  margin: 0;
}

.login-header p {
  color: #d97706;
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
}

.login-header h2 {
  color: #111827;
  font-size: 1.25rem;
}

.login-header button {
  width: 38px;
  height: 38px;
  border: 1px solid #d6dae2;
  border-radius: 8px;
  background: #ffffff;
  color: #111827;
  cursor: pointer;
}

.login-form,
.session-box {
  display: grid;
  gap: 16px;
  padding: 22px;
}

.login-form label {
  display: grid;
  gap: 8px;
}

.login-form span,
.session-box p {
  color: #4b5563;
  font-size: 0.86rem;
  font-weight: 700;
}

.login-form input {
  min-height: 46px;
  border: 1px solid #d6dae2;
  border-radius: 8px;
  padding: 0 14px;
  font: inherit;
}

.notice-message,
.error-message {
  margin: 0;
  border-radius: 8px;
  padding: 10px 12px;
  font-size: 0.9rem;
}

.notice-message {
  background: #eff6ff;
  color: #175cd3;
}

.error-message {
  background: #fef3f2;
  color: #b42318;
}

.login-form button,
.session-box button {
  min-height: 46px;
  border: 0;
  border-radius: 8px;
  background: #14213d;
  color: #ffffff;
  font: inherit;
  font-weight: 800;
  cursor: pointer;
}

.session-box strong {
  color: #111827;
  font-size: 1.1rem;
}

.session-box span {
  color: #5b6475;
}
</style>
