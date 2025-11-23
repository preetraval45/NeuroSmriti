/**
 * TypeScript type definitions
 */

export interface User {
  id: string
  email: string
  full_name?: string
  role: 'admin' | 'caregiver' | 'doctor' | 'researcher'
  is_active: boolean
  is_verified: boolean
  created_at: string
  last_login?: string
}

export interface Patient {
  id: string
  full_name: string
  date_of_birth: string
  gender?: string
  current_stage?: number
  diagnosis_date?: string
  mmse_score?: number
  moca_score?: number
  cdr_score?: number
  notes?: string
  created_at: string
  updated_at: string
}

export interface Memory {
  id: string
  type: 'person' | 'place' | 'event' | 'skill' | 'routine' | 'object'
  name: string
  description?: string
  recall_strength: number
  emotional_weight: number
  importance: number
  last_accessed: string
  high_risk: boolean
}

export interface MemoryConnection {
  source: string
  target: string
  type: 'family' | 'friend' | 'associated_with' | 'located_at' | 'temporal' | 'emotional'
  strength: number
}

export interface MemoryGraph {
  nodes: Memory[]
  edges: MemoryConnection[]
}

export interface Prediction {
  patient_id: string
  predicted_stage: number
  confidence: number
  stage_probabilities: Record<string, number>
  progression_risk: 'low' | 'medium' | 'high'
  estimated_progression_months?: number
  top_contributing_factors: string[]
  created_at: string
}

export interface MemoryDecayPrediction {
  memory_id: string
  name: string
  type: string
  decay_probability: number
  days_until_critical: number
  intervention_recommended: boolean
}

export interface Intervention {
  id: string
  type: 'spaced_repetition' | 'contextual_anchoring' | 'multimedia_reinforcement' | 'emotional_preservation' | 'routine_reminder' | 'navigation_assist'
  title: string
  description?: string
  scheduled_for: string
  status: 'scheduled' | 'delivered' | 'completed' | 'skipped' | 'failed'
}
