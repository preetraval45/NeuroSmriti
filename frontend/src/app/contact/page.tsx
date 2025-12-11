'use client'

import { useState } from 'react'
import Link from 'next/link'

export default function ContactPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    organization: '',
    subject: 'research',
    message: ''
  })
  const [submitted, setSubmitted] = useState(false)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)

    // Simulate form submission
    setTimeout(() => {
      setSubmitted(true)
      setLoading(false)
    }, 1000)
  }

  if (submitted) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8 text-center border border-gray-200">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Message Received!</h2>
          <p className="text-gray-600 mb-6">Thank you for your inquiry. We&apos;ll review your message and respond accordingly.</p>
          <Link
            href="/"
            className="inline-block px-6 py-3 bg-indigo-600 text-white rounded-xl font-semibold hover:bg-indigo-700 transition"
          >
            Back to Home
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="relative bg-gradient-to-br from-indigo-900 via-purple-900 to-blue-900 text-white py-20 overflow-hidden">
        <div className="absolute inset-0 bg-[url('/grid.svg')] opacity-10"></div>
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500 rounded-full filter blur-3xl opacity-20"></div>
        <div className="absolute bottom-20 right-10 w-96 h-96 bg-blue-500 rounded-full filter blur-3xl opacity-20"></div>

        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="inline-flex items-center px-4 py-2 bg-blue-500/20 border border-blue-400/30 rounded-full text-sm mb-8 backdrop-blur-sm">
              <svg className="w-4 h-4 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
              </svg>
              Research Inquiry Portal
            </div>

            <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
              Contact Us
            </h1>
            <p className="text-xl text-purple-200 leading-relaxed max-w-3xl mx-auto">
              Connect with us for research collaborations, technical inquiries, or general questions about the NeuroSmriti platform.
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Contact Info */}
            <div className="md:col-span-1">
              <div className="bg-white rounded-2xl shadow-lg p-6 mb-6 border border-gray-200">
                <h3 className="text-xl font-bold mb-6 text-indigo-900">Get in Touch</h3>

                <div className="space-y-6">
                  <div className="flex items-start">
                    <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mr-4 flex-shrink-0">
                      <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-800 mb-1">Research Lab</h4>
                      <p className="text-gray-600 text-sm">
                        University of North Carolina<br />
                        at Charlotte<br />
                        Charlotte, NC 28223
                      </p>
                    </div>
                  </div>

                  <div className="flex items-start">
                    <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mr-4 flex-shrink-0">
                      <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-800 mb-1">Email</h4>
                      <p className="text-gray-600 text-sm mb-1">research@neurosmriti.com</p>
                      <p className="text-xs text-gray-500">For research inquiries</p>
                    </div>
                  </div>

                  <div className="flex items-start">
                    <div className="w-12 h-12 bg-indigo-100 rounded-xl flex items-center justify-center mr-4 flex-shrink-0">
                      <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </div>
                    <div>
                      <h4 className="font-semibold text-gray-800 mb-1">Resources</h4>
                      <Link href="https://github.com" className="text-indigo-600 hover:text-indigo-700 text-sm block">
                        GitHub Repository
                      </Link>
                      <Link href="#" className="text-indigo-600 hover:text-indigo-700 text-sm block">
                        Documentation
                      </Link>
                    </div>
                  </div>
                </div>
              </div>

              {/* Important Notice */}
              <div className="bg-amber-50 rounded-2xl p-6 border-2 border-amber-200">
                <div className="flex items-start gap-3 mb-3">
                  <svg className="w-6 h-6 text-amber-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                  <div>
                    <h4 className="font-bold text-amber-900 mb-2">Not for Medical Use</h4>
                    <p className="text-amber-800 text-sm leading-relaxed">
                      This is a research platform only. For medical concerns or emergencies, please contact your healthcare provider or call 911.
                    </p>
                  </div>
                </div>
                <div className="mt-4 pt-4 border-t border-amber-200">
                  <p className="text-amber-900 text-xs font-medium mb-2">Alzheimer&apos;s Association Helpline:</p>
                  <a
                    href="tel:+18002723900"
                    className="inline-flex items-center px-3 py-2 bg-amber-600 text-white rounded-lg font-semibold hover:bg-amber-700 transition text-sm"
                  >
                    <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                    1-800-272-3900
                  </a>
                  <p className="text-amber-700 text-xs mt-2">24/7 support for patients and caregivers</p>
                </div>
              </div>
            </div>

            {/* Contact Form */}
            <div className="md:col-span-2">
              <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
                <h3 className="text-2xl font-bold mb-2 text-indigo-900">Send us a Message</h3>
                <p className="text-gray-600 mb-6">
                  For research collaboration, technical questions, or platform inquiries
                </p>

                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Full Name *</label>
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-gray-900"
                        placeholder="Dr. John Smith"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Email Address *</label>
                      <input
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-gray-900"
                        placeholder="john.smith@university.edu"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Organization / Institution</label>
                    <input
                      type="text"
                      value={formData.organization}
                      onChange={(e) => setFormData({ ...formData, organization: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-gray-900"
                      placeholder="University or Research Institution"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Inquiry Type *</label>
                    <select
                      value={formData.subject}
                      onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition text-gray-900"
                      required
                    >
                      <option value="research">Research Collaboration</option>
                      <option value="technical">Technical Question</option>
                      <option value="demo">Platform Demo Request</option>
                      <option value="data">Dataset Integration</option>
                      <option value="academic">Academic Partnership</option>
                      <option value="general">General Inquiry</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Message *</label>
                    <textarea
                      value={formData.message}
                      onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                      rows={6}
                      className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition resize-none text-gray-900"
                      placeholder="Tell us about your research interests or technical questions..."
                      required
                    />
                  </div>

                  <div className="bg-blue-50 border border-blue-200 rounded-xl p-4">
                    <div className="flex items-start">
                      <svg className="w-5 h-5 text-blue-600 mt-0.5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                      </svg>
                      <p className="text-blue-900 text-sm">
                        <strong>Research Platform Notice:</strong> This is an educational and research prototype. Responses are for informational purposes only and do not constitute medical advice or clinical consultation.
                      </p>
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={loading}
                    className="w-full py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-xl font-semibold hover:shadow-lg transition disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? (
                      <span className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Sending...
                      </span>
                    ) : (
                      'Send Message'
                    )}
                  </button>
                </form>
              </div>
            </div>
          </div>

          {/* FAQ Section */}
          <div className="mt-16">
            <h2 className="text-3xl font-bold text-center mb-4 text-indigo-900">Frequently Asked Questions</h2>
            <p className="text-center text-gray-600 mb-12 max-w-2xl mx-auto">
              Common questions about the NeuroSmriti research platform
            </p>
            <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto">
              {[
                {
                  q: 'Can I use this platform for patient care?',
                  a: 'No. NeuroSmriti is a research prototype for educational purposes only. It is NOT FDA-approved and is NOT intended for clinical diagnosis or treatment decisions. Always consult qualified healthcare professionals for medical care.'
                },
                {
                  q: 'How can I access real datasets (ADNI, OASIS, NACC)?',
                  a: 'See our Data Sources Guide (ml/data/README_DATA_SOURCES.md) for detailed instructions on registration, data use agreements, and citation requirements for each dataset.'
                },
                {
                  q: 'Is the platform suitable for research publications?',
                  a: 'The platform demonstrates clinical-grade validation methodologies (nested CV, clinical metrics). However, any research publication should use real patient data with proper IRB approval and follow institutional guidelines.'
                },
                {
                  q: 'How is data privacy handled?',
                  a: 'The platform implements HIPAA-aware design principles and privacy-preserving techniques. All synthetic data generation follows de-identification best practices. Real data integration requires proper institutional data use agreements.'
                },
                {
                  q: 'Can I contribute to the project?',
                  a: 'Yes! We welcome contributions from researchers and developers. Please review our documentation and reach out for collaboration opportunities in ML research, clinical validation, or platform development.'
                },
                {
                  q: 'What technical requirements are needed?',
                  a: 'See the Deployment Guide (DEPLOYMENT_GUIDE.md) for complete system requirements, Docker setup, and cloud deployment options for AWS, GCP, and Azure.'
                }
              ].map((faq, i) => (
                <div key={i} className="bg-white rounded-xl shadow-md p-6 border border-gray-200 hover:shadow-lg transition">
                  <h4 className="font-bold text-gray-900 mb-3">{faq.q}</h4>
                  <p className="text-gray-600 text-sm leading-relaxed">{faq.a}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Additional Resources */}
          <div className="mt-16 bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 rounded-2xl p-8 text-white">
            <div className="text-center max-w-3xl mx-auto">
              <h2 className="text-3xl font-bold mb-4">Additional Resources</h2>
              <p className="text-purple-100 mb-8">
                Explore our comprehensive documentation for detailed technical information
              </p>
              <div className="grid sm:grid-cols-3 gap-4">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 hover:bg-white/20 transition">
                  <h3 className="font-bold mb-2">Documentation</h3>
                  <p className="text-purple-100 text-sm">Complete setup and usage guides</p>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 hover:bg-white/20 transition">
                  <h3 className="font-bold mb-2">API Reference</h3>
                  <p className="text-purple-100 text-sm">Technical API documentation</p>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 hover:bg-white/20 transition">
                  <h3 className="font-bold mb-2">Research Papers</h3>
                  <p className="text-purple-100 text-sm">Citations and references</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
