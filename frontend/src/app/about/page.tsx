import Link from 'next/link'

export default function AboutPage() {
  const researchAreas = [
    {
      title: 'AI-Powered Cognitive Assessment',
      description: 'Developing deep learning models for early detection of cognitive decline using multimodal data including MRI scans, cognitive test results, and speech patterns.',
      icon: '🧠',
      color: 'from-indigo-500 to-purple-600'
    },
    {
      title: 'Memory Graph Neural Networks',
      description: 'Novel GNN architectures that model patient memory networks to predict cognitive deterioration and personalize intervention strategies.',
      icon: '🔬',
      color: 'from-blue-500 to-cyan-600'
    },
    {
      title: 'Clinical Validation Studies',
      description: 'Conducting rigorous nested cross-validation studies with real patient data from ADNI, OASIS, and NACC datasets to ensure clinical reliability.',
      icon: '📊',
      color: 'from-green-500 to-emerald-600'
    },
    {
      title: 'Digital Biomarker Research',
      description: 'Investigating eye-tracking patterns, speech analysis, and keystroke dynamics as non-invasive biomarkers for Alzheimer\'s progression.',
      icon: '💻',
      color: 'from-orange-500 to-red-600'
    }
  ]

  const technicalApproach = [
    {
      name: 'Dataset Integration',
      details: 'ADNI, OASIS, NACC, DementiaBank',
      description: 'Multi-source real clinical data with 10-fold nested cross-validation'
    },
    {
      name: 'Model Architecture',
      details: 'Graph Neural Networks + Transformers',
      description: 'Memory GNN with multimodal fusion for cognitive state prediction'
    },
    {
      name: 'Validation Metrics',
      details: 'Sensitivity, Specificity, AUC-ROC',
      description: 'Clinical-grade evaluation with 95% confidence intervals'
    },
    {
      name: 'Compliance Standards',
      details: 'HIPAA, FDA Guidelines',
      description: 'Privacy-preserving ML with regulatory awareness'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-indigo-900 via-purple-900 to-blue-900 text-white py-24 overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500 rounded-full filter blur-3xl opacity-20"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500 rounded-full filter blur-3xl opacity-20"></div>

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center px-4 py-2 bg-amber-500/20 border border-amber-400/30 rounded-full text-sm mb-8 backdrop-blur-sm">
              <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
              Research Prototype - Not for Clinical Use
            </div>

            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              About NeuroSmriti
            </h1>
            <p className="text-xl md:text-2xl text-purple-200 leading-relaxed mb-4">
              AI-Powered Research Platform for Alzheimer&apos;s Detection
            </p>
            <p className="text-lg text-purple-300 max-w-3xl mx-auto">
              An educational and research prototype demonstrating the potential of graph neural networks and multimodal AI for early cognitive decline detection.
            </p>
          </div>
        </div>
      </section>

      {/* Mission & Purpose */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-2 gap-16 items-center">
              <div>
                <h2 className="text-4xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600">
                  Our Research Mission
                </h2>
                <p className="text-lg text-gray-700 mb-6 leading-relaxed">
                  NeuroSmriti is a research platform developed to explore how artificial intelligence, particularly Graph Neural Networks and multimodal deep learning, can assist in early detection of cognitive decline and Alzheimer&apos;s disease.
                </p>
                <p className="text-lg text-gray-700 mb-6 leading-relaxed">
                  This project demonstrates advanced machine learning techniques including nested cross-validation, clinical metric evaluation (sensitivity, specificity, AUC-ROC), and integration with real medical datasets such as ADNI, OASIS, and NACC.
                </p>
                <div className="bg-indigo-50 border-l-4 border-indigo-600 p-6 rounded-r-xl">
                  <p className="text-indigo-900 font-medium mb-2">
                    <strong>Educational Purpose</strong>
                  </p>
                  <p className="text-indigo-800 text-sm">
                    This platform serves as a learning tool for understanding clinical AI development, regulatory compliance (FDA, HIPAA), and medical-grade validation methodologies.
                  </p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="bg-gradient-to-br from-indigo-100 to-purple-100 rounded-2xl p-6 border border-indigo-200">
                  <div className="flex items-center space-x-4 mb-3">
                    <div className="w-12 h-12 bg-indigo-600 rounded-xl flex items-center justify-center">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="font-bold text-lg text-indigo-900">Research Focus</h3>
                      <p className="text-indigo-700 text-sm">Academic & Clinical Validation</p>
                    </div>
                  </div>
                  <p className="text-gray-700">
                    Exploring AI methodologies for cognitive healthcare with proper clinical validation protocols and ethical considerations.
                  </p>
                </div>

                <div className="bg-gradient-to-br from-blue-100 to-cyan-100 rounded-2xl p-6 border border-blue-200">
                  <div className="flex items-center space-x-4 mb-3">
                    <div className="w-12 h-12 bg-blue-600 rounded-xl flex items-center justify-center">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="font-bold text-lg text-blue-900">Open Research</h3>
                      <p className="text-blue-700 text-sm">Transparent Development</p>
                    </div>
                  </div>
                  <p className="text-gray-700">
                    Complete documentation of data sources, model architectures, validation methodologies, and compliance requirements.
                  </p>
                </div>

                <div className="bg-gradient-to-br from-green-100 to-emerald-100 rounded-2xl p-6 border border-green-200">
                  <div className="flex items-center space-x-4 mb-3">
                    <div className="w-12 h-12 bg-green-600 rounded-xl flex items-center justify-center">
                      <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                      </svg>
                    </div>
                    <div>
                      <h3 className="font-bold text-lg text-green-900">Ethical AI</h3>
                      <p className="text-green-700 text-sm">Privacy & Compliance</p>
                    </div>
                  </div>
                  <p className="text-gray-700">
                    HIPAA-aware design, privacy-preserving techniques, and clear disclaimers about research prototype status.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Research Areas */}
      <section className="py-20 bg-gradient-to-br from-gray-50 to-indigo-50">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4">Research Areas</h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Exploring cutting-edge AI techniques for cognitive healthcare
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-8">
              {researchAreas.map((area, i) => (
                <div key={i} className="bg-white rounded-2xl shadow-lg p-8 hover:shadow-xl transition-all border border-gray-100">
                  <div className={`w-16 h-16 bg-gradient-to-br ${area.color} rounded-2xl flex items-center justify-center mb-6`}>
                    <span className="text-3xl">{area.icon}</span>
                  </div>
                  <h3 className="text-2xl font-bold mb-4">{area.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{area.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Technical Approach */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4">Technical Approach</h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Clinical-grade AI development with rigorous validation
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {technicalApproach.map((item, i) => (
                <div key={i} className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6 border-2 border-indigo-100">
                  <h3 className="font-bold text-lg text-indigo-900 mb-2">{item.name}</h3>
                  <p className="text-indigo-700 font-semibold text-sm mb-3">{item.details}</p>
                  <p className="text-gray-700 text-sm leading-relaxed">{item.description}</p>
                </div>
              ))}
            </div>

            <div className="mt-12 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-8 text-white">
              <div className="flex items-start gap-4">
                <svg className="w-8 h-8 flex-shrink-0 mt-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                </svg>
                <div>
                  <h3 className="text-xl font-bold mb-2">Nested Cross-Validation</h3>
                  <p className="text-purple-100">
                    Our platform implements 10-fold nested cross-validation with 5-fold inner hyperparameter tuning—the gold standard for medical AI validation. This prevents data leakage and provides unbiased performance estimates with 95% confidence intervals.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Data Sources */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4">Real Clinical Data Integration</h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Support for industry-standard Alzheimer&apos;s research datasets
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                { name: 'ADNI', full: 'Alzheimer\'s Disease Neuroimaging Initiative', type: 'MRI, PET, Biomarkers' },
                { name: 'OASIS', full: 'Open Access Series of Imaging Studies', type: 'Brain MRI, Clinical Data' },
                { name: 'NACC', full: 'National Alzheimer\'s Coordinating Center', type: 'Clinical Evaluations' },
                { name: 'DementiaBank', full: 'Speech & Language Database', type: 'Audio, Linguistic Analysis' }
              ].map((dataset, i) => (
                <div key={i} className="bg-white rounded-xl p-6 shadow-md border-l-4 border-indigo-500">
                  <h3 className="font-bold text-xl text-indigo-600 mb-2">{dataset.name}</h3>
                  <p className="text-gray-700 font-medium text-sm mb-2">{dataset.full}</p>
                  <p className="text-gray-600 text-xs">{dataset.type}</p>
                </div>
              ))}
            </div>

            <div className="mt-8 bg-blue-50 border border-blue-200 rounded-xl p-6">
              <p className="text-blue-900">
                <strong>Note:</strong> The platform currently uses synthetic data generated from published research parameters. Integration with real datasets requires proper institutional access, data use agreements, and IRB approval. Comprehensive documentation is provided in <code className="bg-blue-100 px-2 py-1 rounded">ml/data/README_DATA_SOURCES.md</code>.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Important Disclaimer */}
      <section className="py-16 bg-amber-50 border-y-4 border-amber-400">
        <div className="container mx-auto px-4">
          <div className="max-w-5xl mx-auto">
            <div className="flex items-start gap-6">
              <div className="flex-shrink-0">
                <svg className="w-12 h-12 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
              </div>
              <div>
                <h3 className="text-3xl font-bold text-amber-900 mb-4">Critical Medical Disclaimer</h3>
                <div className="space-y-3 text-amber-900 leading-relaxed">
                  <p>
                    <strong className="text-amber-950">Research Prototype Status:</strong> NeuroSmriti is an educational and research platform. It is NOT FDA-approved, NOT clinically validated with real patient outcomes, and NOT intended for medical diagnosis or treatment decisions.
                  </p>
                  <p>
                    <strong className="text-amber-950">Training Data:</strong> The AI models demonstrated here are trained on synthetic data generated from published clinical research parameters. While based on real-world datasets (ADNI, OASIS, NACC), the models have NOT been validated in prospective clinical studies.
                  </p>
                  <p>
                    <strong className="text-amber-950">No Medical Advice:</strong> This platform does not provide medical advice. Always consult qualified healthcare professionals for diagnosis, treatment, and medical decisions. If you have concerns about cognitive health, contact your doctor immediately.
                  </p>
                  <p>
                    <strong className="text-amber-950">Performance Claims:</strong> Any accuracy metrics, sensitivity, or specificity values displayed are from controlled research environments using synthetic or retrospective data. They do NOT reflect real-world clinical performance.
                  </p>
                  <p>
                    <strong className="text-amber-950">Regulatory Path:</strong> Clinical deployment would require FDA approval (510(k) or De Novo), prospective clinical validation, IRB oversight, and continuous post-market surveillance.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Documentation & Resources */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold mb-4">Documentation & Resources</h2>
              <p className="text-xl text-gray-600">Comprehensive guides for researchers and developers</p>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl p-6 border border-indigo-200">
                <svg className="w-10 h-10 text-indigo-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <h3 className="text-xl font-bold mb-3 text-indigo-900">Deployment Guide</h3>
                <p className="text-gray-700 mb-4">Complete setup instructions, Docker configuration, cloud deployment, and security compliance.</p>
                <code className="text-xs bg-white px-2 py-1 rounded border border-indigo-200 block">DEPLOYMENT_GUIDE.md</code>
              </div>

              <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-6 border border-blue-200">
                <svg className="w-10 h-10 text-blue-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4" />
                </svg>
                <h3 className="text-xl font-bold mb-3 text-blue-900">Data Sources Guide</h3>
                <p className="text-gray-700 mb-4">Instructions for accessing ADNI, OASIS, NACC datasets with registration and citation requirements.</p>
                <code className="text-xs bg-white px-2 py-1 rounded border border-blue-200 block">ml/data/README_DATA_SOURCES.md</code>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
                <svg className="w-10 h-10 text-green-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
                <h3 className="text-xl font-bold mb-3 text-green-900">Improvements Summary</h3>
                <p className="text-gray-700 mb-4">Overview of all platform enhancements, validation methods, and compliance updates.</p>
                <code className="text-xs bg-white px-2 py-1 rounded border border-green-200 block">IMPROVEMENTS_SUMMARY.md</code>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Explore the Research Platform</h2>
          <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
            Discover how AI technologies are being researched for potential applications in cognitive healthcare.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/demo"
              className="px-8 py-4 bg-white text-indigo-600 rounded-xl font-semibold text-lg hover:bg-indigo-50 transition shadow-lg"
            >
              Try Demo
            </Link>
            <Link
              href="/contact"
              className="px-8 py-4 bg-transparent border-2 border-white rounded-xl font-semibold text-lg hover:bg-white/10 transition"
            >
              Contact Us
            </Link>
          </div>
          <p className="text-purple-200 mt-8 text-sm max-w-2xl mx-auto">
            Educational and research purposes only. Not approved for clinical use. All research conducted with appropriate ethical oversight and data privacy protections.
          </p>
        </div>
      </section>
    </div>
  )
}
