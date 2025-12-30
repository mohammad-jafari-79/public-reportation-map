<template>
  <NuxtLayout>
    <div class="container mx-auto px-4 py-8 max-w-md">
      <div class="bg-white rounded-lg shadow-lg p-8">
        <h1 class="text-3xl font-bold text-center mb-6">ثبت‌نام</h1>
        
        <form @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="block text-sm font-medium mb-1">نام</label>
            <input
              v-model="form.name"
              type="text"
              required
              class="w-full border rounded px-3 py-2"
              placeholder="نام و نام خانوادگی"
            />
          </div>
          
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
            <label class="block text-sm font-medium mb-1">
              شماره تماس (اختیاری)
            </label>
            <input
              v-model="form.phone"
              type="tel"
              class="w-full border rounded px-3 py-2"
              placeholder="09123456789"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">رمز عبور</label>
            <input
              v-model="form.password"
              type="password"
              required
              minlength="6"
              class="w-full border rounded px-3 py-2"
              placeholder="حداقل ۶ کاراکتر"
            />
          </div>
          
          <div v-if="error" class="text-red-600 text-sm">
            {{ error }}
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 transition disabled:opacity-50"
          >
            {{ loading ? 'در حال ثبت‌نام...' : 'ثبت‌نام' }}
          </button>
        </form>
        
        <p class="text-center mt-4 text-sm">
          حساب کاربری دارید؟
          <NuxtLink to="/login" class="text-blue-600 hover:underline">
            وارد شوید
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
  name: '',
  email: '',
  phone: '',
  password: '',
})

const loading = ref(false)
const error = ref('')

async function handleRegister() {
  loading.value = true
  error.value = ''
  
  try {
    const user = await api.register(form.value)
    // Auto login after registration
    const loginResponse = await api.login({
      email: form.value.email,
      password: form.value.password,
    })
    authStore.setAuth(user, loginResponse.access_token)
    router.push('/')
  } catch (err) {
    error.value = err.data?.detail || 'خطا در ثبت‌نام'
  } finally {
    loading.value = false
  }
}
</script>
