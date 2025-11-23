/**
 * API Service for NeuroSmriti Frontend
 * Handles all communication with the backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3102'

interface ApiResponse<T> {
  data?: T
  error?: string
}

// Token management
export const getToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token')
  }
  return null
}

export const setTokens = (accessToken: string, refreshToken: string) => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', refreshToken)
  }
}

export const clearTokens = () => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }
}

// Generic fetch wrapper
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const token = getToken()

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token) {
    (headers as Record<string, string>)['Authorization'] = `Bearer ${token}`
  }

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      return { error: errorData.detail || `Error: ${response.status}` }
    }

    const data = await response.json()
    return { data }
  } catch (error) {
    console.error('API Error:', error)
    return { error: 'Network error. Please check your connection.' }
  }
}

// Auth API
export const authApi = {
  login: async (email: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}))
        return { error: errorData.detail || 'Login failed' }
      }

      const data = await response.json()
      setTokens(data.access_token, data.refresh_token)
      return { data }
    } catch (error) {
      return { error: 'Network error. Please check your connection.' }
    }
  },

  register: async (userData: {
    email: string
    password: string
    full_name: string
    role: string
  }) => {
    return fetchApi('/api/v1/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
  },

  logout: async () => {
    clearTokens()
    return { data: { message: 'Logged out successfully' } }
  },
}

// Patients API
export const patientsApi = {
  getAll: async () => {
    return fetchApi<Patient[]>('/api/v1/patients/')
  },

  getById: async (id: string) => {
    return fetchApi<Patient>(`/api/v1/patients/${id}`)
  },

  create: async (patientData: PatientCreate) => {
    return fetchApi<Patient>('/api/v1/patients/', {
      method: 'POST',
      body: JSON.stringify(patientData),
    })
  },

  update: async (id: string, patientData: Partial<PatientCreate>) => {
    return fetchApi<Patient>(`/api/v1/patients/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(patientData),
    })
  },

  delete: async (id: string) => {
    return fetchApi(`/api/v1/patients/${id}`, {
      method: 'DELETE',
    })
  },
}

// Memories API
export const memoriesApi = {
  getGraph: async (patientId: string) => {
    return fetchApi<MemoryGraph>(`/api/v1/memories/graph/${patientId}`)
  },

  create: async (memoryData: MemoryCreate) => {
    return fetchApi<Memory>('/api/v1/memories/', {
      method: 'POST',
      body: JSON.stringify(memoryData),
    })
  },

  updateStrength: async (memoryId: string, strength: number) => {
    return fetchApi(`/api/v1/memories/${memoryId}/strength`, {
      method: 'PATCH',
      body: JSON.stringify({ recall_strength: strength }),
    })
  },
}

// Predictions API
export const predictionsApi = {
  predictStage: async (patientId: string, mriFile?: File) => {
    if (mriFile) {
      const formData = new FormData()
      formData.append('mri_scan', mriFile)

      const token = getToken()
      const headers: HeadersInit = {}
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }

      try {
        const response = await fetch(
          `${API_BASE_URL}/api/v1/predictions/stage?patient_id=${patientId}`,
          {
            method: 'POST',
            headers,
            body: formData,
          }
        )
        const data = await response.json()
        return { data }
      } catch (error) {
        return { error: 'Failed to upload scan' }
      }
    }

    return fetchApi(`/api/v1/predictions/stage?patient_id=${patientId}`, {
      method: 'POST',
    })
  },

  predictMemoryDecay: async (patientId: string) => {
    return fetchApi(`/api/v1/predictions/memory-decay/${patientId}`)
  },
}

// Cognitive Tests API
export const cognitiveTestsApi = {
  startTest: async (testType: string, patientId: string) => {
    return fetchApi('/api/v1/cognitive-tests/start', {
      method: 'POST',
      body: JSON.stringify({ test_type: testType, patient_id: patientId }),
    })
  },

  submitAnswer: async (testId: string, questionId: string, answer: string) => {
    return fetchApi(`/api/v1/cognitive-tests/${testId}/answer`, {
      method: 'POST',
      body: JSON.stringify({ question_id: questionId, answer }),
    })
  },

  getResults: async (testId: string) => {
    return fetchApi(`/api/v1/cognitive-tests/${testId}/results`)
  },
}

// Interventions API
export const interventionsApi = {
  getAll: async (patientId: string) => {
    return fetchApi(`/api/v1/interventions/?patient_id=${patientId}`)
  },

  create: async (interventionData: InterventionCreate) => {
    return fetchApi('/api/v1/interventions/', {
      method: 'POST',
      body: JSON.stringify(interventionData),
    })
  },
}

// Types
export interface Patient {
  id: string
  first_name: string
  last_name: string
  date_of_birth: string
  gender: string
  diagnosis_stage: number
  mmse_score: number
  moca_score: number
  created_at: string
  updated_at: string
}

export interface PatientCreate {
  first_name: string
  last_name: string
  date_of_birth: string
  gender: string
  diagnosis_stage?: number
  medical_history?: string
  current_medications?: string[]
  emergency_contact_name?: string
  emergency_contact_phone?: string
}

export interface Memory {
  id: string
  type: string
  name: string
  description: string
  recall_strength: number
  emotional_weight: number
  created_at: string
}

export interface MemoryCreate {
  patient_id: string
  type: string
  name: string
  description: string
  emotional_weight?: number
}

export interface MemoryGraph {
  patient_id: string
  nodes: MemoryNode[]
  edges: MemoryEdge[]
}

export interface MemoryNode {
  id: string
  type: string
  name: string
  recall_strength: number
  emotional_weight: number
  last_accessed: string
}

export interface MemoryEdge {
  source: string
  target: string
  type: string
  strength: number
}

export interface InterventionCreate {
  patient_id: string
  type: string
  content: string
  scheduled_time?: string
}
