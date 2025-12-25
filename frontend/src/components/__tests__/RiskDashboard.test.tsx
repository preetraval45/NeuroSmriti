import { render, screen } from '@testing-library/react'
import RiskDashboard from '../RiskDashboard'

describe('RiskDashboard', () => {
  it('renders with no data', () => {
    render(<RiskDashboard predictions={{}} />)
    expect(screen.getByText(/No memory data available/i)).toBeInTheDocument()
  })

  it('displays total memories count', () => {
    const predictions = {
      total_memories: 50,
      at_risk_count: 10,
      intervention_recommended_count: 3
    }

    render(<RiskDashboard predictions={predictions} />)
    expect(screen.getByText('50')).toBeInTheDocument()
    expect(screen.getByText('10')).toBeInTheDocument()
  })

  it('shows high risk memories', () => {
    const predictions = {
      total_memories: 50,
      at_risk_count: 5,
      high_risk_memories: [
        {
          memory_id: '1',
          name: 'Test Memory',
          type: 'person',
          decay_probability: 0.85,
          days_until_critical: 10,
          intervention_recommended: true
        }
      ]
    }

    render(<RiskDashboard predictions={predictions} />)
    expect(screen.getByText('Test Memory')).toBeInTheDocument()
    expect(screen.getByText(/85%/)).toBeInTheDocument()
  })

  it('displays progression risk', () => {
    const predictions = {
      progression_risk: 'high',
      estimated_progression_months: 12,
      predicted_stage: 2
    }

    render(<RiskDashboard predictions={predictions} />)
    expect(screen.getByText(/HIGH RISK/i)).toBeInTheDocument()
    expect(screen.getByText(/12 months/i)).toBeInTheDocument()
  })

  it('shows patient name when provided', () => {
    render(<RiskDashboard predictions={{}} patientName="John Doe" />)
    expect(screen.getByText('John Doe')).toBeInTheDocument()
  })
})
