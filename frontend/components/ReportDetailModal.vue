<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[2000] p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold">جزئیات گزارش</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700 text-2xl">
          ×
        </button>
      </div>
      
      <div class="space-y-4">
        <div>
          <h3 class="font-bold text-xl">{{ report.title }}</h3>
          <div class="flex gap-2 mt-2">
            <span 
              class="px-2 py-1 rounded text-sm"
              :class="{
                'bg-yellow-100 text-yellow-800': report.status === 'pending',
                'bg-green-100 text-green-800': report.status === 'approved',
                'bg-red-100 text-red-800': report.status === 'rejected',
              }"
            >
              {{ statusText[report.status] }}
            </span>
          </div>
        </div>
        
        <div>
          <p class="text-gray-700">{{ report.description }}</p>
        </div>
        
        <div v-if="report.address" class="text-sm text-gray-600">
          <i class="fa-solid fa-map-pin"></i> {{ report.address }}
        </div>
        
        <div class="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span class="font-medium">ارگان:</span>
            {{ report.organization.name_fa }}
          </div>
          <div>
            <span class="font-medium">دسته‌بندی:</span>
            {{ report.category.name_fa }}
          </div>
          <div>
            <span class="font-medium">ثبت‌کننده:</span>
            {{ report.user.name }}
          </div>
          <div>
            <span class="font-medium">تاریخ:</span>
            {{ new Date(report.created_at).toLocaleDateString('fa-IR') }}
          </div>
        </div>
        
        <div v-if="report.images && report.images.length > 0" class="space-y-2">
          <h4 class="font-bold">تصاویر:</h4>
          <div class="grid grid-cols-3 gap-2">
            <img
              v-for="image in report.images"
              :key="image.id"
              :src="api.getImageUrl(image.image_path)"
              :alt="report.title"
              class="w-full h-32 object-cover rounded cursor-pointer hover:opacity-75"
              @click="openImage(api.getImageUrl(image.image_path))"
            />
          </div>
        </div>
        
        <div class="flex items-center gap-3 pt-4 border-t">
          <button
            v-if="authStore.isAuthenticated"
            @click="toggleVote"
            :disabled="voteLoading"
            class="flex items-center gap-2 px-4 py-2 rounded transition"
            :class="hasVoted ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'"
          >
            <i :class="hasVoted ? 'fa-solid fa-thumbs-up' : 'fa-regular fa-thumbs-up'"></i> {{ report.votes_count }}
          </button>
          <span v-else class="text-gray-600">
            <i class="fa-regular fa-thumbs-up"></i> {{ report.votes_count }} رای
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  report: Object,
})

const emit = defineEmits(['close', 'voted'])
const api = useApi()
const authStore = useAuthStore()

const voteLoading = ref(false)
const hasVoted = ref(false)

const statusText = {
  pending: 'در انتظار تایید',
  approved: 'تایید شده',
  rejected: 'رد شده',
}

async function toggleVote() {
  voteLoading.value = true
  try {
    let response
    if (hasVoted.value) {
      response = await api.unvoteReport(props.report.id)
      hasVoted.value = false
    } else {
      response = await api.voteReport(props.report.id)
      hasVoted.value = true
    }
    // Update local vote count
    if (response && response.votes_count !== undefined) {
      props.report.votes_count = response.votes_count
    }
    emit('voted')
  } catch (err) {
    console.error('Vote error:', err)
  } finally {
    voteLoading.value = false
  }
}

function openImage(url) {
  window.open(url, '_blank')
}
</script>
