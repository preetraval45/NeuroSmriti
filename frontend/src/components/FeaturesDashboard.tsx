"use client";

import React, { useState } from 'react';

interface FeatureCategory {
  name: string;
  icon: string;
  features: string[];
  color: string;
}

const featureCategories: FeatureCategory[] = [
  {
    name: "Clinical Decision Support",
    icon: "🏥",
    color: "bg-blue-100 text-blue-800 border-blue-300",
    features: [
      "AI Treatment Plan Generator",
      "Drug Interaction Checker",
      "Clinical Trial Matcher",
      "Genetic Risk Calculator (APOE4)",
      "Comorbidity Tracker",
      "Personalized Lifestyle Recommendations"
    ]
  },
  {
    name: "Research & Data",
    icon: "📊",
    color: "bg-purple-100 text-purple-800 border-purple-300",
    features: [
      "Research Data Contribution",
      "FHIR-Compliant Export",
      "PDF Report Generation",
      "Population Analytics Dashboard",
      "Cohort Analysis",
      "Predictive Analytics"
    ]
  },
  {
    name: "Social & Support",
    icon: "👥",
    color: "bg-green-100 text-green-800 border-green-300",
    features: [
      "Support Group Finder",
      "Caregiver Forums",
      "Educational Resources Library",
      "Expert Q&A",
      "Peer Matching",
      "Volunteer Opportunities"
    ]
  },
  {
    name: "Gamification & Engagement",
    icon: "🎮",
    color: "bg-yellow-100 text-yellow-800 border-yellow-300",
    features: [
      "Brain Training Games",
      "Achievement System",
      "Progress Milestones",
      "Social Challenges",
      "Reminiscence Therapy Games",
      "VR Therapy Integration"
    ]
  },
  {
    name: "Integration & Automation",
    icon: "🔌",
    color: "bg-indigo-100 text-indigo-800 border-indigo-300",
    features: [
      "EHR Integration (Epic, Cerner)",
      "Wearable Device Sync",
      "Smart Home Integration (Alexa, Google)",
      "Calendar Sync",
      "Pharmacy Auto-Refill",
      "Insurance Portal"
    ]
  },
  {
    name: "Advanced AI Features",
    icon: "🤖",
    color: "bg-pink-100 text-pink-800 border-pink-300",
    features: [
      "24/7 Conversational AI Assistant",
      "Predictive Crisis Detection",
      "Speech Pattern Analysis",
      "Eye Tracking Integration",
      "Gait & Fall Detection",
      "Sleep Pattern Analysis"
    ]
  },
  {
    name: "Communication Tools",
    icon: "💬",
    color: "bg-cyan-100 text-cyan-800 border-cyan-300",
    features: [
      "Video Call Integration",
      "Family Portal",
      "HIPAA-Compliant Care Team Chat",
      "Multi-Language Translation",
      "Text-to-Speech",
      "Emergency Alerts"
    ]
  },
  {
    name: "Safety & Monitoring",
    icon: "🛡️",
    color: "bg-red-100 text-red-800 border-red-300",
    features: [
      "GPS Wandering Detection",
      "Fall Detection",
      "Activity Monitoring",
      "Medication Compliance",
      "Home Safety Checklist",
      "Caregiver Burnout Monitor"
    ]
  },
  {
    name: "Accessibility Features",
    icon: "♿",
    color: "bg-gray-100 text-gray-800 border-gray-300",
    features: [
      "Screen Reader Optimization",
      "Keyboard Navigation",
      "Voice Control",
      "Simplified Language Mode",
      "Picture-Based UI",
      "Adjustable Timing"
    ]
  }
];

export default function FeaturesDashboard() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredCategories = featureCategories.filter(category =>
    category.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    category.features.some(feature =>
      feature.toLowerCase().includes(searchTerm.toLowerCase())
    )
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            NeuroSmriti Features Dashboard
          </h1>
          <p className="text-xl text-gray-600 mb-6">
            Comprehensive AI-Powered Alzheimer's Care Platform
          </p>

          {/* Search Bar */}
          <div className="max-w-2xl mx-auto">
            <input
              type="text"
              placeholder="Search features..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-6 py-3 text-lg border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500"
            />
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-4xl font-bold text-blue-600 mb-2">
              {featureCategories.reduce((sum, cat) => sum + cat.features.length, 0)}
            </div>
            <div className="text-gray-600 font-medium">Total Features</div>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-4xl font-bold text-purple-600 mb-2">
              {featureCategories.length}
            </div>
            <div className="text-gray-600 font-medium">Feature Categories</div>
          </div>
          <div className="bg-white rounded-lg shadow-lg p-6 text-center">
            <div className="text-4xl font-bold text-green-600 mb-2">100%</div>
            <div className="text-gray-600 font-medium">AI-Powered</div>
          </div>
        </div>

        {/* Feature Categories Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredCategories.map((category) => (
            <div
              key={category.name}
              className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer"
              onClick={() => setSelectedCategory(
                selectedCategory === category.name ? null : category.name
              )}
            >
              {/* Category Header */}
              <div className={`p-4 border-2 ${category.color}`}>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <span className="text-3xl">{category.icon}</span>
                    <h3 className="text-lg font-bold">{category.name}</h3>
                  </div>
                  <div className="text-sm font-semibold bg-white px-2 py-1 rounded">
                    {category.features.length}
                  </div>
                </div>
              </div>

              {/* Features List */}
              <div className={`p-4 ${selectedCategory === category.name ? 'block' : 'hidden'}`}>
                <ul className="space-y-2">
                  {category.features.map((feature, idx) => (
                    <li key={idx} className="flex items-start">
                      <span className="text-green-500 mr-2 mt-1">✓</span>
                      <span className="text-gray-700 text-sm">{feature}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Preview (when collapsed) */}
              {selectedCategory !== category.name && (
                <div className="p-4">
                  <p className="text-sm text-gray-600 line-clamp-2">
                    {category.features.slice(0, 2).join(', ')}...
                  </p>
                  <button className="text-blue-600 text-sm font-medium mt-2 hover:underline">
                    View all {category.features.length} features →
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="mt-12 text-center text-gray-600">
          <p className="text-lg font-medium mb-2">
            All features are HIPAA-compliant and designed for accessibility
          </p>
          <div className="flex justify-center space-x-8 mt-4">
            <div className="flex items-center">
              <span className="text-green-500 text-2xl mr-2">✓</span>
              <span>HIPAA Compliant</span>
            </div>
            <div className="flex items-center">
              <span className="text-green-500 text-2xl mr-2">✓</span>
              <span>WCAG AAA Accessible</span>
            </div>
            <div className="flex items-center">
              <span className="text-green-500 text-2xl mr-2">✓</span>
              <span>FHIR Compatible</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
