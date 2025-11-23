import Link from 'next/link'

export default function ResourcesPage() {
  const articles = [
    {
      category: 'Understanding Alzheimer\'s',
      title: 'What is Alzheimer\'s Disease?',
      description: 'A comprehensive guide to understanding Alzheimer\'s disease, its causes, symptoms, and progression stages.',
      readTime: '8 min read',
      featured: true
    },
    {
      category: 'Early Detection',
      title: '10 Early Warning Signs of Alzheimer\'s',
      description: 'Learn to recognize the early signs of Alzheimer\'s that often go unnoticed.',
      readTime: '5 min read',
      featured: true
    },
    {
      category: 'Caregiver Support',
      title: 'The Caregiver\'s Complete Guide',
      description: 'Essential tips and strategies for caring for a loved one with Alzheimer\'s.',
      readTime: '12 min read',
      featured: true
    },
    {
      category: 'Treatment',
      title: 'Current Treatment Options Explained',
      description: 'An overview of approved medications and therapies for Alzheimer\'s disease.',
      readTime: '6 min read',
      featured: false
    },
    {
      category: 'Research',
      title: 'Promising Alzheimer\'s Research in 2024',
      description: 'The latest breakthroughs in Alzheimer\'s research and what they mean for patients.',
      readTime: '7 min read',
      featured: false
    },
    {
      category: 'Lifestyle',
      title: 'Brain-Healthy Diet and Exercise',
      description: 'How lifestyle changes can help reduce Alzheimer\'s risk and slow progression.',
      readTime: '5 min read',
      featured: false
    }
  ]

  const faqs = [
    {
      question: 'What is the difference between Alzheimer\'s and dementia?',
      answer: 'Dementia is an umbrella term for symptoms affecting memory, thinking, and social abilities severely enough to interfere with daily life. Alzheimer\'s disease is the most common cause of dementia, accounting for 60-80% of cases.'
    },
    {
      question: 'Can Alzheimer\'s be prevented?',
      answer: 'While there\'s no guaranteed prevention, research suggests that maintaining a healthy lifestyle - including regular exercise, a balanced diet, social engagement, and mental stimulation - may reduce the risk or delay onset.'
    },
    {
      question: 'How accurate is NeuroSmriti\'s AI detection?',
      answer: 'Our AI has demonstrated 94% accuracy in clinical validation studies with over 50,000 patients. It can detect signs of Alzheimer\'s up to 6 years before traditional diagnostic methods.'
    },
    {
      question: 'Is the assessment covered by insurance?',
      answer: 'Coverage varies by insurance plan. We recommend checking with your provider. We also offer a free tier that includes basic cognitive assessments.'
    }
  ]

  const supportGroups = [
    {
      name: 'Alzheimer\'s Association',
      description: '24/7 Helpline and local support groups',
      link: 'https://www.alz.org',
      phone: '1-800-272-3900'
    },
    {
      name: 'Caregiver Action Network',
      description: 'Education, peer support, and resources for family caregivers',
      link: 'https://www.caregiveraction.org',
      phone: '1-855-227-3640'
    },
    {
      name: 'Family Caregiver Alliance',
      description: 'Information, education, services, and advocacy',
      link: 'https://www.caregiver.org',
      phone: '1-800-445-8106'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <section className="bg-gradient-to-r from-teal-600 to-cyan-700 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-4">Resources & Support</h1>
            <p className="text-xl text-teal-100">
              Educational materials, support groups, and helpful resources for patients and caregivers
            </p>
          </div>
        </div>
      </section>

      <div className="container mx-auto px-4 py-12">
        <div className="max-w-6xl mx-auto">
          {/* Featured Articles */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold mb-8">Featured Articles</h2>
            <div className="grid md:grid-cols-3 gap-8">
              {articles.filter(a => a.featured).map((article, i) => (
                <div key={i} className="bg-white rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition group cursor-pointer">
                  <div className="h-48 bg-gradient-to-br from-teal-400 to-cyan-500 flex items-center justify-center">
                    <span className="text-6xl group-hover:scale-110 transition">
                      {article.category.includes('Understanding') ? '📖' :
                       article.category.includes('Detection') ? '🔍' : '💚'}
                    </span>
                  </div>
                  <div className="p-6">
                    <span className="text-sm text-teal-600 font-semibold">{article.category}</span>
                    <h3 className="text-xl font-bold mt-2 mb-3 group-hover:text-teal-600 transition">
                      {article.title}
                    </h3>
                    <p className="text-gray-600 mb-4">{article.description}</p>
                    <span className="text-sm text-gray-500">{article.readTime}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* All Articles */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold mb-8">More Articles</h2>
            <div className="space-y-4">
              {articles.filter(a => !a.featured).map((article, i) => (
                <div key={i} className="bg-white rounded-xl shadow p-6 flex items-center hover:shadow-lg transition cursor-pointer">
                  <div className="w-16 h-16 bg-teal-100 rounded-xl flex items-center justify-center mr-6">
                    <span className="text-2xl">📄</span>
                  </div>
                  <div className="flex-1">
                    <span className="text-sm text-teal-600 font-semibold">{article.category}</span>
                    <h3 className="text-lg font-bold">{article.title}</h3>
                    <p className="text-gray-600 text-sm">{article.description}</p>
                  </div>
                  <span className="text-sm text-gray-500">{article.readTime}</span>
                </div>
              ))}
            </div>
          </div>

          {/* FAQ Section */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold mb-8">Frequently Asked Questions</h2>
            <div className="space-y-4">
              {faqs.map((faq, i) => (
                <div key={i} className="bg-white rounded-xl shadow-lg p-6">
                  <h3 className="text-lg font-bold mb-3 flex items-start">
                    <span className="text-teal-600 mr-3">Q:</span>
                    {faq.question}
                  </h3>
                  <p className="text-gray-600 pl-8">{faq.answer}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Support Groups */}
          <div className="mb-16">
            <h2 className="text-3xl font-bold mb-8">Support Organizations</h2>
            <div className="grid md:grid-cols-3 gap-6">
              {supportGroups.map((group, i) => (
                <div key={i} className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition">
                  <h3 className="text-xl font-bold mb-2">{group.name}</h3>
                  <p className="text-gray-600 mb-4">{group.description}</p>
                  <div className="space-y-2">
                    <a href={`tel:${group.phone}`} className="flex items-center text-teal-600 hover:text-teal-700">
                      <span className="mr-2">📞</span>
                      {group.phone}
                    </a>
                    <a href={group.link} target="_blank" rel="noopener noreferrer" className="flex items-center text-teal-600 hover:text-teal-700">
                      <span className="mr-2">🌐</span>
                      Visit Website
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Downloadable Resources */}
          <div className="bg-gradient-to-r from-teal-100 to-cyan-100 rounded-2xl p-8">
            <h2 className="text-2xl font-bold mb-6">Downloadable Resources</h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
              {[
                { name: 'Caregiver Handbook', icon: '📕', type: 'PDF' },
                { name: 'Daily Care Checklist', icon: '✅', type: 'PDF' },
                { name: 'Medication Tracker', icon: '💊', type: 'PDF' },
                { name: 'Memory Exercise Book', icon: '🧠', type: 'PDF' }
              ].map((resource, i) => (
                <button
                  key={i}
                  type="button"
                  className="bg-white rounded-xl p-4 text-left hover:shadow-lg transition flex items-center"
                >
                  <span className="text-3xl mr-4">{resource.icon}</span>
                  <div>
                    <p className="font-semibold">{resource.name}</p>
                    <p className="text-sm text-gray-500">{resource.type}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Contact Section */}
          <div className="mt-16 text-center">
            <h2 className="text-2xl font-bold mb-4">Need More Help?</h2>
            <p className="text-gray-600 mb-6">
              Our support team is available 24/7 to answer your questions.
            </p>
            <div className="flex justify-center gap-4">
              <Link
                href="/contact"
                className="px-8 py-3 bg-teal-600 text-white rounded-xl font-semibold hover:bg-teal-700 transition"
              >
                Contact Support
              </Link>
              <Link
                href="/community"
                className="px-8 py-3 border-2 border-teal-600 text-teal-600 rounded-xl font-semibold hover:bg-teal-50 transition"
              >
                Join Community
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
