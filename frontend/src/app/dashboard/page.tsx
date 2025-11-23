'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'

interface PatientStats {
  total: number
  none: number
  preclinical: number
  mci: number
  mild: number
  moderate: number
  severe: number
  active: number
  monitoring: number
  critical: number
  youngOnset: number
}

export default function DashboardPage() {
  const [selectedFilter, setSelectedFilter] = useState('all')
  const [stats, setStats] = useState<PatientStats>({
    total: 200,
    none: 50,
    preclinical: 15,
    mci: 30,
    mild: 40,
    moderate: 35,
    severe: 30,
    active: 105,
    monitoring: 65,
    critical: 30,
    youngOnset: 24
  })

  const recentActivities = [
    { time: '9:00 AM', activity: 'New patient assessment completed - P125', type: 'assessment', patient: 'Robert Martinez' },
    { time: '10:30 AM', activity: 'Critical alert: P089 cognitive score dropped', type: 'alert', patient: 'Margaret Chen' },
    { time: '11:00 AM', activity: 'Treatment plan updated - P042', type: 'treatment', patient: 'James Anderson' },
    { time: '2:00 PM', activity: 'Memory test completed - P156', type: 'test', patient: 'Dorothy Williams' },
    { time: '3:30 PM', activity: 'New patient registered - P201', type: 'new', patient: 'Helen Martinez' }
  ]

  const upcomingAppointments = [
    { date: 'Today', time: '4:00 PM', patient: 'Eleanor Thompson', type: 'Follow-up', level: 'MCI' },
    { date: 'Today', time: '5:30 PM', patient: 'Patricia Brown', type: 'Care Review', level: 'Severe' },
    { date: 'Tomorrow', time: '9:00 AM', patient: 'William Johnson', type: 'Annual Screening', level: 'None' },
    { date: 'Tomorrow', time: '11:00 AM', patient: 'Sandra Miller', type: 'Therapy Session', level: 'None' },
    { date: 'Wed', time: '10:00 AM', patient: 'George Wilson', type: 'Neurology Consult', level: 'None' }
  ]

  const cognitiveMetrics = [
    { name: 'Average Memory Score', score: 68, change: '+2.3%', color: '#8B5CF6' },
    { name: 'Average Attention Score', score: 74, change: '+1.8%', color: '#3B82F6' },
    { name: 'Average Language Score', score: 71, change: '+0.5%', color: '#10B981' },
    { name: 'Average Executive Function', score: 62, change: '-0.8%', color: '#F97316' },
    { name: 'Average Visuospatial', score: 69, change: '+1.2%', color: '#EC4899' }
  ]

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

  return (
    <div className="min-h-screen bg-gray-50 pt-20">
      {/* Header */}
      <div className="bg-gradient-to-r from-purple-700 via-indigo-700 to-blue-700 text-white py-8">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold">Dashboard</h1>
              <p className="text-purple-100 mt-1">Patient overview and cognitive health statistics</p>
            </div>
            <div className="flex items-center gap-3">
              <Link href="/patients" className="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-lg transition font-medium">
                View All Patients
              </Link>
              <Link href="/detection" className="px-4 py-2 bg-white text-purple-700 rounded-lg font-semibold hover:bg-purple-50 transition">
                New Assessment
              </Link>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Filter Tabs */}
        <div className="bg-white rounded-xl shadow-sm p-2 mb-8 flex flex-wrap gap-2">
          {[
            { id: 'all', label: 'All Patients', count: stats.total },
            { id: 'none', label: 'No Alzheimer\'s', count: stats.none },
            { id: 'preclinical', label: 'Pre-clinical', count: stats.preclinical },
            { id: 'mci', label: 'MCI', count: stats.mci },
            { id: 'mild', label: 'Mild', count: stats.mild },
            { id: 'moderate', label: 'Moderate', count: stats.moderate },
            { id: 'severe', label: 'Severe', count: stats.severe }
          ].map(filter => (
            <button
              key={filter.id}
              type="button"
              onClick={() => setSelectedFilter(filter.id)}
              className={`px-4 py-2 rounded-lg font-medium transition flex items-center gap-2 ${
                selectedFilter === filter.id
                  ? 'bg-purple-600 text-white'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              {filter.label}
              <span className={`px-2 py-0.5 rounded-full text-xs ${
                selectedFilter === filter.id
                  ? 'bg-white/20 text-white'
                  : 'bg-gray-200 text-gray-600'
              }`}>
                {filter.count}
              </span>
            </button>
          ))}
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-purple-500">
            <div className="text-3xl font-bold text-purple-600">{stats.total}</div>
            <div className="text-gray-600 text-sm">Total Patients</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-green-500">
            <div className="text-3xl font-bold text-green-600">{stats.active}</div>
            <div className="text-gray-600 text-sm">Active</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-yellow-500">
            <div className="text-3xl font-bold text-yellow-600">{stats.monitoring}</div>
            <div className="text-gray-600 text-sm">Monitoring</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-red-500">
            <div className="text-3xl font-bold text-red-600">{stats.critical}</div>
            <div className="text-gray-600 text-sm">Critical</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-orange-500">
            <div className="text-3xl font-bold text-orange-600">{stats.youngOnset}</div>
            <div className="text-gray-600 text-sm">Young-Onset</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-sm border-l-4 border-blue-500">
            <div className="text-3xl font-bold text-blue-600">{stats.none}</div>
            <div className="text-gray-600 text-sm">Non-Alzheimer&apos;s</div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Patient Distribution Chart */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-6">Patient Distribution by Stage</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {[
                  { label: 'No Alzheimer\'s', count: stats.none, color: 'bg-green-500', pct: Math.round(stats.none / stats.total * 100) },
                  { label: 'Pre-clinical', count: stats.preclinical, color: 'bg-blue-500', pct: Math.round(stats.preclinical / stats.total * 100) },
                  { label: 'MCI', count: stats.mci, color: 'bg-yellow-500', pct: Math.round(stats.mci / stats.total * 100) },
                  { label: 'Mild', count: stats.mild, color: 'bg-orange-500', pct: Math.round(stats.mild / stats.total * 100) },
                  { label: 'Moderate', count: stats.moderate, color: 'bg-red-500', pct: Math.round(stats.moderate / stats.total * 100) },
                  { label: 'Severe', count: stats.severe, color: 'bg-purple-500', pct: Math.round(stats.severe / stats.total * 100) }
                ].map((item, i) => (
                  <div key={i} className="bg-gray-50 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-medium text-sm">{item.label}</span>
                      <span className="text-2xl font-bold">{item.count}</span>
                    </div>
                    <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <div className={`h-full ${item.color} rounded-full`} style={{ width: `${item.pct}%` }} />
                    </div>
                    <div className="text-right text-xs text-gray-500 mt-1">{item.pct}%</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Cognitive Metrics */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-6">Average Cognitive Scores (All Patients)</h2>
              <div className="space-y-4">
                {cognitiveMetrics.map((metric, i) => (
                  <div key={i} className="flex items-center">
                    <span className="w-48 font-medium text-sm">{metric.name}</span>
                    <div className="flex-1 mx-4">
                      <div className="h-4 bg-gray-200 rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full transition-all duration-500"
                          style={{ width: `${metric.score}%`, backgroundColor: metric.color }}
                        />
                      </div>
                    </div>
                    <span className="w-12 text-right font-bold">{metric.score}</span>
                    <span className={`w-16 text-right text-sm ${metric.change.startsWith('+') ? 'text-green-600' : 'text-red-600'}`}>
                      {metric.change}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Activities */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-bold">Recent Activities</h2>
                <Link href="/patients" className="text-purple-600 hover:text-purple-700 font-medium text-sm">View All</Link>
              </div>
              <div className="space-y-3">
                {recentActivities.map((activity, i) => (
                  <div key={i} className="flex items-center p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition">
                    <span className="text-2xl mr-4">
                      {activity.type === 'assessment' ? '📋' :
                       activity.type === 'alert' ? '🚨' :
                       activity.type === 'treatment' ? '💊' :
                       activity.type === 'test' ? '🧠' : '👤'}
                    </span>
                    <div className="flex-1">
                      <p className="font-medium">{activity.activity}</p>
                      <p className="text-sm text-gray-500">{activity.patient} • {activity.time}</p>
                    </div>
                    {activity.type === 'alert' && (
                      <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-medium">Urgent</span>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* Quick Actions */}
            <div className="grid md:grid-cols-4 gap-4">
              <Link href="/detection" className="bg-purple-100 hover:bg-purple-200 rounded-xl p-6 text-center transition">
                <span className="text-3xl block mb-2">🧠</span>
                <span className="font-semibold text-purple-800">New Assessment</span>
              </Link>
              <Link href="/patients" className="bg-blue-100 hover:bg-blue-200 rounded-xl p-6 text-center transition">
                <span className="text-3xl block mb-2">👥</span>
                <span className="font-semibold text-blue-800">All Patients</span>
              </Link>
              <Link href="/cognitive-tests" className="bg-green-100 hover:bg-green-200 rounded-xl p-6 text-center transition">
                <span className="text-3xl block mb-2">📊</span>
                <span className="font-semibold text-green-800">Cognitive Tests</span>
              </Link>
              <Link href="/memory-games" className="bg-orange-100 hover:bg-orange-200 rounded-xl p-6 text-center transition">
                <span className="text-3xl block mb-2">🎮</span>
                <span className="font-semibold text-orange-800">Memory Games</span>
              </Link>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Upcoming Appointments */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-4">Upcoming Appointments</h2>
              <div className="space-y-3">
                {upcomingAppointments.map((appt, i) => (
                  <div key={i} className="flex items-start p-3 border-l-4 border-purple-500 bg-purple-50 rounded-r-lg">
                    <div className="flex-1">
                      <p className="font-medium">{appt.patient}</p>
                      <p className="text-sm text-gray-600">{appt.type}</p>
                      <p className="text-xs text-gray-500">{appt.date}, {appt.time}</p>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getLevelColor(appt.level)}`}>
                      {appt.level}
                    </span>
                  </div>
                ))}
              </div>
              <button type="button" className="w-full mt-4 py-2 text-purple-600 font-semibold hover:bg-purple-50 rounded-lg transition">
                View Calendar →
              </button>
            </div>

            {/* Critical Patients Alert */}
            <div className="bg-red-50 border border-red-200 rounded-2xl p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl">🚨</span>
                <h2 className="text-xl font-bold text-red-800">Critical Patients</h2>
              </div>
              <p className="text-red-700 mb-4">{stats.critical} patients require immediate attention</p>
              <Link href="/patients?status=Critical" className="block w-full py-2 bg-red-600 text-white text-center rounded-lg font-semibold hover:bg-red-700 transition">
                View Critical Patients
              </Link>
            </div>

            {/* Young-Onset Cases */}
            <div className="bg-orange-50 border border-orange-200 rounded-2xl p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl">👤</span>
                <h2 className="text-xl font-bold text-orange-800">Young-Onset Cases</h2>
              </div>
              <p className="text-orange-700 mb-2">{stats.youngOnset} patients diagnosed before age 65</p>
              <p className="text-sm text-orange-600">These patients require specialized care protocols.</p>
            </div>

            {/* System Status */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-4">System Status</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">AI Detection</span>
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">Online</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Database</span>
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">Healthy</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Last Sync</span>
                  <span className="text-gray-800 font-semibold">2 min ago</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Active Users</span>
                  <span className="text-gray-800 font-semibold">12</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
