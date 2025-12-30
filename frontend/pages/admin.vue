<template>
  <NuxtLayout>
    <div v-if="!authStore.isAdmin" class="container mx-auto px-4 py-8 text-center">
      <p class="text-red-600 text-xl">دسترسی غیرمجاز</p>
    </div>
    
    <div v-else class="container mx-auto px-4 py-8">
      <h1 class="text-3xl font-bold mb-6">پنل مدیریت</h1>
      
      <!-- Stats -->
      <div v-if="stats" class="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
        <div class="bg-blue-100 p-4 rounded-lg">
          <p class="text-sm text-gray-600">کل گزارشات</p>
          <p class="text-2xl font-bold">{{ stats.total_reports }}</p>
        </div>
        <div class="bg-yellow-100 p-4 rounded-lg">
          <p class="text-sm text-gray-600">در انتظار</p>
          <p class="text-2xl font-bold">{{ stats.pending_reports }}</p>
        </div>
        <div class="bg-green-100 p-4 rounded-lg">
          <p class="text-sm text-gray-600">تایید شده</p>
          <p class="text-2xl font-bold">{{ stats.approved_reports }}</p>
        </div>
        <div class="bg-red-100 p-4 rounded-lg">
          <p class="text-sm text-gray-600">رد شده</p>
          <p class="text-2xl font-bold">{{ stats.rejected_reports }}</p>
        </div>
        <div class="bg-purple-100 p-4 rounded-lg">
          <p class="text-sm text-gray-600">کاربران</p>
          <p class="text-2xl font-bold">{{ stats.total_users }}</p>
        </div>
      </div>
      
      <!-- Reports by Organization -->
      <div v-if="stats" class="bg-white rounded-lg shadow p-6 mb-8">
        <h2 class="text-xl font-bold mb-4">گزارشات به تفکیک ارگان</h2>
        <div class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div 
            v-for="(count, org) in stats.reports_by_organization" 
            :key="org"
            class="border rounded p-3"
          >
            <p class="font-medium">{{ org }}</p>
            <p class="text-2xl text-blue-600">{{ count }}</p>
          </div>
        </div>
      </div>
      
      <!-- Reports Table -->
      <div class="bg-white rounded-lg shadow">
        <div class="p-6 border-b">
          <h2 class="text-xl font-bold">لیست گزارشات</h2>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead class="bg-gray-50">
              <tr>
                <th class="px-4 py-3 text-right text-sm font-medium">شناسه</th>
                <th class="px-4 py-3 text-right text-sm font-medium">عنوان</th>
                <th class="px-4 py-3 text-right text-sm font-medium">ارگان</th>
                <th class="px-4 py-3 text-right text-sm font-medium">دسته‌بندی</th>
                <th class="px-4 py-3 text-right text-sm font-medium">کاربر</th>
                <th class="px-4 py-3 text-right text-sm font-medium">رای</th>
                <th class="px-4 py-3 text-right text-sm font-medium">وضعیت</th>
                <th class="px-4 py-3 text-right text-sm font-medium">نقشه</th>
                <th class="px-4 py-3 text-right text-sm font-medium">عملیات</th>
              </tr>
            </thead>
            <tbody class="divide-y">
              <tr v-for="report in reports" :key="report.id" class="hover:bg-gray-50">
                <td class="px-4 py-3 text-sm">{{ report.id }}</td>
                <td class="px-4 py-3 text-sm">{{ report.title }}</td>
                <td class="px-4 py-3 text-sm">{{ report.organization.name_fa }}</td>
                <td class="px-4 py-3 text-sm">{{ report.category.name_fa }}</td>
                <td class="px-4 py-3 text-sm">{{ report.user.name }}</td>
                <td class="px-4 py-3 text-sm">{{ report.votes_count }}</td>
                <td class="px-4 py-3 text-sm">
                  <span 
                    class="px-2 py-1 rounded text-xs"
                    :class="{
                      'bg-yellow-100 text-yellow-800': report.status === 'pending',
                      'bg-green-100 text-green-800': report.status === 'approved',
                      'bg-red-100 text-red-800': report.status === 'rejected',
                    }"
                  >
                    {{ statusText[report.status] }}
                  </span>
                </td>
                <td class="px-4 py-3 text-sm">
                  <a 
                    :href="`/?lat=${report.latitude}&lng=${report.longitude}&zoom=16`"
                    target="_blank"
                    class="text-blue-600 hover:text-blue-800 text-lg"
                    title="نمایش روی نقشه"
                  >
                    <i class="fa-solid fa-map-pin"></i>
                  </a>
                </td>
                <td class="px-4 py-3 text-sm">
                  <div class="flex gap-2">
                    <button
                      v-if="report.status !== 'approved'"
                      @click="updateStatus(report.id, 'approved')"
                      class="text-green-600 hover:text-green-800"
                      title="تایید"
                    >
                      <i class="fa-solid fa-check"></i>
                    </button>
                    <button
                      v-if="report.status !== 'rejected'"
                      @click="updateStatus(report.id, 'rejected')"
                      class="text-red-600 hover:text-red-800"
                      title="رد"
                    >
                      <i class="fa-solid fa-xmark"></i>
                    </button>
                    <button
                      @click="deleteReport(report.id)"
                      class="text-gray-600 hover:text-gray-800"
                      title="حذف"
                    >
                      <i class="fa-solid fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </NuxtLayout>
</template>

<script setup>
const api = useApi()
const authStore = useAuthStore()

const reports = ref([])
const stats = ref(null)

const statusText = {
  pending: 'در انتظار',
  approved: 'تایید شده',
  rejected: 'رد شده',
}

onMounted(async () => {
  if (authStore.isAdmin) {
    await loadData()
  }
})

async function loadData() {
  try {
    const [reportsData, statsData] = await Promise.all([
      api.getAllReports(),
      api.getStats(),
    ])
    reports.value = reportsData
    stats.value = statsData
  } catch (error) {
    console.error('Error loading admin data:', error)
  }
}

async function updateStatus(reportId, status) {
  try {
    await api.updateReportStatus(reportId, status)
    await loadData()
  } catch (error) {
    console.error('Error updating status:', error)
    alert('خطا در به‌روزرسانی وضعیت')
  }
}

async function deleteReport(reportId) {
  if (!confirm('آیا از حذف این گزارش مطمئن هستید؟')) {
    return
  }
  
  try {
    await api.deleteReport(reportId)
    await loadData()
  } catch (error) {
    console.error('Error deleting report:', error)
    alert('خطا در حذف گزارش')
  }
}
</script>
