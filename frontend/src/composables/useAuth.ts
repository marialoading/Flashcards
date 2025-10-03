import { useRouter } from 'vue-router'

export function useAuth() {
  const router = useRouter()
  
  const getToken = () => localStorage.getItem('token') || ''
  
  const handleAuthError = () => {
    localStorage.removeItem('token')
    router.push('/login')
  }
  
  const getApiHeaders = () => ({
    Authorization: `Bearer ${getToken()}`
  })
  
  const getApiBase = () => 
    (import.meta.env.VITE_API_BASE as string) || 'http://localhost:5000/api'
  

  const apiCall = async (endpoint: string, options: RequestInit = {}) => {
    try {
      const res = await fetch(`${getApiBase()}${endpoint}`, {
        headers: {
          'Content-Type': 'application/json',
          ...getApiHeaders(),
          ...options.headers
        },
        ...options
      })
      
      if (res.status === 401) {
        handleAuthError()
        return { error: 'Unauthorized', status: 401 }
      }
      
      if (!res.ok) {
        return { error: 'Request failed', status: res.status }
      }
      
      const data = await res.json()
      return { data, status: res.status }
    } catch (e) {
      return { error: 'Network error', status: 0 }
    }
  }
  
  return {
    router,
    getToken,
    handleAuthError,
    getApiHeaders,
    getApiBase,
    apiCall
  }
}
