<template>
  <NuxtLayout>
    <div class="h-[calc(100vh-144px)] relative">
      <!-- Filters -->
      <div class="absolute top-4 right-4 z-[1000] bg-white rounded-lg shadow-lg p-4 max-w-xs">
        <h3 class="font-bold mb-3">فیلترها</h3>
        
        <div class="space-y-3">
          <div>
            <label class="text-sm font-medium block mb-1">ارگان:</label>
            <select 
              v-model="filters.organization_id" 
              class="w-full border rounded px-2 py-1 text-sm"
              @change="loadReports"
            >
              <option :value="null">همه</option>
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
            <label class="text-sm font-medium block mb-1">دسته‌بندی:</label>
            <select 
              v-model="filters.category_id" 
              class="w-full border rounded px-2 py-1 text-sm"
              @change="loadReports"
            >
              <option :value="null">همه</option>
              <option 
                v-for="cat in categories" 
                :key="cat.id" 
                :value="cat.id"
              >
                {{ cat.name_fa }}
              </option>
            </select>
          </div>
          
          <div v-if="authStore.isAuthenticated">
            <label class="text-sm font-medium block mb-1">وضعیت:</label>
            <select 
              v-model="filters.status" 
              class="w-full border rounded px-2 py-1 text-sm"
              @change="loadReports"
            >
              <option value="">همه</option>
              <option value="pending">در انتظار تایید</option>
              <option value="approved">تایید شده</option>
              <option value="rejected">رد شده</option>
            </select>
          </div>
        </div>
        
        <button 
          v-if="authStore.isAuthenticated"
          @click="openReportModalManually"
          class="w-full bg-blue-600 text-white py-2 rounded mt-4 hover:bg-blue-700 transition"
        >
          + ثبت گزارش جدید
        </button>
        <div v-else class="mt-4">
          <p class="text-sm text-gray-600 text-center mb-2">
            برای ثبت گزارش، ابتدا وارد شوید
          </p>
          <div class="flex gap-2">
            <NuxtLink 
              to="/login" 
              class="flex-1 bg-blue-600 text-white py-2 rounded text-center hover:bg-blue-700 transition"
            >
              ورود
            </NuxtLink>
            <NuxtLink 
              to="/register" 
              class="flex-1 bg-green-600 text-white py-2 rounded text-center hover:bg-green-700 transition"
            >
              ثبت‌نام
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <!-- Map -->
      <div id="map" class="h-full w-full"></div>
      
      <!-- Report Modal -->
      <ReportModal 
        v-if="showReportModal"
        :organizations="organizations"
        :categories="categories"
        :initial-lat="clickedLocation.lat"
        :initial-lng="clickedLocation.lng"
        @close="closeReportModal"
        @created="onReportCreated"
      />
      
      <!-- Report Detail Modal -->
      <ReportDetailModal
        v-if="selectedReport"
        :report="selectedReport"
        @close="selectedReport = null"
        @voted="loadReports"
      />
      
      <!-- Login Prompt Modal -->
      <div 
        v-if="showLoginPrompt" 
        class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[2000]"
        @click.self="showLoginPrompt = false"
      >
        <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
          <h3 class="text-xl font-bold mb-4 text-center">برای ثبت گزارش وارد شوید</h3>
          <p class="text-gray-600 text-center mb-6">
            برای ثبت گزارش جدید، ابتدا باید وارد حساب کاربری خود شوید یا ثبت‌نام کنید.
          </p>
          <div class="flex gap-3">
            <NuxtLink 
              to="/login" 
              class="flex-1 bg-blue-600 text-white py-3 rounded text-center hover:bg-blue-700 transition font-medium"
            >
              ورود
            </NuxtLink>
            <NuxtLink 
              to="/register" 
              class="flex-1 bg-green-600 text-white py-3 rounded text-center hover:bg-green-700 transition font-medium"
            >
              ثبت‌نام
            </NuxtLink>
          </div>
          <button 
            @click="showLoginPrompt = false"
            class="w-full mt-3 text-gray-600 hover:text-gray-800 py-2"
          >
            بستن
          </button>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
const api = useApi()
const authStore = useAuthStore()

const map = ref(null)
const reports = ref([])
const organizations = ref([])
const categories = ref([])
const showReportModal = ref(false)
const selectedReport = ref(null)
const markers = ref([])
const clickedLocation = ref({ lat: 36.2974, lng: 59.6059 })
const tempMarker = ref(null)
const showLoginPrompt = ref(false)
let L = null

const filters = ref({
  organization_id: null,
  category_id: null,
  status: '',
})

// Load initial data
onMounted(async () => {
  // Import Leaflet only on client side
  if (process.client) {
    L = (await import('leaflet')).default
  }
  
  await Promise.all([
    loadOrganizations(),
    loadCategories(),
  ])
  initMap()
  await loadReports()
  
  // Check for URL parameters to focus on specific location
  if (process.client) {
    const urlParams = new URLSearchParams(window.location.search)
    const lat = urlParams.get('lat')
    const lng = urlParams.get('lng')
    const zoom = urlParams.get('zoom')
    
    if (lat && lng && map.value) {
      map.value.setView([parseFloat(lat), parseFloat(lng)], zoom ? parseInt(zoom) : 16)
    }
  }
})

async function loadOrganizations() {
  try {
    organizations.value = await api.getOrganizations()
  } catch (error) {
    console.error('Error loading organizations:', error)
  }
}

async function loadCategories() {
  try {
    categories.value = await api.getCategories()
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

async function loadReports() {
  try {
    const params = {}
    if (filters.value.organization_id) params.organization_id = filters.value.organization_id
    if (filters.value.category_id) params.category_id = filters.value.category_id
    if (filters.value.status) params.status = filters.value.status
    
    reports.value = await api.getReports(params)
    updateMarkers()
  } catch (error) {
    console.error('Error loading reports:', error)
  }
}

function initMap() {
  if (!L) return
  
  // Mashhad coordinates
  map.value = L.map('map').setView([36.2974, 59.6059], 12)
  
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: ''
  }).addTo(map.value)
  
  // Add click listener for adding reports
  map.value.on('click', (e) => {
    if (authStore.isAuthenticated) {
      clickedLocation.value = { lat: e.latlng.lat, lng: e.latlng.lng }
      
      // Remove old temp marker
      if (tempMarker.value) {
        tempMarker.value.remove()
      }
      
      // Add new temp marker with custom icon
      const greenIcon = L.icon({
        iconUrl: 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iNDgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgZmlsbD0ibm9uZSIgZmlsbC1ydWxlPSJldmVub2RkIj48cGF0aCBkPSJNMTYgNDhzMTYtMTYgMTYtMjhDMzIgOC45NTQgMjUuMDQ2IDIgMTYgMlMwIDguOTU0IDAgMjBjMCAxMiAxNiAyOCAxNiAyOHoiIGZpbGw9IiMyMmM1NWUiLz48Y2lyY2xlIGZpbGw9IiNmZmYiIGN4PSIxNiIgY3k9IjE2IiByPSI2Ii8+PC9nPjwvc3ZnPg==',
        iconSize: [32, 48],
        iconAnchor: [16, 48],
        popupAnchor: [0, -48]
      })
      
      tempMarker.value = L.marker([e.latlng.lat, e.latlng.lng], { icon: greenIcon })
        .addTo(map.value)
        .bindPopup('موقعیت انتخاب شده - برای ثبت گزارش روی دکمه زیر کلیک کنید')
        .openPopup()
      
      showReportModal.value = true
    } else {
      // Show login prompt for non-authenticated users
      showLoginPrompt.value = true
    }
  })
}

function updateMarkers() {
  if (!L) return
  
  // Clear existing markers
  markers.value.forEach(marker => marker.remove())
  markers.value = []
  
  // Add new markers
  reports.value.forEach(report => {
    const marker = L.marker([report.latitude, report.longitude])
      .addTo(map.value)
      .on('click', () => openReportDetail(report.id))
    
    markers.value.push(marker)
  })
}

async function openReportDetail(reportId) {
  try {
    selectedReport.value = await api.getReport(reportId)
  } catch (error) {
    console.error('Error loading report:', error)
  }
}

function openReportModalManually() {
  clickedLocation.value = { lat: 36.2974, lng: 59.6059 }
  showReportModal.value = true
}

function closeReportModal() {
  showReportModal.value = false
  // Remove temp marker when modal closes
  if (tempMarker.value) {
    tempMarker.value.remove()
    tempMarker.value = null
  }
}

function onReportCreated() {
  showReportModal.value = false
  // Remove temp marker
  if (tempMarker.value) {
    tempMarker.value.remove()
    tempMarker.value = null
  }
  loadReports()
}
</script>
