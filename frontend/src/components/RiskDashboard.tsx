"use client"

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { AlertTriangle, TrendingUp, Brain, Clock, Target, Activity } from 'lucide-react'
import { Progress } from '@/components/ui/progress'

interface HighRiskMemory {
  memory_id: string
  name: string
  type: string
  decay_probability: number
  days_until_critical: number
  intervention_recommended: boolean
}

interface PredictionData {
  predicted_stage?: number
  stage_name?: string
  confidence?: number
  progression_risk?: string
  estimated_progression_months?: number | null
  high_risk_memories?: HighRiskMemory[]
  total_memories?: number
  at_risk_count?: number
  intervention_recommended_count?: number
}

interface RiskDashboardProps {
  predictions: PredictionData
  patientName?: string
}

export default function RiskDashboard({ predictions, patientName }: RiskDashboardProps) {
  const highRiskMemories = predictions?.high_risk_memories || []
  const totalMemories = predictions?.total_memories || 0
  const atRiskCount = predictions?.at_risk_count || 0
  const interventionsNeeded = predictions?.intervention_recommended_count || 0

  // Calculate memory preservation rate
  const preservationRate = totalMemories > 0
    ? ((totalMemories - atRiskCount) / totalMemories) * 100
    : 100

  // Get risk level color
  const getRiskColor = (risk?: string) => {
    switch (risk?.toLowerCase()) {
      case 'high': return 'text-red-600 bg-red-50'
      case 'medium': return 'text-orange-600 bg-orange-50'
      case 'low': return 'text-yellow-600 bg-yellow-50'
      case 'very_low': return 'text-green-600 bg-green-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  // Get stage description
  const getStageDescription = (stage?: number) => {
    const stages: Record<number, string> = {
      0: 'Normal',
      1: 'Mild Cognitive Impairment (MCI)',
      2: 'Mild Alzheimer\'s',
      3: 'Mild-Moderate Alzheimer\'s',
      4: 'Moderate Alzheimer\'s',
      5: 'Moderate-Severe Alzheimer\'s',
      6: 'Severe Alzheimer\'s',
      7: 'Very Severe Alzheimer\'s'
    }
    return stage !== undefined ? stages[stage] : 'Unknown'
  }

  return (
    <div className="space-y-6">
      {/* Patient Header */}
      {patientName && (
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold mb-2">{patientName}</h2>
          <p className="text-blue-100">Cognitive Health Dashboard</p>
        </div>
      )}

      {/* Main Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {/* Current Stage */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Current Stage</CardTitle>
            <Brain className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {predictions?.predicted_stage !== undefined ? `Stage ${predictions.predicted_stage}` : 'N/A'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">
              {getStageDescription(predictions?.predicted_stage)}
            </p>
            {predictions?.confidence && (
              <div className="mt-2">
                <div className="flex justify-between text-xs text-gray-600 mb-1">
                  <span>Confidence</span>
                  <span>{(predictions.confidence * 100).toFixed(0)}%</span>
                </div>
                <Progress value={predictions.confidence * 100} className="h-1" />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Total Memories */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Memories</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalMemories}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Tracked memories
            </p>
            {totalMemories > 0 && (
              <div className="mt-2">
                <div className="flex justify-between text-xs text-gray-600 mb-1">
                  <span>Preservation Rate</span>
                  <span>{preservationRate.toFixed(0)}%</span>
                </div>
                <Progress value={preservationRate} className="h-1" />
              </div>
            )}
          </CardContent>
        </Card>

        {/* At Risk Memories */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">At Risk</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">{atRiskCount}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Memories showing decline
            </p>
            {totalMemories > 0 && (
              <p className="text-xs text-orange-600 mt-2 font-medium">
                {((atRiskCount / totalMemories) * 100).toFixed(1)}% of total
              </p>
            )}
          </CardContent>
        </Card>

        {/* Interventions Needed */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Interventions</CardTitle>
            <Target className="h-4 w-4 text-red-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{interventionsNeeded}</div>
            <p className="text-xs text-muted-foreground mt-1">
              Immediate action needed
            </p>
            {interventionsNeeded > 0 && (
              <p className="text-xs text-red-600 mt-2 font-medium">
                Critical priority
              </p>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Progression Risk */}
      {predictions?.progression_risk && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Progression Risk Assessment</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center gap-4">
              <div className={`px-4 py-2 rounded-lg ${getRiskColor(predictions.progression_risk)}`}>
                <div className="text-sm font-medium uppercase">
                  {predictions.progression_risk.replace('_', ' ')} RISK
                </div>
              </div>
              {predictions?.estimated_progression_months && (
                <div className="flex items-center gap-2 text-gray-600">
                  <Clock className="h-4 w-4" />
                  <span className="text-sm">
                    Estimated progression in ~{predictions.estimated_progression_months} months
                  </span>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      )}

      {/* High Priority Interventions */}
      {highRiskMemories.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-red-500" />
              High Priority Memory Interventions
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {highRiskMemories.map((memory) => (
              <Alert key={memory.memory_id} variant="destructive" className="bg-red-50 border-red-200">
                <AlertTriangle className="h-4 w-4" />
                <AlertDescription>
                  <div className="flex justify-between items-start">
                    <div>
                      <strong className="text-red-900">{memory.name}</strong>
                      <span className="text-red-700 text-sm ml-2">({memory.type})</span>
                      <div className="text-sm text-red-700 mt-1">
                        Decay Risk: {(memory.decay_probability * 100).toFixed(0)}%
                        {memory.days_until_critical > 0 && (
                          <span className="ml-3">
                            ⏰ Critical in {memory.days_until_critical} days
                          </span>
                        )}
                      </div>
                    </div>
                    {memory.intervention_recommended && (
                      <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-600 text-white">
                        Action Required
                      </span>
                    )}
                  </div>
                </AlertDescription>
              </Alert>
            ))}
          </CardContent>
        </Card>
      )}

      {/* No Data State */}
      {totalMemories === 0 && highRiskMemories.length === 0 && (
        <Card>
          <CardContent className="py-12 text-center text-gray-500">
            <Brain className="h-12 w-12 mx-auto mb-4 text-gray-400" />
            <p className="text-lg font-medium">No memory data available</p>
            <p className="text-sm mt-2">Start tracking memories to see risk analysis</p>
          </CardContent>
        </Card>
      )}

      {/* Recommendations */}
      {atRiskCount > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="text-lg">Recommended Actions</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm">
              {interventionsNeeded > 0 && (
                <li className="flex items-start gap-2">
                  <span className="text-red-500 font-bold">•</span>
                  <span>Schedule immediate interventions for {interventionsNeeded} critical memories</span>
                </li>
              )}
              {atRiskCount > 3 && (
                <li className="flex items-start gap-2">
                  <span className="text-orange-500 font-bold">•</span>
                  <span>Implement spaced repetition exercises for at-risk memories</span>
                </li>
              )}
              <li className="flex items-start gap-2">
                <span className="text-blue-500 font-bold">•</span>
                <span>Review and update memory assessments weekly</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-500 font-bold">•</span>
                <span>Continue reinforcing strong memories through regular engagement</span>
              </li>
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
