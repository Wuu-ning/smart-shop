import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem('cart') || '[]'))

  function save() {
    localStorage.setItem('cart', JSON.stringify(items.value))
  }

  const totalCount = computed(() => items.value.reduce((s, i) => s + i.quantity, 0))
  const totalPrice = computed(() => items.value.reduce((s, i) => s + i.price * i.quantity, 0))

  function addItem(product) {
    const existing = items.value.find(i => i.id === product.id)
    if (existing) {
      existing.quantity++
    } else {
      items.value.push({
        id: product.id,
        name: product.name,
        price: product.price,
        image_url: product.image_url,
        quantity: 1,
      })
    }
    save()
  }

  function updateQuantity(productId, qty) {
    const item = items.value.find(i => i.id === productId)
    if (item) {
      item.quantity = Math.max(1, qty)
      save()
    }
  }

  function removeItem(productId) {
    items.value = items.value.filter(i => i.id !== productId)
    save()
  }

  function clear() {
    items.value = []
    save()
  }

  return { items, totalCount, totalPrice, addItem, updateQuantity, removeItem, clear }
})
