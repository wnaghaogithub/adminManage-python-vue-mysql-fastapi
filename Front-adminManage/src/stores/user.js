import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('admin_token') || '',
    username: localStorage.getItem('admin_username') || '',
  }),
  actions: {
    setLogin(token, username) {
      this.token = token
      this.username = username
      localStorage.setItem('admin_token', token)
      localStorage.setItem('admin_username', username)
    },
    clear() {
      this.token = ''
      this.username = ''
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_username')
    },
  },
})
