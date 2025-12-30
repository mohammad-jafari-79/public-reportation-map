<template>
  <NuxtLayout>
    <div class="container mx-auto px-4 py-8 max-w-md">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-3xl font-bold text-center mb-6">ورود</h1>
        
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">ایمیل</label>
            <input
              v-model="form.email"
              type="email"
              required
              class="w-full border rounded px-3 py-2"
              placeholder="example@email.com"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">رمز عبور</label>
            <input
              v-model="form.password"
              type="password"
              required
              class="w-full border rounded px-3 py-2"
              placeholder="••••••••"
            />
          </div>
          
          <div v-if="error" class="text-red-600 text-sm">
            {{ error }}
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
          >
            {{ loading ? 'در حال ورود...' : 'ورود' }}
          </button>
        </form>
        
        <p class="text-center mt-4 text-sm">
          حساب کاربری ندارید؟
          <NuxtLink to="/register" class="text-blue-600 hover:underline">
            ثبت‌نام کنید
          </NuxtLink>
        </p>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
const api = useApi()
const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  email: '',
  password: '',
})

const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''
  
  try {
    const response = await api.login(form.value)
    
    // Get user info after login
    const userInfo = await $fetch(`${useRuntimeConfig().public.apiBase}/api/auth/me`, {
      headers: {
        Authorization: `Bearer ${response.access_token}`
      }
    })
    
    authStore.setAuth(userInfo, response.access_token)
    router.push('/')
  } catch (err) {
    error.value = 'ایمیل یا رمز عبور اشتباه است'
  } finally {
    loading.value = false
  }
}
</script>
