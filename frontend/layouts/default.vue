<template>
  <div class="min-h-screen flex flex-col">
    <header class="bg-blue-700 text-white shadow-lg">
      <div class="container mx-auto px-4 py-4">
        <div class="flex justify-between items-center">
          <NuxtLink to="/" class="text-2xl font-bold">
            نقشه گزارشات شهری مشهد
          </NuxtLink>
          
          <nav class="flex gap-4 items-center">
            <NuxtLink 
              to="/" 
              class="hover:text-blue-200 transition"
            >
              نقشه
            </NuxtLink>
            
            <template v-if="authStore.isAuthenticated">
              <NuxtLink 
                v-if="authStore.isAdmin" 
                to="/admin" 
                class="hover:text-blue-200 transition"
              >
                پنل ادمین
              </NuxtLink>
              
              <button 
                @click="authStore.logout" 
                class="bg-red-500 hover:bg-red-600 px-4 py-2 rounded transition"
              >
                خروج
              </button>
            </template>
            
            <template v-else>
              <NuxtLink 
                to="/login" 
                class="hover:text-blue-200 transition"
              >
                ورود
              </NuxtLink>
              <NuxtLink 
                to="/register" 
                class="bg-green-500 hover:bg-green-600 px-4 py-2 rounded transition"
              >
                ثبت‌نام
              </NuxtLink>
            </template>
          </nav>
        </div>
      </div>
    </header>
    
    <main class="flex-1">
      <slot />
    </main>
    
    <footer class="bg-gray-800 text-white py-6">
      <div class="container mx-auto px-4 text-center">
        <p>© {{ new Date().getFullYear() }} سامانه گزارشات شهری مشهد</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
const authStore = useAuthStore()
</script>
