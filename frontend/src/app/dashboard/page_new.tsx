'use client'

import { useState } from 'react'
import Link from 'next/link'

interface ResearchMetrics {
  datasetSamples: number
  trainingEpochs: number
  validationFolds: number
  modelVersions: number
  activeExperiments: number
  completedTests: number
}

export default function DashboardPage() {
  const [selectedView, setSelectedView] = useState('overview')
  const [metrics, setMetrics] = useState<ResearchMetrics>({
    datasetSamples: 0,
    trainingEpochs: 0,
    validationFolds: 10,
    modelVersions: 0,
    activeExperiments: 0,
    completedTests: 0
  })

  const researchDatasets = [
    { name: 'ADNI', description: 'Alzheimer\'s Disease Neuroimaging Initiative', samples: 'Brain MRI scans', color: 'indigo' },
    { name: 'OASIS', description: 'Open Access Series of Imaging Studies', samples: 'Structural MRI data', color: 'purple' },
    { name: 'NACC', description: 'National Alzheimer\'s Coordinating Center', samples: 'Clinical assessments', color: 'blue' },
    { name: 'DementiaBank', description: 'Speech and language database', samples: 'Audio recordings', color: 'green' }
  ]

  const researchFeatures = [
    { name: 'Neuroimaging Analysis', status: 'Demo', description: 'MRI/CT scan processing with CNN', icon: '🧠', route: '/detection' },
    { name: 'Cognitive Testing', status: 'Demo', description: 'Memory and cognition assessments', icon: '📝', route: '/cognitive-tests' },
    { name: 'Speech Analysis', status: 'Experimental', description: 'Voice pattern detection', icon: '🎤', route: '/speech-analysis' },
    { name: 'Eye Tracking', status: 'Experimental', description: 'Gaze pattern analysis', icon: '👁️', route: '/eye-tracking' },
    { name: 'Digital Biomarkers', status: 'Experimental', description: 'Device usage patterns', icon: '📱', route: '/digital-biomarkers' }
  ]

  const modelMetrics = [
    { name: 'Sensitivity (Recall)', value: 'Training', target: '≥ 85%', description: 'True Positive Rate', color: 'indigo' },
    { name: 'Specificity', value: 'Training', target: '≥ 80%', description: 'True Negative Rate', color: 'purple' },
    { name: 'AUC-ROC', value: 'Training', target: '≥ 0.85', description: 'Discrimination ability', color: 'blue' },
    { name: 'Cohen\'s Kappa', value: 'Training', target: '≥ 0.70', description: 'Inter-rater reliability', color: 'green' }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-indigo-700 via-purple-700 to-blue-700 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="inline-block px-4 py-2 bg-amber-500 text-amber-900 rounded-full text-sm font-bold mb-4">
              RESEARCH PROTOTYPE - NOT FOR CLINICAL USE
            </div>
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Research Dashboard</h1>
            <p className="text-xl text-indigo-100 mb-2">
              AI-Powered Cognitive Decline Detection Platform
            </p>
            <p className="text-sm text-indigo-200 max-w-3xl">
              This dashboard provides an overview of our research tools, datasets, and experimental features.
              All components are for research and educational purposes only.
            </p>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {/* Critical Disclaimer */}
        <div className="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-300 rounded-2xl p-6 mb-8">
          <div className="flex items-start gap-4">
            <span className="text-3xl">⚠️</span>
            <div className="flex-1">
              <h2 className="text-xl font-bold text-amber-900 mb-2">Not for Clinical Diagnosis</h2>
              <p className="text-amber-800 mb-3">
                This is a research prototype exploring AI techniques for early cognitive decline detection.
                <strong> It cannot diagnose Alzheimer's disease or any medical condition.</strong> All results are
                for research demonstration purposes only. Always seek professional medical evaluation from qualified healthcare providers.
              </p>
              <div className="flex flex-wrap gap-3">
                <a
                  href="tel:+18002723900"
                  className="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition text-sm"
                >
                  Alzheimer's Association: 1-800-272-3900
                </a>
                <a
                  href="https://www.alz.org"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block px-4 py-2 border-2 border-blue-600 text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition text-sm"
                >
                  Professional Resources
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Research Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
          <div className="bg-white rounded-xl p-5 shadow-md border-l-4 border-indigo-500">
            <div className="text-3xl font-bold text-indigo-600">{metrics.validationFolds}</div>
            <div className="text-gray-600 text-sm font-semibold">CV Folds</div>
            <div className="text-xs text-gray-500 mt-1">Nested Cross-Val</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-md border-l-4 border-purple-500">
            <div className="text-3xl font-bold text-purple-600">4</div>
            <div className="text-gray-600 text-sm font-semibold">Datasets</div>
            <div className="text-xs text-gray-500 mt-1">Medical Sources</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-md border-l-4 border-blue-500">
            <div className="text-3xl font-bold text-blue-600">5</div>
            <div className="text-gray-600 text-sm font-semibold">Modalities</div>
            <div className="text-xs text-gray-500 mt-1">Analysis Tools</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-md border-l-4 border-green-500">
            <div className="text-2xl font-bold text-green-600">GNN</div>
            <div className="text-gray-600 text-sm font-semibold">Architecture</div>
            <div className="text-xs text-gray-500 mt-1">Graph Neural Net</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-md border-l-4 border-orange-500">
            <div className="text-2xl font-bold text-orange-600">Training</div>
            <div className="text-gray-600 text-sm font-semibold">Status</div>
            <div className="text-xs text-gray-500 mt-1">In Development</div>
          </div>
          <div className="bg-white rounded-xl p-5 shadow-md border-l-4 border-pink-500">
            <div className="text-2xl font-bold text-pink-600">Demo</div>
            <div className="text-gray-600 text-sm font-semibold">Mode</div>
            <div className="text-xs text-gray-500 mt-1">Research Only</div>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Research Datasets */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border-t-4 border-indigo-500">
              <h2 className="text-2xl font-bold mb-4 text-gray-900">Research Datasets</h2>
              <p className="text-sm text-gray-600 mb-6">
                Our platform integrates with established medical research datasets for model training and validation.
              </p>
              <div className="grid md:grid-cols-2 gap-4">
                {researchDatasets.map((dataset, i) => (
                  <div key={i} className={`p-5 border-2 border-${dataset.color}-200 bg-${dataset.color}-50 rounded-xl hover:shadow-md transition`}>
                    <h3 className="font-bold text-lg text-gray-900 mb-1">{dataset.name}</h3>
                    <p className="text-sm text-gray-700 mb-2">{dataset.description}</p>
                    <p className="text-xs text-gray-600">
                      <strong>Data Type:</strong> {dataset.samples}
                    </p>
                  </div>
                ))}
              </div>
              <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <p className="text-sm text-blue-900">
                  <strong>Note:</strong> Access to these datasets requires institutional approval and data use agreements.
                  See our <Link href="/about" className="underline font-semibold">research documentation</Link> for details.
                </p>
              </div>
            </div>

            {/* Research Features */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border-t-4 border-purple-500">
              <h2 className="text-2xl font-bold mb-4 text-gray-900">Multimodal Analysis Tools</h2>
              <p className="text-sm text-gray-600 mb-6">
                Experimental AI tools for analyzing different aspects of cognitive function.
              </p>
              <div className="space-y-3">
                {researchFeatures.map((feature, i) => (
                  <Link
                    key={i}
                    href={feature.route}
                    className="block p-4 border-2 border-gray-200 rounded-xl hover:border-indigo-400 hover:bg-indigo-50 transition group"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-4">
                        <span className="text-3xl">{feature.icon}</span>
                        <div>
                          <h3 className="font-bold text-gray-900 group-hover:text-indigo-700">{feature.name}</h3>
                          <p className="text-sm text-gray-600">{feature.description}</p>
                        </div>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                        feature.status === 'Demo' ? 'bg-green-100 text-green-800' : 'bg-amber-100 text-amber-800'
                      }`}>
                        {feature.status}
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            </div>

            {/* Model Performance Targets */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border-t-4 border-blue-500">
              <h2 className="text-2xl font-bold mb-4 text-gray-900">Clinical Validation Metrics</h2>
              <p className="text-sm text-gray-600 mb-6">
                Target performance metrics for clinical-grade AI systems based on medical research standards.
              </p>
              <div className="space-y-4">
                {modelMetrics.map((metric, i) => (
                  <div key={i} className="p-4 bg-gray-50 rounded-xl border border-gray-200">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-bold text-gray-900">{metric.name}</h3>
                      <span className="px-3 py-1 bg-amber-100 text-amber-800 rounded-full text-xs font-bold">
                        {metric.value}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-1">{metric.description}</p>
                    <p className="text-xs text-gray-500">
                      <strong>Target:</strong> {metric.target}
                    </p>
                  </div>
                ))}
              </div>
              <div className="mt-6 p-4 bg-indigo-50 rounded-lg border border-indigo-200">
                <p className="text-sm text-indigo-900">
                  <strong>Validation Method:</strong> 10-fold Nested Cross-Validation with 5-fold inner loop for hyperparameter tuning.
                  Wilson score confidence intervals (95% CI) for statistical reliability.
                </p>
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-4 text-gray-900">Explore Tools</h2>
              <div className="space-y-3">
                <Link href="/detection" className="block p-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl hover:shadow-lg transition">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">🧠</span>
                    <div>
                      <p className="font-semibold">Detection Platform</p>
                      <p className="text-xs text-indigo-100">Multimodal analysis tools</p>
                    </div>
                  </div>
                </Link>
                <Link href="/about" className="block p-4 border-2 border-gray-300 rounded-xl hover:border-indigo-500 hover:bg-indigo-50 transition">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">📚</span>
                    <div>
                      <p className="font-semibold text-gray-900">Research Overview</p>
                      <p className="text-xs text-gray-600">Learn about our approach</p>
                    </div>
                  </div>
                </Link>
                <Link href="/contact" className="block p-4 border-2 border-gray-300 rounded-xl hover:border-blue-500 hover:bg-blue-50 transition">
                  <div className="flex items-center gap-3">
                    <span className="text-2xl">✉️</span>
                    <div>
                      <p className="font-semibold text-gray-900">Research Inquiries</p>
                      <p className="text-xs text-gray-600">Collaborate with us</p>
                    </div>
                  </div>
                </Link>
              </div>
            </div>

            {/* Technology Stack */}
            <div className="bg-gradient-to-br from-purple-50 to-indigo-50 rounded-2xl shadow-lg p-6 border-2 border-purple-200">
              <h2 className="text-xl font-bold mb-4 text-gray-900">Technology Stack</h2>
              <div className="space-y-3 text-sm">
                <div>
                  <p className="font-semibold text-gray-900">Deep Learning</p>
                  <p className="text-gray-600">PyTorch, TensorFlow, Graph Neural Networks</p>
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Imaging</p>
                  <p className="text-gray-600">3D CNN, ResNet, DenseNet architectures</p>
                </div>
                <div>
                  <p className="font-semibold text-gray-900">NLP</p>
                  <p className="text-gray-600">Transformers, BERT for speech analysis</p>
                </div>
                <div>
                  <p className="font-semibold text-gray-900">Validation</p>
                  <p className="text-gray-600">Nested CV, Bootstrap, Wilson CI</p>
                </div>
              </div>
            </div>

            {/* Medical Resources */}
            <div className="bg-blue-50 border-2 border-blue-300 rounded-2xl p-6">
              <div className="flex items-center gap-3 mb-4">
                <span className="text-2xl">🏥</span>
                <h2 className="text-xl font-bold text-blue-900">Medical Resources</h2>
              </div>
              <p className="text-sm text-blue-800 mb-4">
                For clinical evaluation, diagnosis, or medical advice, please contact qualified healthcare professionals.
              </p>
              <div className="space-y-2">
                <a
                  href="tel:+18002723900"
                  className="block w-full py-3 bg-blue-600 text-white text-center rounded-lg font-semibold hover:bg-blue-700 transition"
                >
                  Call 1-800-272-3900
                </a>
                <a
                  href="https://www.alz.org"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="block w-full py-3 border-2 border-blue-600 text-blue-600 text-center rounded-lg font-semibold hover:bg-blue-50 transition"
                >
                  Alzheimer's Association
                </a>
              </div>
            </div>

            {/* System Status */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-bold mb-4 text-gray-900">Platform Status</h2>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Frontend</span>
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">Online</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Backend API</span>
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">Active</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">Database</span>
                  <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">Connected</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-700">ML Models</span>
                  <span className="px-3 py-1 bg-amber-100 text-amber-700 rounded-full text-sm font-semibold">Training</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
