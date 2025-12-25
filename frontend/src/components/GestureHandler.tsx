'use client'

import React, { useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'

export default function GestureHandler({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const touchStartX = useRef(0)
  const touchStartY = useRef(0)
  const touchEndX = useRef(0)
  const touchEndY = useRef(0)

  useEffect(() => {
    const minSwipeDistance = 100 // Minimum distance for swipe gesture

    const handleTouchStart = (e: TouchEvent) => {
      touchStartX.current = e.touches[0].clientX
      touchStartY.current = e.touches[0].clientY
    }

    const handleTouchMove = (e: TouchEvent) => {
      touchEndX.current = e.touches[0].clientX
      touchEndY.current = e.touches[0].clientY
    }

    const handleTouchEnd = () => {
      const distanceX = touchEndX.current - touchStartX.current
      const distanceY = touchEndY.current - touchStartY.current

      // Determine if swipe is primarily horizontal or vertical
      const isHorizontalSwipe = Math.abs(distanceX) > Math.abs(distanceY)

      if (Math.abs(distanceX) < minSwipeDistance && Math.abs(distanceY) < minSwipeDistance) {
        return // Not a swipe, just a tap
      }

      if (isHorizontalSwipe) {
        // Horizontal swipes
        if (distanceX > 0) {
          // Swipe right - go back
          if (window.history.length > 1) {
            router.back()
          }
        } else {
          // Swipe left - go forward (if available)
          router.forward()
        }
      } else {
        // Vertical swipes
        if (distanceY > 0) {
          // Swipe down - scroll to top
          window.scrollTo({ top: 0, behavior: 'smooth' })
        } else {
          // Swipe up - scroll to bottom
          window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })
        }
      }

      // Reset
      touchStartX.current = 0
      touchStartY.current = 0
      touchEndX.current = 0
      touchEndY.current = 0
    }

    // Add touch event listeners
    document.addEventListener('touchstart', handleTouchStart, { passive: true })
    document.addEventListener('touchmove', handleTouchMove, { passive: true })
    document.addEventListener('touchend', handleTouchEnd, { passive: true })

    // Cleanup
    return () => {
      document.removeEventListener('touchstart', handleTouchStart)
      document.removeEventListener('touchmove', handleTouchMove)
      document.removeEventListener('touchend', handleTouchEnd)
    }
  }, [router])

  // Double-tap to zoom
  useEffect(() => {
    let lastTap = 0

    const handleDoubleTap = (e: TouchEvent) => {
      const currentTime = new Date().getTime()
      const tapLength = currentTime - lastTap

      if (tapLength < 300 && tapLength > 0) {
        // Double tap detected
        const target = e.target as HTMLElement

        // Toggle zoom on double-tap
        if (target.style.transform === 'scale(1.5)') {
          target.style.transform = 'scale(1)'
        } else {
          target.style.transform = 'scale(1.5)'
          target.style.transition = 'transform 0.3s ease'
        }

        e.preventDefault()
      }

      lastTap = currentTime
    }

    document.addEventListener('touchend', handleDoubleTap)

    return () => {
      document.removeEventListener('touchend', handleDoubleTap)
    }
  }, [])

  return <>{children}</>
}
