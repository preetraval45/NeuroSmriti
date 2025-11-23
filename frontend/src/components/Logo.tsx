'use client'

interface LogoProps {
  size?: number
  className?: string
}

export default function Logo({ size = 48, className = '' }: LogoProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <defs>
        <linearGradient id="ns-bg" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#7C3AED" />
          <stop offset="100%" stopColor="#2563EB" />
        </linearGradient>
        <linearGradient id="ns-glow" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#A855F7" />
          <stop offset="100%" stopColor="#3B82F6" />
        </linearGradient>
        <linearGradient id="ns-accent" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stopColor="#F472B6" />
          <stop offset="100%" stopColor="#C084FC" />
        </linearGradient>
        <filter id="ns-shadow" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="2" stdDeviation="3" floodColor="#7C3AED" floodOpacity="0.3"/>
        </filter>
      </defs>

      {/* Main Circle Background */}
      <circle cx="50" cy="50" r="48" fill="url(#ns-bg)" filter="url(#ns-shadow)" />

      {/* Inner glow ring */}
      <circle cx="50" cy="50" r="42" fill="none" stroke="url(#ns-glow)" strokeWidth="1" opacity="0.5" />

      {/* Brain Shape - Stylized */}
      <g transform="translate(50, 50)">
        {/* Left Brain Half */}
        <path
          d="M -5 -28
             C -20 -28 -30 -18 -32 -5
             C -34 8 -28 20 -18 26
             C -12 30 -5 30 -5 30
             L -5 -28"
          fill="white"
          opacity="0.25"
        />

        {/* Right Brain Half */}
        <path
          d="M 5 -28
             C 20 -28 30 -18 32 -5
             C 34 8 28 20 18 26
             C 12 30 5 30 5 30
             L 5 -28"
          fill="white"
          opacity="0.25"
        />

        {/* Center Connection */}
        <rect x="-5" y="-28" width="10" height="58" fill="white" opacity="0.15" rx="2" />
      </g>

      {/* Neural Network - Clean Design */}
      <g>
        {/* Central Hub */}
        <circle cx="50" cy="50" r="8" fill="white" opacity="0.95" />
        <circle cx="50" cy="50" r="5" fill="url(#ns-accent)" />

        {/* Top Node */}
        <circle cx="50" cy="25" r="5" fill="white" opacity="0.9" />
        <circle cx="50" cy="25" r="3" fill="url(#ns-glow)" />

        {/* Bottom Nodes */}
        <circle cx="35" cy="70" r="4" fill="white" opacity="0.85" />
        <circle cx="65" cy="70" r="4" fill="white" opacity="0.85" />

        {/* Side Nodes */}
        <circle cx="25" cy="45" r="4" fill="white" opacity="0.85" />
        <circle cx="75" cy="45" r="4" fill="white" opacity="0.85" />
        <circle cx="28" cy="60" r="3" fill="white" opacity="0.75" />
        <circle cx="72" cy="60" r="3" fill="white" opacity="0.75" />

        {/* Connections - Clean Lines */}
        <g stroke="white" strokeWidth="2" opacity="0.6" strokeLinecap="round">
          {/* Center to Top */}
          <line x1="50" y1="42" x2="50" y2="30" />

          {/* Center to Sides */}
          <line x1="42" y1="50" x2="29" y2="45" />
          <line x1="58" y1="50" x2="71" y2="45" />

          {/* Center to Bottom */}
          <line x1="45" y1="56" x2="37" y2="66" />
          <line x1="55" y1="56" x2="63" y2="66" />
        </g>

        {/* Secondary Connections */}
        <g stroke="white" strokeWidth="1.5" opacity="0.4" strokeLinecap="round">
          <line x1="25" y1="49" x2="28" y2="57" />
          <line x1="75" y1="49" x2="72" y2="57" />
          <line x1="32" y1="63" x2="35" y2="66" />
          <line x1="68" y1="63" x2="65" y2="66" />
        </g>
      </g>

      {/* Memory Symbol - Simplified Lotus */}
      <g transform="translate(50, 50)">
        <ellipse cx="0" cy="0" rx="2" ry="3" fill="#FBBF24" opacity="0.9" />
      </g>

      {/* Decorative Sparkles */}
      <circle cx="22" cy="28" r="2" fill="white" opacity="0.6" />
      <circle cx="78" cy="28" r="2" fill="white" opacity="0.6" />
      <circle cx="18" cy="72" r="1.5" fill="white" opacity="0.4" />
      <circle cx="82" cy="72" r="1.5" fill="white" opacity="0.4" />
    </svg>
  )
}
