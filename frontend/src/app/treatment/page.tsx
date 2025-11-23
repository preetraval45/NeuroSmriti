'use client'

import { useState } from 'react'

export default function TreatmentPage() {
  const [selectedPlan, setSelectedPlan] = useState('medication')

  const medications = [
    {
      name: 'Donepezil (Aricept)',
      type: 'Cholinesterase Inhibitor',
      dosage: '10mg daily',
      schedule: 'Evening',
      status: 'active',
      nextRefill: '15 days',
      effectiveness: 'Good response observed'
    },
    {
      name: 'Memantine (Namenda)',
      type: 'NMDA Receptor Antagonist',
      dosage: '10mg twice daily',
      schedule: 'Morning & Evening',
      status: 'active',
      nextRefill: '22 days',
      effectiveness: 'Stable cognitive function'
    },
    {
      name: 'Vitamin E',
      type: 'Antioxidant Supplement',
      dosage: '2000 IU daily',
      schedule: 'Morning',
      status: 'active',
      nextRefill: '30 days',
      effectiveness: 'Supportive'
    }
  ]

  const therapies = [
    {
      name: 'Cognitive Behavioral Therapy',
      frequency: 'Weekly',
      nextSession: 'Tomorrow at 2 PM',
      provider: 'Dr. Sarah Johnson',
      progress: 75
    },
    {
      name: 'Occupational Therapy',
      frequency: 'Twice weekly',
      nextSession: 'Thursday at 10 AM',
      provider: 'Mike Thompson, OT',
      progress: 60
    },
    {
      name: 'Speech Therapy',
      frequency: 'Weekly',
      nextSession: 'Friday at 3 PM',
      provider: 'Lisa Chen, SLP',
      progress: 80
    },
    {
      name: 'Music Therapy',
      frequency: 'Weekly',
      nextSession: 'Wednesday at 11 AM',
      provider: 'David Park, MT-BC',
      progress: 90
    }
  ]

  const lifestyleRecommendations = [
    {
      category: 'Diet',
      icon: '🥗',
      recommendations: [
        'Follow Mediterranean diet rich in omega-3s',
        'Eat leafy greens and berries daily',
        'Limit processed foods and sugar',
        'Stay hydrated with 8 glasses of water'
      ]
    },
    {
      category: 'Exercise',
      icon: '🚶',
      recommendations: [
        '30 minutes of walking daily',
        'Gentle yoga or tai chi twice a week',
        'Balance exercises to prevent falls',
        'Stretching routine each morning'
      ]
    },
    {
      category: 'Sleep',
      icon: '😴',
      recommendations: [
        'Maintain consistent sleep schedule',
        'Aim for 7-8 hours of quality sleep',
        'Avoid screens 1 hour before bed',
        'Create calm, dark sleeping environment'
      ]
    },
    {
      category: 'Social',
      icon: '👥',
      recommendations: [
        'Daily conversations with family',
        'Weekly social activities or groups',
        'Regular video calls with distant family',
        'Participate in community events'
      ]
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-green-600 to-teal-700 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Treatment Plans</h1>
            <p className="text-xl text-green-100">
              Personalized care plans designed to slow progression and improve quality of life
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          {/* Treatment Navigation */}
          <div className="flex flex-wrap gap-4 mb-8">
            {[
              { id: 'medication', label: 'Medications', icon: '💊' },
              { id: 'therapy', label: 'Therapies', icon: '🧠' },
              { id: 'lifestyle', label: 'Lifestyle', icon: '🌿' },
              { id: 'clinical-trials', label: 'Clinical Trials', icon: '🔬' }
            ].map(tab => (
              <button
                key={tab.id}
                type="button"
                onClick={() => setSelectedPlan(tab.id)}
                className={`px-6 py-3 rounded-xl font-semibold transition flex items-center ${
                  selectedPlan === tab.id
                    ? 'bg-green-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-gray-100 shadow'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>

          {/* Medication Plan */}
          {selectedPlan === 'medication' && (
            <div className="space-y-6">
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-2xl font-bold">Current Medications</h2>
                  <button type="button" className="px-4 py-2 bg-green-100 text-green-700 rounded-lg font-semibold hover:bg-green-200 transition">
                    + Add Medication
                  </button>
                </div>

                <div className="space-y-4">
                  {medications.map((med, i) => (
                    <div key={i} className="border-2 border-gray-100 rounded-xl p-6 hover:border-green-200 transition">
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="text-xl font-bold text-gray-800">{med.name}</h3>
                          <p className="text-green-600">{med.type}</p>
                        </div>
                        <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                          Active
                        </span>
                      </div>
                      <div className="grid md:grid-cols-4 gap-4 mt-4">
                        <div>
                          <p className="text-sm text-gray-500">Dosage</p>
                          <p className="font-semibold">{med.dosage}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Schedule</p>
                          <p className="font-semibold">{med.schedule}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Next Refill</p>
                          <p className="font-semibold">{med.nextRefill}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-500">Effectiveness</p>
                          <p className="font-semibold text-green-600">{med.effectiveness}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div className="bg-white rounded-2xl shadow-lg p-6">
                  <h3 className="text-xl font-bold mb-4">Medication Adherence</h3>
                  <div className="text-center mb-4">
                    <div className="text-5xl font-bold text-green-600">94%</div>
                    <p className="text-gray-600">This Month</p>
                  </div>
                  <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
                    <div className="h-full bg-green-500 rounded-full" style={{ width: '94%' }} />
                  </div>
                  <p className="text-sm text-gray-500 mt-2">Great job! Keep up the consistency.</p>
                </div>

                <div className="bg-white rounded-2xl shadow-lg p-6">
                  <h3 className="text-xl font-bold mb-4">Today&apos;s Schedule</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
                      <div className="flex items-center">
                        <span className="text-xl mr-3">☀️</span>
                        <span>Morning medications</span>
                      </div>
                      <span className="text-green-600">✓ Done</span>
                    </div>
                    <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg">
                      <div className="flex items-center">
                        <span className="text-xl mr-3">🌙</span>
                        <span>Evening medications</span>
                      </div>
                      <span className="text-yellow-600">8:00 PM</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Therapy Plan */}
          {selectedPlan === 'therapy' && (
            <div className="space-y-6">
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <h2 className="text-2xl font-bold mb-6">Therapy Sessions</h2>
                <div className="grid md:grid-cols-2 gap-6">
                  {therapies.map((therapy, i) => (
                    <div key={i} className="border-2 border-gray-100 rounded-xl p-6 hover:border-teal-200 transition">
                      <h3 className="text-xl font-bold mb-2">{therapy.name}</h3>
                      <p className="text-gray-600 mb-4">with {therapy.provider}</p>
                      <div className="space-y-2 mb-4">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Frequency</span>
                          <span className="font-semibold">{therapy.frequency}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-500">Next Session</span>
                          <span className="font-semibold text-teal-600">{therapy.nextSession}</span>
                        </div>
                      </div>
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span className="text-gray-500">Progress</span>
                          <span className="font-semibold">{therapy.progress}%</span>
                        </div>
                        <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-teal-500 rounded-full"
                            style={{ width: `${therapy.progress}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-gradient-to-r from-teal-100 to-green-100 rounded-2xl p-8">
                <h3 className="text-xl font-bold mb-4">Recommended Additional Therapies</h3>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="bg-white rounded-xl p-4">
                    <span className="text-3xl">🎨</span>
                    <h4 className="font-bold mt-2">Art Therapy</h4>
                    <p className="text-sm text-gray-600">Express emotions and memories through creative activities</p>
                  </div>
                  <div className="bg-white rounded-xl p-4">
                    <span className="text-3xl">🐕</span>
                    <h4 className="font-bold mt-2">Pet Therapy</h4>
                    <p className="text-sm text-gray-600">Animal-assisted therapy for emotional support</p>
                  </div>
                  <div className="bg-white rounded-xl p-4">
                    <span className="text-3xl">🌳</span>
                    <h4 className="font-bold mt-2">Nature Therapy</h4>
                    <p className="text-sm text-gray-600">Outdoor activities and garden therapy</p>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Lifestyle Plan */}
          {selectedPlan === 'lifestyle' && (
            <div className="space-y-6">
              <div className="grid md:grid-cols-2 gap-6">
                {lifestyleRecommendations.map((category, i) => (
                  <div key={i} className="bg-white rounded-2xl shadow-lg p-6">
                    <div className="flex items-center mb-4">
                      <span className="text-4xl mr-4">{category.icon}</span>
                      <h3 className="text-xl font-bold">{category.category}</h3>
                    </div>
                    <ul className="space-y-3">
                      {category.recommendations.map((rec, j) => (
                        <li key={j} className="flex items-start">
                          <span className="text-green-500 mr-2 mt-1">✓</span>
                          <span className="text-gray-700">{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>

              <div className="bg-white rounded-2xl shadow-lg p-8">
                <h3 className="text-xl font-bold mb-6">Weekly Activity Tracker</h3>
                <div className="grid grid-cols-7 gap-2 mb-4">
                  {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(day => (
                    <div key={day} className="text-center text-sm font-semibold text-gray-500">
                      {day}
                    </div>
                  ))}
                </div>
                <div className="grid grid-cols-7 gap-2">
                  {[85, 90, 75, 95, 80, 60, 70].map((value, i) => (
                    <div
                      key={i}
                      className={`h-12 rounded-lg flex items-center justify-center text-white font-bold ${
                        value >= 80 ? 'bg-green-500' :
                        value >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                    >
                      {value}%
                    </div>
                  ))}
                </div>
                <p className="text-sm text-gray-500 mt-4 text-center">
                  Average daily goal completion: 79%
                </p>
              </div>
            </div>
          )}

          {/* Clinical Trials */}
          {selectedPlan === 'clinical-trials' && (
            <div className="space-y-6">
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <h2 className="text-2xl font-bold mb-6">Available Clinical Trials</h2>
                <div className="space-y-4">
                  {[
                    {
                      name: 'CLARITY-AD Extension Study',
                      sponsor: 'Biogen/Eisai',
                      phase: 'Phase 3',
                      focus: 'Lecanemab for early Alzheimer\'s',
                      eligibility: 'High match',
                      location: 'Charlotte, NC'
                    },
                    {
                      name: 'AHEAD Study',
                      sponsor: 'Eli Lilly',
                      phase: 'Phase 3',
                      focus: 'Prevention in high-risk individuals',
                      eligibility: 'Medium match',
                      location: 'Durham, NC'
                    },
                    {
                      name: 'DIAN-TU Prevention Trial',
                      sponsor: 'Washington University',
                      phase: 'Phase 2/3',
                      focus: 'Dominantly inherited Alzheimer\'s',
                      eligibility: 'Requires genetic testing',
                      location: 'Multiple sites'
                    }
                  ].map((trial, i) => (
                    <div key={i} className="border-2 border-gray-100 rounded-xl p-6 hover:border-blue-200 transition">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h3 className="text-xl font-bold">{trial.name}</h3>
                          <p className="text-gray-600">{trial.sponsor} • {trial.phase}</p>
                        </div>
                        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                          trial.eligibility.includes('High') ? 'bg-green-100 text-green-700' :
                          trial.eligibility.includes('Medium') ? 'bg-yellow-100 text-yellow-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {trial.eligibility}
                        </span>
                      </div>
                      <p className="text-gray-700 mb-2"><strong>Focus:</strong> {trial.focus}</p>
                      <p className="text-gray-700 mb-4"><strong>Location:</strong> {trial.location}</p>
                      <button type="button" className="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition">
                        Learn More
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-gradient-to-r from-blue-100 to-purple-100 rounded-2xl p-8">
                <div className="max-w-2xl mx-auto text-center">
                  <h3 className="text-xl font-bold mb-4">Interested in Clinical Trials?</h3>
                  <p className="text-gray-700 mb-6">
                    Our team can help match you with appropriate trials and guide you through the enrollment process.
                  </p>
                  <button type="button" className="px-8 py-3 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700 transition">
                    Schedule Consultation
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
