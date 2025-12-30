import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as any,
    token: null as string | null,
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin',
  },
  
  actions: {
    setAuth(user: any, token: string) {
      this.user = user
      this.token = token
      if (process.client) {
        localStorage.setItem('token', token)
        localStorage.setItem('user', JSON.stringify(user))
      }
    },
    
    loadAuth() {
      if (process.client) {
        const token = localStorage.getItem('token')
        const user = localStorage.getItem('user')
        if (token && user) {
          this.token = token
          this.user = JSON.parse(user)
        }
      }
    },
    
    logout() {
      this.user = null
      this.token = null
      if (process.client) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
      }
      navigateTo('/login')
    },
  },
})
