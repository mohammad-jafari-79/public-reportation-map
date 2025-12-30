<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[2000] p-4" @click.self="$emit('close')">
    <div class="bg-white rounded-lg p-6 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-2xl font-bold">ثبت گزارش جدید</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700 text-2xl">
          ×
        </button>
      </div>
      
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-sm font-medium mb-1">عنوان گزارش *</label>
          <input
            v-model="form.title"
            type="text"
            required
            class="w-full border rounded px-3 py-2"
            placeholder="مثال: چراغ برق خاموش"
          />
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-1">توضیحات *</label>
          <textarea
            v-model="form.description"
            required
            rows="4"
            class="w-full border rounded px-3 py-2"
            placeholder="توضیحات کامل مشکل را بنویسید..."
          ></textarea>
        </div>
        
        <div class="bg-blue-50 p-3 rounded">
          <p class="text-sm text-blue-800">
            <i class="fa-solid fa-map-pin text-blue-600"></i> موقعیت انتخاب شده: {{ form.latitude.toFixed(6) }}, {{ form.longitude.toFixed(6) }}
          </p>
          <p class="text-xs text-blue-600 mt-1">
            برای تغییر موقعیت، روی نقشه کلیک کنید و دوباره فرم را باز کنید
          </p>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-1">آدرس</label>
          <input
            v-model="form.address"
            type="text"
            class="w-full border rounded px-3 py-2"
            placeholder="آدرس دقیق (اختیاری)"
          />
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium mb-1">ارگان مربوطه *</label>
            <select
              v-model="form.organization_id"
              required
              class="w-full border rounded px-3 py-2"
            >
              <option value="">انتخاب کنید</option>
              <option 
                v-for="org in organizations" 
                :key="org.id" 
                :value="org.id"
              >
                {{ org.name_fa }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium mb-1">دسته‌بندی *</label>
            <select
              v-model="form.category_id"
              required
              class="w-full border rounded px-3 py-2"
            >
              <option value="">انتخاب کنید</option>
              <option 
                v-for="cat in categories" 
                :key="cat.id" 
                :value="cat.id"
              >
                {{ cat.name_fa }}
              </option>
            </select>
          </div>
        </div>
        
        <div>
          <label class="block text-sm font-medium mb-1">تصاویر (حداکثر 3 عکس)</label>
          <input
            type="file"
            accept="image/*"
            multiple
            @change="handleFileChange"
            class="w-full border rounded px-3 py-2"
          />
          <p class="text-xs text-gray-500 mt-1">
            عکس‌ها به صورت خودکار فشرده می‌شوند
          </p>
        </div>
        
        <div v-if="error" class="text-red-600 text-sm">
          {{ error }}
        </div>
        
        <div class="flex gap-3">
          <button
            type="submit"
            :disabled="loading"
            class="flex-1 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
          >
            {{ loading ? 'در حال ثبت...' : 'ثبت گزارش' }}
          </button>
          <button
            type="button"
            @click="$emit('close')"
            class="px-6 bg-gray-300 text-gray-700 py-2 rounded hover:bg-gray-400 transition"
          >
            انصراف
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  organizations: Array,
  categories: Array,
  initialLat: Number,
  initialLng: Number,
})

const emit = defineEmits(['close', 'created'])
const api = useApi()

const form = ref({
  title: '',
  description: '',
  latitude: props.initialLat || 36.2974,
  longitude: props.initialLng || 59.6059,
  address: '',
  organization_id: '',
  category_id: '',
})

// Update form when props change
watch(() => [props.initialLat, props.initialLng], ([lat, lng]) => {
  if (lat && lng) {
    form.value.latitude = lat
    form.value.longitude = lng
  }
})

const images = ref([])
const loading = ref(false)
const error = ref('')

function handleFileChange(event) {
  const files = Array.from(event.target.files)
  if (files.length > 3) {
    error.value = 'حداکثر 3 عکس مجاز است'
    event.target.value = ''
    return
  }
  images.value = files
}

async function handleSubmit() {
  loading.value = true
  error.value = ''
  
  try {
    const formData = new FormData()
    formData.append('title', form.value.title)
    formData.append('description', form.value.description)
    formData.append('latitude', form.value.latitude)
    formData.append('longitude', form.value.longitude)
    formData.append('address', form.value.address || '')
    formData.append('organization_id', form.value.organization_id)
    formData.append('category_id', form.value.category_id)
    
    images.value.forEach(image => {
      formData.append('images', image)
    })
    
    await api.createReport(formData)
    emit('created')
  } catch (err) {
    error.value = 'خطا در ثبت گزارش'
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>
