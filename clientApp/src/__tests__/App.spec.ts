import { describe, it, expect } from 'vitest'

import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App', () => {
  it('renders the storefront content', () => {
    const wrapper = mount(App)
    expect(wrapper.text()).toContain('NovaShop')
    expect(wrapper.text()).toContain('Produtos disponiveis')
    expect(wrapper.text()).toContain('Headphone Aurora X1')
  })
})
