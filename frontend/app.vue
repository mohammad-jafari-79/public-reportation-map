<template>
  <div>
    <NuxtPage />
  </div>
</template>

<script setup>
const authStore = useAuthStore()

onMounted(() => {
  authStore.loadAuth()
})
</script>
