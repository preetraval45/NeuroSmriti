import Link from 'next/link'

export default function AboutPage() {
  const team = [
    {
      name: 'Dr. Emily Chen',
      role: 'Chief Medical Officer',
      bio: 'Neurologist with 20+ years of experience in Alzheimer\'s research',
      image: '👩‍⚕️'
    },
    {
      name: 'Dr. Michael Park',
      role: 'AI Research Director',
      bio: 'PhD in Machine Learning from Stanford, focused on medical AI',
      image: '👨‍💻'
    },
    {
      name: 'Sarah Williams',
      role: 'Head of Patient Care',
      bio: 'Former caregiver turned patient advocate and product designer',
      image: '👩‍💼'
    },
    {
      name: 'Dr. James Thompson',
      role: 'Clinical Research Lead',
      bio: 'Leading clinical trials and validation studies',
      image: '👨‍🔬'
    }
  ]

  const milestones = [
    { year: '2020', event: 'NeuroSmriti founded with mission to transform Alzheimer\'s care' },
    { year: '2021', event: 'First AI model achieves 90% detection accuracy' },
    { year: '2022', event: 'Clinical validation with 10,000 patients completed' },
    { year: '2023', event: 'FDA Breakthrough Device Designation received' },
    { year: '2024', event: 'Launched to public, helping 50,000+ families' }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-purple-900 via-indigo-900 to-blue-900 text-white py-24">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">About NeuroSmriti</h1>
            <p className="text-xl text-purple-200 leading-relaxed">
              We believe that every memory matters. Our mission is to harness the power of AI
              to detect Alzheimer&apos;s earlier, preserve precious memories longer, and give families
              the time they deserve together.
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <div className="grid md:grid-cols-2 gap-16 items-center">
              <div>
                <h2 className="text-4xl font-bold mb-6">Our Mission</h2>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  Alzheimer&apos;s disease affects over 55 million people worldwide, with a new case
                  developing every 3 seconds. Traditional diagnosis often comes too late, after
                  significant brain damage has already occurred.
                </p>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  At NeuroSmriti, we&apos;re changing this narrative. Our AI-powered platform can detect
                  early signs of Alzheimer&apos;s up to 6 years before traditional methods, giving families
                  precious time for treatment, planning, and making memories.
                </p>
                <p className="text-lg text-gray-600 leading-relaxed">
                  &quot;Smriti&quot; means &quot;memory&quot; in Sanskrit. We chose this name because memory is at the
                  heart of everything we do – preserving it, protecting it, and honoring it.
                </p>
              </div>
              <div className="bg-gradient-to-br from-purple-100 to-blue-100 rounded-3xl p-8">
                <div className="space-y-6">
                  <div className="flex items-center space-x-4">
                    <div className="w-16 h-16 bg-purple-600 rounded-2xl flex items-center justify-center">
                      <span className="text-3xl">🎯</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-xl">Early Detection</h3>
                      <p className="text-gray-600">Catch it before symptoms appear</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="w-16 h-16 bg-blue-600 rounded-2xl flex items-center justify-center">
                      <span className="text-3xl">💚</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-xl">Memory Preservation</h3>
                      <p className="text-gray-600">Help protect what matters most</p>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="w-16 h-16 bg-green-600 rounded-2xl flex items-center justify-center">
                      <span className="text-3xl">🤝</span>
                    </div>
                    <div>
                      <h3 className="font-bold text-xl">Family Support</h3>
                      <p className="text-gray-600">Help for patients and caregivers</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gradient-to-r from-purple-600 to-blue-600 text-white">
        <div className="container mx-auto px-4">
          <div className="max-w-5xl mx-auto grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-5xl font-bold mb-2">94%</div>
              <div className="text-purple-200">Detection Accuracy</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">50K+</div>
              <div className="text-purple-200">Families Helped</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">6 Years</div>
              <div className="text-purple-200">Earlier Detection</div>
            </div>
            <div>
              <div className="text-5xl font-bold mb-2">100+</div>
              <div className="text-purple-200">Clinical Partners</div>
            </div>
          </div>
        </div>
      </section>

      {/* Timeline Section */}
      <section className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-4xl font-bold text-center mb-16">Our Journey</h2>
            <div className="relative">
              <div className="absolute left-1/2 transform -translate-x-1/2 h-full w-1 bg-purple-200" />
              {milestones.map((milestone, i) => (
                <div key={i} className={`relative flex items-center mb-12 ${i % 2 === 0 ? 'flex-row-reverse' : ''}`}>
                  <div className={`w-1/2 ${i % 2 === 0 ? 'text-right pr-12' : 'pl-12'}`}>
                    <div className="bg-white rounded-xl shadow-lg p-6">
                      <span className="text-purple-600 font-bold text-xl">{milestone.year}</span>
                      <p className="text-gray-700 mt-2">{milestone.event}</p>
                    </div>
                  </div>
                  <div className="absolute left-1/2 transform -translate-x-1/2 w-6 h-6 bg-purple-600 rounded-full border-4 border-white" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center mb-4">Meet Our Team</h2>
            <p className="text-xl text-gray-600 text-center mb-16 max-w-2xl mx-auto">
              A dedicated team of doctors, researchers, engineers, and caregivers united by
              one goal: making Alzheimer&apos;s care better.
            </p>
            <div className="grid md:grid-cols-4 gap-8">
              {team.map((member, i) => (
                <div key={i} className="bg-gray-50 rounded-2xl p-6 text-center hover:shadow-lg transition">
                  <div className="w-24 h-24 bg-gradient-to-br from-purple-200 to-blue-200 rounded-full flex items-center justify-center mx-auto mb-4">
                    <span className="text-5xl">{member.image}</span>
                  </div>
                  <h3 className="text-xl font-bold">{member.name}</h3>
                  <p className="text-purple-600 font-medium mb-2">{member.role}</p>
                  <p className="text-gray-600 text-sm">{member.bio}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Research Section */}
      <section className="py-20 bg-gradient-to-br from-purple-50 to-blue-50">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-4xl font-bold text-center mb-16">Our Research</h2>
            <div className="grid md:grid-cols-3 gap-8">
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <span className="text-4xl block mb-4">📊</span>
                <h3 className="text-xl font-bold mb-3">Clinical Validation</h3>
                <p className="text-gray-600 mb-4">
                  Our AI models have been validated in clinical studies with over 50,000 patients
                  across multiple healthcare systems.
                </p>
                <a href="#" className="text-purple-600 font-semibold hover:text-purple-700">
                  Read the research →
                </a>
              </div>
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <span className="text-4xl block mb-4">🔬</span>
                <h3 className="text-xl font-bold mb-3">Ongoing Trials</h3>
                <p className="text-gray-600 mb-4">
                  We&apos;re continuously improving our technology through partnerships with leading
                  research institutions worldwide.
                </p>
                <a href="#" className="text-purple-600 font-semibold hover:text-purple-700">
                  View active trials →
                </a>
              </div>
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <span className="text-4xl block mb-4">📚</span>
                <h3 className="text-xl font-bold mb-3">Publications</h3>
                <p className="text-gray-600 mb-4">
                  Our team has published over 30 peer-reviewed papers on AI in Alzheimer&apos;s
                  detection and cognitive care.
                </p>
                <a href="#" className="text-purple-600 font-semibold hover:text-purple-700">
                  Browse publications →
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Partners Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="max-w-6xl mx-auto text-center">
            <h2 className="text-2xl font-bold mb-8 text-gray-600">Trusted By Leading Institutions</h2>
            <div className="flex flex-wrap justify-center items-center gap-12 opacity-60">
              <div className="text-2xl font-bold text-gray-400">Mayo Clinic</div>
              <div className="text-2xl font-bold text-gray-400">Cleveland Clinic</div>
              <div className="text-2xl font-bold text-gray-400">Johns Hopkins</div>
              <div className="text-2xl font-bold text-gray-400">Stanford Medicine</div>
              <div className="text-2xl font-bold text-gray-400">UCSF Health</div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-blue-600 text-white">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-6">Join Us in the Fight Against Alzheimer&apos;s</h2>
          <p className="text-xl text-purple-100 mb-8 max-w-2xl mx-auto">
            Whether you&apos;re a patient, caregiver, healthcare provider, or researcher,
            there&apos;s a place for you in our community.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/register"
              className="px-8 py-4 bg-white text-purple-600 rounded-xl font-semibold text-lg hover:bg-purple-50 transition"
            >
              Get Started
            </Link>
            <Link
              href="/contact"
              className="px-8 py-4 bg-transparent border-2 border-white rounded-xl font-semibold text-lg hover:bg-white/10 transition"
            >
              Contact Us
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
