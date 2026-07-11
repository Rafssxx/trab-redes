import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

import { flushPromises, mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: () =>
          Promise.resolve([
            {
              id: 'headphone-aurora-x1',
              nome: 'Headphone Aurora X1',
              categoria: 'Eletronicos',
              descricao: 'Cancelamento de ruido, bateria de longa duracao e conexao multiponto.',
              preco: 429.9,
              estoque: 18,
              imagem_url:
                'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80',
              avaliacao: 4.8,
            },
          ]),
      }),
    )
  })

  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('renders the storefront content', async () => {
    const wrapper = mount(App)

    await flushPromises()

    expect(wrapper.text()).toContain('NovaShop')
    expect(wrapper.text()).toContain('Produtos disponiveis')
    expect(wrapper.text()).toContain('Headphone Aurora X1')
  })
})
