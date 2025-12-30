export const useApi = () => {
  const { $api } = useNuxtApp()
  const config = useRuntimeConfig()
  
  return {
    // Auth
    register: (data: any) => $api('/api/auth/register', { method: 'POST', body: data }),
    login: (data: any) => $api('/api/auth/login', { method: 'POST', body: data }),
    
    // Reports
    getReports: (params?: any) => $api('/api/reports/', { params }),
    getMyReports: () => $api('/api/reports/my-reports'),
    getReport: (id: number) => $api(`/api/reports/${id}`),
    createReport: (formData: FormData) => $api('/api/reports/', { 
      method: 'POST', 
      body: formData 
    }),
    voteReport: (id: number) => $api(`/api/reports/${id}/vote`, { method: 'POST' }),
    unvoteReport: (id: number) => $api(`/api/reports/${id}/vote`, { method: 'DELETE' }),
    
    // Public
    getOrganizations: () => $api('/api/organizations'),
    getCategories: () => $api('/api/categories'),
    
    // Admin
    getAllReports: () => $api('/api/admin/reports'),
    updateReportStatus: (id: number, status: string) => 
      $api(`/api/admin/reports/${id}`, { 
        method: 'PATCH', 
        body: { status } 
      }),
    deleteReport: (id: number) => $api(`/api/admin/reports/${id}`, { method: 'DELETE' }),
    getStats: () => $api('/api/admin/stats'),
    
    // Utils
    getImageUrl: (path: string) => `${config.public.apiBase}/uploads/${path}`,
  }
}
