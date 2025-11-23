'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface TestResult {
  name: string
  score: number
  accuracy: number
  date: string
  status: 'passed' | 'needs_attention' | 'critical'
}

interface Memory {
  id: string
  title: string
  description: string
  date: string
  type: 'photo' | 'audio' | 'video' | 'text'
  importance: 'high' | 'medium' | 'low'
}

interface TreatmentPlan {
  name: string
  description: string
  frequency: string
  startDate: string
  status: 'active' | 'completed' | 'scheduled'
}

interface MealPlan {
  time: string
  meal: string
  foods: string[]
  notes: string
}

interface Patient {
  id: string
  name: string
  age: number
  gender: 'Male' | 'Female'
  stage: string
  alzheimerLevel: 'None' | 'Pre-clinical' | 'MCI' | 'Mild' | 'Moderate' | 'Severe'
  diagnosis: string
  diagnosisDate: string
  riskScore: number
  lastVisit: string
  nextAppointment: string
  caregiver: string
  caregiverPhone: string
  email: string
  address: string
  phone: string
  status: 'Active' | 'Monitoring' | 'Critical'
  cognitiveScore: number
  medications: string[]
  allergies: string[]
  emergencyContact: string
  insuranceProvider: string
  doctorName: string
  testResults: TestResult[]
  memories: Memory[]
  dailyRoutine: string[]
  preferences: string[]
  notes: string
  treatmentPlan: TreatmentPlan[]
  mealPlan: MealPlan[]
  exercisePlan: string[]
}

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [filterStage, setFilterStage] = useState('all')
  const [filterStatus, setFilterStatus] = useState('all')
  const [sortBy, setSortBy] = useState('name')
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null)
  const [showAddModal, setShowAddModal] = useState(false)
  const [activeTab, setActiveTab] = useState<'overview' | 'tests' | 'memories' | 'care' | 'treatment' | 'meals'>('overview')
  const [currentPage, setCurrentPage] = useState(1)
  const patientsPerPage = 10

  useEffect(() => {
    // Helper function to generate patients programmatically
    const firstNames = {
      male: ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles', 'Christopher', 'Daniel', 'Matthew', 'Anthony', 'Mark', 'Donald', 'Steven', 'Paul', 'Andrew', 'Joshua', 'Kenneth', 'Kevin', 'Brian', 'George', 'Timothy', 'Ronald', 'Edward', 'Jason', 'Jeffrey', 'Ryan', 'Jacob', 'Gary', 'Nicholas', 'Eric', 'Jonathan', 'Stephen', 'Larry', 'Justin', 'Scott', 'Brandon', 'Benjamin', 'Samuel', 'Raymond', 'Gregory', 'Frank', 'Alexander', 'Patrick', 'Jack', 'Dennis', 'Jerry'],
      female: ['Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth', 'Susan', 'Jessica', 'Sarah', 'Karen', 'Lisa', 'Nancy', 'Betty', 'Margaret', 'Sandra', 'Ashley', 'Kimberly', 'Emily', 'Donna', 'Michelle', 'Dorothy', 'Carol', 'Amanda', 'Melissa', 'Deborah', 'Stephanie', 'Rebecca', 'Sharon', 'Laura', 'Cynthia', 'Kathleen', 'Amy', 'Angela', 'Shirley', 'Anna', 'Brenda', 'Pamela', 'Emma', 'Nicole', 'Helen', 'Samantha', 'Katherine', 'Christine', 'Debra', 'Rachel', 'Carolyn', 'Janet', 'Catherine', 'Maria', 'Heather']
    }
    const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts']
    const doctors = ['Dr. Sarah Mitchell', 'Dr. James Wilson', 'Dr. Emily Rodriguez', 'Dr. Michael Chen', 'Dr. Lisa Park', 'Dr. Robert Kim', 'Dr. Jennifer Lee', 'Dr. David Thompson', 'Dr. Amanda Foster', 'Dr. Richard Brown']
    const insurers = ['Blue Cross Blue Shield', 'Medicare', 'Medicare Advantage', 'United Healthcare', 'Aetna', 'Cigna', 'Humana', 'Kaiser Permanente', 'Anthem', 'Molina Healthcare']
    const streets = ['Oak Street', 'Maple Drive', 'Pine Avenue', 'Cedar Road', 'Elm Court', 'Birch Lane', 'Willow Street', 'Spruce Avenue', 'Cherry Boulevard', 'Walnut Way', 'Hickory Lane', 'Ash Street', 'Poplar Drive', 'Magnolia Court', 'Cypress Road']
    const cities = ['Charlotte, NC', 'Raleigh, NC', 'Durham, NC', 'Greensboro, NC', 'Winston-Salem, NC', 'Cary, NC', 'Wilmington, NC', 'High Point, NC', 'Fayetteville, NC', 'Asheville, NC']

    const generatePatient = (id: number, alzheimerLevel: 'None' | 'Pre-clinical' | 'MCI' | 'Mild' | 'Moderate' | 'Severe', isYoungOnset: boolean = false): Patient => {
      const gender: 'Male' | 'Female' = Math.random() > 0.5 ? 'Male' : 'Female'
      const nameList = gender === 'Male' ? firstNames.male : firstNames.female
      const firstName = nameList[Math.floor(Math.random() * nameList.length)]
      const lastName = lastNames[Math.floor(Math.random() * lastNames.length)]

      // Age based on condition
      let age: number
      if (isYoungOnset) {
        age = 42 + Math.floor(Math.random() * 18) // 42-59 for young onset
      } else if (alzheimerLevel === 'None') {
        age = 55 + Math.floor(Math.random() * 30) // 55-84 for healthy
      } else if (alzheimerLevel === 'Pre-clinical') {
        age = 55 + Math.floor(Math.random() * 20) // 55-74
      } else if (alzheimerLevel === 'MCI') {
        age = 60 + Math.floor(Math.random() * 20) // 60-79
      } else if (alzheimerLevel === 'Mild') {
        age = 62 + Math.floor(Math.random() * 20) // 62-81
      } else if (alzheimerLevel === 'Moderate') {
        age = 68 + Math.floor(Math.random() * 18) // 68-85
      } else {
        age = 72 + Math.floor(Math.random() * 16) // 72-87
      }

      // Diagnosis based on level
      let diagnosis: string, stage: string, riskScore: number, cognitiveScore: number, status: 'Active' | 'Monitoring' | 'Critical'
      const diagnosisVariants = {
        'None': [
          { diagnosis: 'Healthy - Preventive Monitoring', stage: 'No Cognitive Impairment' },
          { diagnosis: 'Healthy - Family History Monitoring', stage: 'No Cognitive Impairment' },
          { diagnosis: 'Healthy - Annual Screening', stage: 'No Cognitive Impairment' },
          { diagnosis: 'Vascular Dementia - Post Stroke', stage: 'Vascular Dementia (Not Alzheimer\'s)' },
          { diagnosis: 'Dementia with Lewy Bodies', stage: 'Lewy Body Dementia (Not Alzheimer\'s)' },
          { diagnosis: 'Behavioral Variant Frontotemporal Dementia', stage: 'Frontotemporal Dementia (Not Alzheimer\'s)' },
          { diagnosis: 'Primary Progressive Aphasia', stage: 'Language Variant FTD (Not Alzheimer\'s)' },
          { diagnosis: 'Parkinson\'s Disease Dementia', stage: 'Parkinson\'s Dementia (Not Alzheimer\'s)' }
        ],
        'Pre-clinical': [
          { diagnosis: 'Pre-Clinical Alzheimer\'s Disease - Biomarker Positive', stage: 'Pre-Clinical/Very Early Stage' },
          { diagnosis: 'Pre-Clinical AD - PET Amyloid Positive', stage: 'Pre-Clinical Stage' },
          { diagnosis: 'Subjective Cognitive Decline - Biomarker Positive', stage: 'Pre-Clinical/SCD' }
        ],
        'MCI': [
          { diagnosis: 'Mild Cognitive Impairment (MCI) - Amnestic Type', stage: 'Mild Cognitive Impairment' },
          { diagnosis: 'Amnestic MCI - Single Domain', stage: 'Mild Cognitive Impairment' },
          { diagnosis: 'Amnestic MCI - Multi Domain', stage: 'Mild Cognitive Impairment' },
          { diagnosis: 'MCI due to Alzheimer\'s Disease', stage: 'MCI - AD Biomarker Positive' }
        ],
        'Mild': [
          { diagnosis: 'Alzheimer\'s Disease - Early/Mild Stage', stage: 'Early Stage Alzheimer\'s' },
          { diagnosis: 'Mild Alzheimer\'s Dementia', stage: 'Mild Alzheimer\'s Disease' },
          { diagnosis: isYoungOnset ? 'Early-Onset Alzheimer\'s Disease - Mild Stage' : 'Alzheimer\'s Disease - Mild', stage: isYoungOnset ? 'Young-Onset Alzheimer\'s (Mild)' : 'Mild Alzheimer\'s' }
        ],
        'Moderate': [
          { diagnosis: 'Alzheimer\'s Disease - Moderate Stage', stage: 'Moderate Stage Alzheimer\'s' },
          { diagnosis: 'Moderate Alzheimer\'s Dementia', stage: 'Moderate Alzheimer\'s Disease' },
          { diagnosis: isYoungOnset ? 'Early-Onset Alzheimer\'s Disease - Moderate Stage' : 'Alzheimer\'s Disease - Moderate', stage: isYoungOnset ? 'Young-Onset Alzheimer\'s (Moderate)' : 'Moderate Alzheimer\'s' }
        ],
        'Severe': [
          { diagnosis: 'Alzheimer\'s Disease - Severe/Late Stage', stage: 'Severe Alzheimer\'s' },
          { diagnosis: 'Advanced Alzheimer\'s Dementia', stage: 'Late Stage Alzheimer\'s Disease' },
          { diagnosis: isYoungOnset ? 'Early-Onset Alzheimer\'s Disease - Advanced Stage' : 'Alzheimer\'s Disease - End Stage', stage: isYoungOnset ? 'Young-Onset Alzheimer\'s (Severe)' : 'Severe/End Stage Alzheimer\'s' }
        ]
      }

      const variant = diagnosisVariants[alzheimerLevel][Math.floor(Math.random() * diagnosisVariants[alzheimerLevel].length)]
      diagnosis = variant.diagnosis
      stage = variant.stage

      // Set scores based on level
      switch (alzheimerLevel) {
        case 'None':
          riskScore = 5 + Math.floor(Math.random() * 25)
          cognitiveScore = 85 + Math.floor(Math.random() * 15)
          status = 'Active'
          break
        case 'Pre-clinical':
          riskScore = 20 + Math.floor(Math.random() * 20)
          cognitiveScore = 82 + Math.floor(Math.random() * 12)
          status = 'Active'
          break
        case 'MCI':
          riskScore = 35 + Math.floor(Math.random() * 20)
          cognitiveScore = 65 + Math.floor(Math.random() * 18)
          status = 'Monitoring'
          break
        case 'Mild':
          riskScore = 40 + Math.floor(Math.random() * 20)
          cognitiveScore = 55 + Math.floor(Math.random() * 25)
          status = Math.random() > 0.7 ? 'Monitoring' : 'Active'
          break
        case 'Moderate':
          riskScore = 55 + Math.floor(Math.random() * 25)
          cognitiveScore = 35 + Math.floor(Math.random() * 25)
          status = Math.random() > 0.5 ? 'Critical' : 'Monitoring'
          break
        case 'Severe':
          riskScore = 75 + Math.floor(Math.random() * 20)
          cognitiveScore = 15 + Math.floor(Math.random() * 25)
          status = 'Critical'
          break
      }

      const caregiverRelations = ['Spouse', 'Son', 'Daughter', 'Sibling', 'Professional Caregiver', 'Grandchild']
      const caregiverRel = caregiverRelations[Math.floor(Math.random() * caregiverRelations.length)]
      const caregiverFirst = (Math.random() > 0.5 ? firstNames.male : firstNames.female)[Math.floor(Math.random() * 50)]

      // Medications based on level
      const medicationsMap: Record<string, string[][]> = {
        'None': [[], ['Vitamin D3 2000 IU'], ['Omega-3 1000mg'], ['Atorvastatin 20mg']],
        'Pre-clinical': [['Vitamin E 400 IU', 'Omega-3 supplements'], ['B-Complex vitamins', 'Vitamin D3'], ['Fish Oil 2000mg', 'CoQ10']],
        'MCI': [['Donepezil 5mg', 'Vitamin E'], ['Galantamine 8mg', 'Omega-3'], ['Rivastigmine patch 4.6mg', 'B12']],
        'Mild': [['Donepezil 10mg', 'Vitamin B12', 'Omega-3'], ['Rivastigmine 6mg', 'Vitamin E 400 IU'], ['Galantamine 16mg', 'Fish Oil']],
        'Moderate': [['Donepezil 23mg', 'Memantine 10mg', 'Sertraline 50mg'], ['Memantine 28mg', 'Rivastigmine patch 9.5mg', 'Melatonin 3mg'], ['Donepezil 10mg', 'Memantine 20mg', 'Trazodone 50mg']],
        'Severe': [['Memantine 28mg', 'Donepezil 23mg', 'Quetiapine 50mg', 'Trazodone 100mg'], ['Memantine 28mg', 'Rivastigmine patch 13.3mg', 'Lorazepam 0.5mg PRN'], ['Donepezil 23mg', 'Memantine 28mg', 'Mirtazapine 15mg']]
      }
      const medications = medicationsMap[alzheimerLevel][Math.floor(Math.random() * medicationsMap[alzheimerLevel].length)]

      // Test results based on level
      const generateTestResults = (): TestResult[] => {
        const baseScore = cognitiveScore
        const tests = ['Memory Recall', 'Attention Test', 'Executive Function', 'Language Skills', 'Visual-Spatial', 'Processing Speed']
        const selectedTests = tests.sort(() => Math.random() - 0.5).slice(0, 2 + Math.floor(Math.random() * 3))

        return selectedTests.map(test => {
          const variance = Math.floor(Math.random() * 20) - 10
          const score = Math.max(10, Math.min(100, baseScore + variance))
          const accuracy = Math.max(70, Math.min(99, 75 + Math.floor(score / 4)))
          let testStatus: 'passed' | 'needs_attention' | 'critical'
          if (score >= 75) testStatus = 'passed'
          else if (score >= 50) testStatus = 'needs_attention'
          else testStatus = 'critical'

          return {
            name: test,
            score,
            accuracy,
            date: '2024-01-' + (10 + Math.floor(Math.random() * 15)),
            status: testStatus
          }
        })
      }

      // Treatment plans based on level
      const treatmentPlansMap: Record<string, TreatmentPlan[][]> = {
        'None': [
          [{ name: 'Annual Cognitive Screening', description: 'Preventive monitoring', frequency: 'Yearly', startDate: '2023-01-01', status: 'active' }],
          [{ name: 'Brain Health Program', description: 'Cognitive exercises and puzzles', frequency: 'Daily', startDate: '2023-01-01', status: 'active' }]
        ],
        'Pre-clinical': [
          [{ name: 'Clinical Trial Participation', description: 'Anti-amyloid therapy trial', frequency: 'Monthly', startDate: '2023-06-01', status: 'active' }, { name: 'MIND Diet Program', description: 'Brain-healthy nutrition', frequency: 'Daily', startDate: '2023-06-01', status: 'active' }]
        ],
        'MCI': [
          [{ name: 'Cognitive Behavioral Therapy', description: 'Weekly sessions for cognitive function', frequency: 'Weekly', startDate: '2023-03-01', status: 'active' }, { name: 'Memory Training Program', description: 'Daily exercises using memory apps', frequency: 'Daily', startDate: '2023-04-01', status: 'active' }]
        ],
        'Mild': [
          [{ name: 'Cholinesterase Inhibitor Therapy', description: 'Medication for symptom management', frequency: 'Daily', startDate: '2023-05-01', status: 'active' }, { name: 'Cognitive Stimulation Therapy', description: 'Group therapy sessions', frequency: '2x per week', startDate: '2023-06-01', status: 'active' }]
        ],
        'Moderate': [
          [{ name: '24/7 Care Assistance', description: 'Full-time caregiver support', frequency: 'Daily', startDate: '2022-01-01', status: 'active' }, { name: 'Occupational Therapy', description: 'Maintaining daily living skills', frequency: '3x per week', startDate: '2022-03-01', status: 'active' }]
        ],
        'Severe': [
          [{ name: 'Palliative Care', description: 'Comfort-focused care approach', frequency: 'Daily', startDate: '2023-01-01', status: 'active' }, { name: 'Sensory Stimulation', description: 'Music, touch, and visual therapy', frequency: 'Daily', startDate: '2023-01-01', status: 'active' }]
        ]
      }

      // Meal plans
      const mealPlan: MealPlan[] = [
        { time: '8:00 AM', meal: 'Breakfast', foods: ['Oatmeal with berries', 'Green tea', 'Whole grain toast'], notes: 'Brain-healthy antioxidants' },
        { time: '12:00 PM', meal: 'Lunch', foods: ['Grilled salmon', 'Leafy green salad', 'Quinoa'], notes: 'Omega-3 rich for cognitive function' },
        { time: '6:00 PM', meal: 'Dinner', foods: ['Lean protein', 'Steamed vegetables', 'Brown rice'], notes: 'Light dinner, easy to digest' }
      ]

      // Exercise plans based on level
      const exercisePlansMap: Record<string, string[]> = {
        'None': ['Morning jog - 45 minutes', 'Swimming - 30 minutes', 'Yoga - 30 minutes'],
        'Pre-clinical': ['HIIT training - 30 minutes', 'Strength training - 20 minutes', 'Walking - 10,000 steps'],
        'MCI': ['Morning walk - 30 minutes', 'Chair yoga - 20 minutes', 'Balance exercises - 15 minutes'],
        'Mild': ['Walking - 30 minutes', 'Tai chi - 20 minutes', 'Light stretching - 15 minutes'],
        'Moderate': ['Gentle stretching - 15 minutes', 'Seated exercises - 20 minutes', 'Assisted walking - 15 minutes'],
        'Severe': ['Range of motion exercises', 'Passive stretching', 'Massage therapy']
      }

      // Daily routines based on level
      const dailyRoutinesMap: Record<string, string[]> = {
        'None': ['6:30 AM - Wake up', '7:00 AM - Exercise', '8:00 AM - Breakfast', '10:00 AM - Hobbies', '12:00 PM - Lunch', '6:00 PM - Dinner'],
        'Pre-clinical': ['6:30 AM - Wake up', '7:00 AM - Exercise', '8:00 AM - Breakfast', '9:00 AM - Brain training', '12:00 PM - Lunch', '6:00 PM - Dinner'],
        'MCI': ['7:00 AM - Wake up', '8:00 AM - Breakfast', '9:00 AM - Memory exercises', '12:00 PM - Lunch', '3:00 PM - Activities', '6:00 PM - Dinner'],
        'Mild': ['7:00 AM - Wake up', '8:00 AM - Breakfast with medication', '9:30 AM - Therapy', '12:00 PM - Lunch', '3:00 PM - Light activities', '6:00 PM - Dinner'],
        'Moderate': ['7:30 AM - Wake up with assistance', '8:30 AM - Breakfast', '10:00 AM - Therapy', '12:00 PM - Lunch', '3:00 PM - Supervised activities', '5:30 PM - Dinner'],
        'Severe': ['8:00 AM - Wake up with full assistance', '9:00 AM - Breakfast (assisted)', '10:30 AM - Sensory therapy', '12:30 PM - Lunch', '3:00 PM - Rest/Comfort care', '5:30 PM - Dinner']
      }

      const preferences = ['Classical music', 'Family photos', 'Gardening', 'Reading', 'Painting', 'Walking', 'Puzzles', 'Cooking', 'Knitting', 'Bird watching']
      const allergies = [['None'], ['Penicillin'], ['Sulfa drugs'], ['Aspirin'], ['Latex'], ['Shellfish'], ['Ibuprofen'], ['Codeine']]

      const year = 2024
      const month = Math.floor(Math.random() * 12) + 1
      const day = Math.floor(Math.random() * 28) + 1
      const diagnosisDate = alzheimerLevel === 'None' && Math.random() > 0.5 ? 'N/A' : `${2019 + Math.floor(Math.random() * 5)}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`

      return {
        id: `P${String(id).padStart(3, '0')}`,
        name: `${firstName} ${lastName}`,
        age,
        gender,
        stage,
        alzheimerLevel,
        diagnosis,
        diagnosisDate,
        riskScore,
        lastVisit: `2024-01-${String(10 + Math.floor(Math.random() * 15)).padStart(2, '0')}`,
        nextAppointment: `2024-02-${String(10 + Math.floor(Math.random() * 18)).padStart(2, '0')}`,
        caregiver: `${caregiverFirst} ${lastName} (${caregiverRel})`,
        caregiverPhone: `+1 (555) ${String(Math.floor(Math.random() * 900) + 100).padStart(3, '0')}-${String(Math.floor(Math.random() * 9000) + 1000)}`,
        email: `${firstName.toLowerCase()}.${lastName.toLowerCase()}@email.com`,
        address: `${Math.floor(Math.random() * 900) + 100} ${streets[Math.floor(Math.random() * streets.length)]}, ${cities[Math.floor(Math.random() * cities.length)]} ${28200 + Math.floor(Math.random() * 20)}`,
        phone: `+1 (555) ${String(Math.floor(Math.random() * 900) + 100).padStart(3, '0')}-${String(Math.floor(Math.random() * 9000) + 1000)}`,
        status,
        cognitiveScore,
        medications,
        allergies: allergies[Math.floor(Math.random() * allergies.length)],
        emergencyContact: `${caregiverFirst} ${lastName}: +1 (555) ${String(Math.floor(Math.random() * 900) + 100).padStart(3, '0')}-${String(Math.floor(Math.random() * 9000) + 1000)}`,
        insuranceProvider: insurers[Math.floor(Math.random() * insurers.length)],
        doctorName: doctors[Math.floor(Math.random() * doctors.length)],
        testResults: generateTestResults(),
        memories: [{ id: 'm1', title: 'Life Memory', description: 'Important life milestone', date: `${1960 + Math.floor(Math.random() * 40)}`, type: 'photo' as const, importance: 'high' as const }],
        dailyRoutine: dailyRoutinesMap[alzheimerLevel],
        preferences: preferences.sort(() => Math.random() - 0.5).slice(0, 3),
        notes: isYoungOnset ? `Young-onset case (diagnosed before age 65). ${alzheimerLevel} stage. Requires specialized support.` : `${alzheimerLevel === 'None' ? 'No Alzheimer\'s - ' + diagnosis : alzheimerLevel + ' stage Alzheimer\'s'}. Regular monitoring.`,
        treatmentPlan: treatmentPlansMap[alzheimerLevel][Math.floor(Math.random() * treatmentPlansMap[alzheimerLevel].length)],
        mealPlan,
        exercisePlan: exercisePlansMap[alzheimerLevel]
      }
    }

    // Generate 200 patients: 150 with Alzheimer's (various stages including young-onset), 50 without
    const generatedPatients: Patient[] = []
    let patientId = 1

    // 50 Non-Alzheimer's patients (healthy, vascular dementia, lewy body, FTD, etc.)
    for (let i = 0; i < 50; i++) {
      generatedPatients.push(generatePatient(patientId++, 'None'))
    }

    // 150 Alzheimer's patients with varied stages
    // 15 Pre-clinical
    for (let i = 0; i < 15; i++) {
      generatedPatients.push(generatePatient(patientId++, 'Pre-clinical'))
    }

    // 30 MCI (including 5 young-onset)
    for (let i = 0; i < 25; i++) {
      generatedPatients.push(generatePatient(patientId++, 'MCI'))
    }
    for (let i = 0; i < 5; i++) {
      generatedPatients.push(generatePatient(patientId++, 'MCI', true))
    }

    // 40 Mild (including 8 young-onset)
    for (let i = 0; i < 32; i++) {
      generatedPatients.push(generatePatient(patientId++, 'Mild'))
    }
    for (let i = 0; i < 8; i++) {
      generatedPatients.push(generatePatient(patientId++, 'Mild', true))
    }

    // 35 Moderate (including 6 young-onset)
    for (let i = 0; i < 29; i++) {
      generatedPatients.push(generatePatient(patientId++, 'Moderate'))
    }
    for (let i = 0; i < 6; i++) {
      generatedPatients.push(generatePatient(patientId++, 'Moderate', true))
    }

    // 30 Severe (including 5 young-onset)
    for (let i = 0; i < 25; i++) {
      generatedPatients.push(generatePatient(patientId++, 'Severe'))
    }
    for (let i = 0; i < 5; i++) {
      generatedPatients.push(generatePatient(patientId++, 'Severe', true))
    }

    setPatients(generatedPatients)
  }, [])

  const filteredPatients = patients
    .filter(p => {
      const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) || p.id.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesStage = filterStage === 'all' || p.alzheimerLevel === filterStage
      const matchesStatus = filterStatus === 'all' || p.status === filterStatus
      return matchesSearch && matchesStage && matchesStatus
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name': return a.name.localeCompare(b.name)
        case 'age': return b.age - a.age
        case 'risk': return b.riskScore - a.riskScore
        case 'cognitive': return a.cognitiveScore - b.cognitiveScore
        default: return 0
      }
    })

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active': return 'bg-green-100 text-green-700'
      case 'Monitoring': return 'bg-yellow-100 text-yellow-700'
      case 'Critical': return 'bg-red-100 text-red-700'
      default: return 'bg-gray-100 text-gray-700'
    }
  }

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'None': return 'bg-green-100 text-green-700'
      case 'Pre-clinical': return 'bg-blue-100 text-blue-700'
      case 'MCI': return 'bg-yellow-100 text-yellow-700'
      case 'Mild': return 'bg-orange-100 text-orange-700'
      case 'Moderate': return 'bg-red-100 text-red-700'
      case 'Severe': return 'bg-purple-100 text-purple-700'
      default: return 'bg-gray-100 text-gray-700'
    }
  }

  const stats = {
    total: patients.length,
    noAlzheimers: patients.filter(p => p.alzheimerLevel === 'None').length,
    mci: patients.filter(p => p.alzheimerLevel === 'MCI' || p.alzheimerLevel === 'Pre-clinical').length,
    alzheimers: patients.filter(p => ['Mild', 'Moderate', 'Severe'].includes(p.alzheimerLevel)).length,
    critical: patients.filter(p => p.status === 'Critical').length
  }

  // Pagination
  const totalPages = Math.ceil(filteredPatients.length / patientsPerPage)
  const startIndex = (currentPage - 1) * patientsPerPage
  const endIndex = startIndex + patientsPerPage
  const currentPatients = filteredPatients.slice(startIndex, endIndex)

  // Reset to page 1 when filters change
  useEffect(() => {
    setCurrentPage(1)
  }, [searchTerm, filterStage, filterStatus, sortBy])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-purple-700 via-indigo-700 to-blue-700 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold mb-2">Patient Management</h1>
              <p className="text-purple-100">Complete patient care with treatment plans, meal plans, and cognitive assessments</p>
            </div>
            <button type="button" onClick={() => setShowAddModal(true)} className="px-6 py-3 bg-white text-purple-700 rounded-xl font-semibold hover:bg-purple-50 transition flex items-center shadow-lg">
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
              Add Patient
            </button>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-8">
        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-sm border-l-4 border-purple-500">
            <div className="text-3xl font-bold text-purple-600">{stats.total}</div>
            <div className="text-gray-600 text-sm">Total Patients</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border-l-4 border-green-500">
            <div className="text-3xl font-bold text-green-600">{stats.noAlzheimers}</div>
            <div className="text-gray-600 text-sm">No Alzheimer&apos;s</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border-l-4 border-yellow-500">
            <div className="text-3xl font-bold text-yellow-600">{stats.mci}</div>
            <div className="text-gray-600 text-sm">MCI/Pre-clinical</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border-l-4 border-orange-500">
            <div className="text-3xl font-bold text-orange-600">{stats.alzheimers}</div>
            <div className="text-gray-600 text-sm">Alzheimer&apos;s</div>
          </div>
          <div className="bg-white rounded-xl p-6 shadow-sm border-l-4 border-red-500">
            <div className="text-3xl font-bold text-red-600">{stats.critical}</div>
            <div className="text-gray-600 text-sm">Critical</div>
          </div>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-xl shadow-sm p-4 mb-6">
          <div className="grid md:grid-cols-4 gap-4">
            <div>
              <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">Search</label>
              <input id="search" type="text" placeholder="Search..." value={searchTerm} onChange={(e) => setSearchTerm(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500" />
            </div>
            <div>
              <label htmlFor="stage" className="block text-sm font-medium text-gray-700 mb-1">Alzheimer&apos;s Level</label>
              <select id="stage" value={filterStage} onChange={(e) => setFilterStage(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500">
                <option value="all">All Levels</option>
                <option value="None">No Alzheimer&apos;s</option>
                <option value="Pre-clinical">Pre-clinical</option>
                <option value="MCI">MCI</option>
                <option value="Mild">Mild</option>
                <option value="Moderate">Moderate</option>
                <option value="Severe">Severe</option>
              </select>
            </div>
            <div>
              <label htmlFor="status" className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select id="status" value={filterStatus} onChange={(e) => setFilterStatus(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500">
                <option value="all">All Status</option>
                <option value="Active">Active</option>
                <option value="Monitoring">Monitoring</option>
                <option value="Critical">Critical</option>
              </select>
            </div>
            <div>
              <label htmlFor="sort" className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
              <select id="sort" value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500">
                <option value="name">Name</option>
                <option value="age">Age</option>
                <option value="risk">Risk Score</option>
                <option value="cognitive">Cognitive Score</option>
              </select>
            </div>
          </div>
        </div>

        {/* Patients Table */}
        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          {/* Table Header with Count */}
          <div className="px-6 py-4 border-b bg-gray-50 flex justify-between items-center">
            <div className="text-sm text-gray-600">
              Showing <span className="font-semibold">{startIndex + 1}</span> to <span className="font-semibold">{Math.min(endIndex, filteredPatients.length)}</span> of <span className="font-semibold">{filteredPatients.length}</span> patients
            </div>
            <div className="text-sm text-gray-500">
              Page {currentPage} of {totalPages}
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Patient</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Diagnosis</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Level</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Cognitive</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Status</th>
                  <th className="px-6 py-4 text-left text-sm font-semibold text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {currentPatients.map((patient) => (
                  <tr key={patient.id} className="hover:bg-gray-50 transition">
                    <td className="px-6 py-4">
                      <div className="flex items-center">
                        <div className="w-10 h-10 bg-gradient-to-r from-purple-400 to-blue-400 rounded-full flex items-center justify-center text-white font-semibold mr-3">{patient.name.charAt(0)}</div>
                        <div>
                          <div className="font-semibold text-gray-900">{patient.name}</div>
                          <div className="text-sm text-gray-500">{patient.age}y • {patient.gender} • {patient.id}</div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4"><span className="text-sm">{patient.diagnosis.substring(0, 30)}...</span></td>
                    <td className="px-6 py-4"><span className={`px-3 py-1 rounded-full text-xs font-medium ${getLevelColor(patient.alzheimerLevel)}`}>{patient.alzheimerLevel}</span></td>
                    <td className="px-6 py-4"><span className={`font-semibold ${patient.cognitiveScore >= 80 ? 'text-green-600' : patient.cognitiveScore >= 60 ? 'text-yellow-600' : 'text-red-600'}`}>{patient.cognitiveScore}/100</span></td>
                    <td className="px-6 py-4"><span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(patient.status)}`}>{patient.status}</span></td>
                    <td className="px-6 py-4">
                      <button type="button" onClick={() => { setSelectedPatient(patient); setActiveTab('overview'); }} className="px-4 py-2 text-purple-600 hover:bg-purple-50 rounded-lg transition font-medium text-sm">View Details</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination Controls */}
          <div className="px-6 py-4 border-t bg-gray-50 flex flex-col sm:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setCurrentPage(1)}
                disabled={currentPage === 1}
                className="px-3 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                First
              </button>
              <button
                type="button"
                onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
                disabled={currentPage === 1}
                className="px-3 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
            </div>

            <div className="flex items-center gap-1">
              {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                let pageNum: number
                if (totalPages <= 5) {
                  pageNum = i + 1
                } else if (currentPage <= 3) {
                  pageNum = i + 1
                } else if (currentPage >= totalPages - 2) {
                  pageNum = totalPages - 4 + i
                } else {
                  pageNum = currentPage - 2 + i
                }
                return (
                  <button
                    key={pageNum}
                    type="button"
                    onClick={() => setCurrentPage(pageNum)}
                    className={`w-10 h-10 text-sm font-medium rounded-lg ${
                      currentPage === pageNum
                        ? 'bg-purple-600 text-white'
                        : 'text-gray-600 bg-white border border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    {pageNum}
                  </button>
                )
              })}
            </div>

            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
                disabled={currentPage === totalPages}
                className="px-3 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
              <button
                type="button"
                onClick={() => setCurrentPage(totalPages)}
                disabled={currentPage === totalPages}
                className="px-3 py-2 text-sm font-medium text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Last
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Patient Details Modal */}
      {selectedPatient && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-5xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            {/* Header */}
            <div className="p-6 border-b bg-gradient-to-r from-purple-600 to-blue-600 text-white">
              <div className="flex justify-between items-start">
                <div className="flex items-center">
                  <div className="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-2xl font-bold mr-4">{selectedPatient.name.charAt(0)}</div>
                  <div>
                    <h2 className="text-2xl font-bold">{selectedPatient.name}</h2>
                    <p className="text-purple-100">{selectedPatient.age} years • {selectedPatient.gender} • {selectedPatient.diagnosis}</p>
                    <div className="flex gap-2 mt-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${selectedPatient.alzheimerLevel === 'None' ? 'bg-green-500' : selectedPatient.alzheimerLevel === 'Severe' ? 'bg-purple-800' : 'bg-white/20'} text-white`}>{selectedPatient.alzheimerLevel}</span>
                      <span className={`px-3 py-1 rounded-full text-xs font-medium ${selectedPatient.status === 'Critical' ? 'bg-red-500' : 'bg-white/20'} text-white`}>{selectedPatient.status}</span>
                    </div>
                  </div>
                </div>
                <button type="button" onClick={() => setSelectedPatient(null)} className="p-2 hover:bg-white/10 rounded-lg" aria-label="Close modal">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
              </div>
            </div>

            {/* Tabs */}
            <div className="border-b bg-gray-50 overflow-x-auto">
              <div className="flex">
                {(['overview', 'treatment', 'meals', 'tests', 'memories', 'care'] as const).map((tab) => (
                  <button key={tab} type="button" onClick={() => setActiveTab(tab)} className={`px-4 py-3 font-medium capitalize whitespace-nowrap transition ${activeTab === tab ? 'text-purple-600 border-b-2 border-purple-600 bg-white' : 'text-gray-600 hover:text-purple-600'}`}>{tab}</button>
                ))}
              </div>
            </div>

            {/* Content */}
            <div className="p-6 overflow-y-auto flex-1">
              {activeTab === 'overview' && (
                <div className="space-y-6">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-purple-50 rounded-xl p-4 text-center">
                      <p className="text-gray-600 text-sm">Risk Score</p>
                      <p className={`text-3xl font-bold ${selectedPatient.riskScore < 30 ? 'text-green-600' : selectedPatient.riskScore < 60 ? 'text-yellow-600' : 'text-red-600'}`}>{selectedPatient.riskScore}%</p>
                    </div>
                    <div className="bg-blue-50 rounded-xl p-4 text-center">
                      <p className="text-gray-600 text-sm">Cognitive Score</p>
                      <p className="text-3xl font-bold text-blue-600">{selectedPatient.cognitiveScore}/100</p>
                    </div>
                    <div className="bg-green-50 rounded-xl p-4 text-center">
                      <p className="text-gray-600 text-sm">Treatments</p>
                      <p className="text-3xl font-bold text-green-600">{selectedPatient.treatmentPlan.length}</p>
                    </div>
                    <div className="bg-pink-50 rounded-xl p-4 text-center">
                      <p className="text-gray-600 text-sm">Diagnosis Date</p>
                      <p className="text-lg font-bold text-pink-600">{selectedPatient.diagnosisDate}</p>
                    </div>
                  </div>
                  <div className="grid md:grid-cols-2 gap-6">
                    <div className="bg-gray-50 rounded-xl p-4">
                      <h4 className="font-semibold mb-3">Contact Information</h4>
                      <div className="space-y-2 text-sm">
                        <p><span className="text-gray-500">Phone:</span> {selectedPatient.phone}</p>
                        <p><span className="text-gray-500">Email:</span> {selectedPatient.email}</p>
                        <p><span className="text-gray-500">Address:</span> {selectedPatient.address}</p>
                      </div>
                    </div>
                    <div className="bg-gray-50 rounded-xl p-4">
                      <h4 className="font-semibold mb-3">Care Team</h4>
                      <div className="space-y-2 text-sm">
                        <p><span className="text-gray-500">Doctor:</span> {selectedPatient.doctorName}</p>
                        <p><span className="text-gray-500">Caregiver:</span> {selectedPatient.caregiver}</p>
                        <p><span className="text-gray-500">Emergency:</span> {selectedPatient.emergencyContact}</p>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold mb-3">Medications</h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedPatient.medications.length > 0 ? selectedPatient.medications.map((med, i) => (
                        <span key={i} className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm">{med}</span>
                      )) : <span className="text-gray-500">No medications</span>}
                    </div>
                  </div>
                  <div className="bg-yellow-50 rounded-xl p-4">
                    <h4 className="font-semibold mb-2">Clinical Notes</h4>
                    <p className="text-gray-700">{selectedPatient.notes}</p>
                  </div>
                </div>
              )}

              {activeTab === 'treatment' && (
                <div className="space-y-4">
                  <h4 className="font-semibold text-lg">Treatment Plan</h4>
                  {selectedPatient.treatmentPlan.map((treatment, i) => (
                    <div key={i} className="bg-gray-50 rounded-xl p-4 border-l-4 border-purple-500">
                      <div className="flex justify-between items-start mb-2">
                        <h5 className="font-semibold text-purple-700">{treatment.name}</h5>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${treatment.status === 'active' ? 'bg-green-100 text-green-700' : treatment.status === 'scheduled' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700'}`}>{treatment.status}</span>
                      </div>
                      <p className="text-gray-600 text-sm mb-2">{treatment.description}</p>
                      <div className="flex gap-4 text-xs text-gray-500">
                        <span>Frequency: {treatment.frequency}</span>
                        <span>Started: {treatment.startDate}</span>
                      </div>
                    </div>
                  ))}
                  <div className="mt-4">
                    <h4 className="font-semibold text-lg mb-3">Exercise Plan</h4>
                    <div className="bg-blue-50 rounded-xl p-4">
                      <ul className="space-y-2">
                        {selectedPatient.exercisePlan.map((exercise, i) => (
                          <li key={i} className="flex items-center"><span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>{exercise}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              )}

              {activeTab === 'meals' && (
                <div className="space-y-4">
                  <h4 className="font-semibold text-lg">Daily Meal Plan</h4>
                  {selectedPatient.mealPlan.map((meal, i) => (
                    <div key={i} className="bg-gray-50 rounded-xl p-4">
                      <div className="flex items-center mb-3">
                        <span className="text-2xl mr-3">{meal.meal === 'Breakfast' ? '🌅' : meal.meal === 'Lunch' ? '☀️' : '🌙'}</span>
                        <div>
                          <h5 className="font-semibold">{meal.meal}</h5>
                          <span className="text-sm text-gray-500">{meal.time}</span>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-2 mb-2">
                        {meal.foods.map((food, j) => (
                          <span key={j} className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm">{food}</span>
                        ))}
                      </div>
                      <p className="text-sm text-gray-600 italic">{meal.notes}</p>
                    </div>
                  ))}
                </div>
              )}

              {activeTab === 'tests' && (
                <div className="space-y-4">
                  <h4 className="font-semibold text-lg">Test Results</h4>
                  {selectedPatient.testResults.map((test, i) => (
                    <div key={i} className="bg-gray-50 rounded-xl p-4 flex items-center justify-between">
                      <div>
                        <span className="font-medium">{test.name}</span>
                        <span className={`ml-3 px-2 py-0.5 rounded-full text-xs font-medium ${test.status === 'passed' ? 'bg-green-100 text-green-700' : test.status === 'needs_attention' ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700'}`}>{test.status.replace('_', ' ')}</span>
                        <p className="text-sm text-gray-500">{test.date}</p>
                      </div>
                      <div className="text-right">
                        <div className="text-2xl font-bold text-purple-600">{test.score}/100</div>
                        <div className="text-sm text-green-600">{test.accuracy}% accuracy</div>
                      </div>
                    </div>
                  ))}
                  <Link href="/cognitive-tests" className="inline-block px-6 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700 transition">Run New Test</Link>
                </div>
              )}

              {activeTab === 'memories' && (
                <div className="space-y-4">
                  <h4 className="font-semibold text-lg">Memory Collection</h4>
                  <div className="grid md:grid-cols-2 gap-4">
                    {selectedPatient.memories.map((memory) => (
                      <div key={memory.id} className={`rounded-xl p-4 border-l-4 ${memory.importance === 'high' ? 'bg-pink-50 border-pink-500' : 'bg-blue-50 border-blue-500'}`}>
                        <div className="flex items-start justify-between">
                          <div>
                            <h5 className="font-semibold">{memory.title}</h5>
                            <p className="text-sm text-gray-600 mt-1">{memory.description}</p>
                            <p className="text-xs text-gray-500 mt-2">{memory.date}</p>
                          </div>
                          <span className="text-2xl">{memory.type === 'photo' ? '📷' : memory.type === 'video' ? '🎥' : '📝'}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                  <Link href="/memory-games" className="inline-block px-6 py-3 bg-pink-600 text-white rounded-xl font-semibold hover:bg-pink-700 transition">Memory Exercises</Link>
                </div>
              )}

              {activeTab === 'care' && (
                <div className="space-y-6">
                  <div>
                    <h4 className="font-semibold text-lg mb-3">Daily Routine</h4>
                    <div className="bg-gray-50 rounded-xl p-4">
                      {selectedPatient.dailyRoutine.map((item, i) => (
                        <div key={i} className="flex items-center gap-3 py-2 border-b border-gray-200 last:border-0">
                          <span className="w-2 h-2 bg-purple-500 rounded-full"></span>
                          <span>{item}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold text-lg mb-3">Preferences</h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedPatient.preferences.map((pref, i) => (
                        <span key={i} className="px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm">{pref}</span>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="font-semibold text-lg mb-3">Allergies</h4>
                    <div className="flex flex-wrap gap-2">
                      {selectedPatient.allergies.map((allergy, i) => (
                        <span key={i} className="px-4 py-2 bg-red-100 text-red-700 rounded-full text-sm">{allergy}</span>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Add Patient Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b flex justify-between items-center">
              <h2 className="text-2xl font-bold">Add New Patient</h2>
              <button type="button" onClick={() => setShowAddModal(false)} className="p-2 hover:bg-gray-100 rounded-lg" aria-label="Close">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
            </div>
            <form className="p-6 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="firstName" className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                  <input id="firstName" type="text" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
                </div>
                <div>
                  <label htmlFor="lastName" className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                  <input id="lastName" type="text" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label htmlFor="age" className="block text-sm font-medium text-gray-700 mb-1">Age</label>
                  <input id="age" type="number" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
                </div>
                <div>
                  <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-1">Gender</label>
                  <select id="gender" className="w-full px-4 py-2 border border-gray-300 rounded-lg">
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                  </select>
                </div>
              </div>
              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-1">Phone</label>
                <input id="phone" type="tel" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
              </div>
              <div>
                <label htmlFor="caregiver" className="block text-sm font-medium text-gray-700 mb-1">Primary Caregiver</label>
                <input id="caregiver" type="text" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
              </div>
              <div className="flex space-x-3 pt-4">
                <button type="button" onClick={() => setShowAddModal(false)} className="flex-1 py-3 border-2 border-gray-300 text-gray-600 rounded-xl font-semibold hover:bg-gray-50">Cancel</button>
                <button type="submit" className="flex-1 py-3 bg-purple-600 text-white rounded-xl font-semibold hover:bg-purple-700">Add Patient</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
