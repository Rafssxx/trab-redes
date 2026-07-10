import { ref } from 'vue'
import type { CustomerSession, LoginPayload } from '../types/storeTypes'

export function useCustomerSession() {
  const customerSession = ref<CustomerSession | null>(null)
  const loginError = ref('')

  function login(payload: LoginPayload) {
    const email = payload.email.trim()
    const password = payload.password.trim()

    if (!email || !password) {
      loginError.value = 'Informe e-mail e senha para entrar.'
      return false
    }

    if (!email.includes('@')) {
      loginError.value = 'Informe um e-mail valido.'
      return false
    }

    if (password.length < 4) {
      loginError.value = 'A senha precisa ter pelo menos 4 caracteres.'
      return false
    }

    customerSession.value = {
      email,
      name: email.split('@')[0] || 'Cliente',
    }
    loginError.value = ''
    return true
  }

  function logout() {
    customerSession.value = null
    loginError.value = ''
  }

  return {
    customerSession,
    loginError,
    login,
    logout,
  }
}
