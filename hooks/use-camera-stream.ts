import { useState, useEffect } from 'react'

export function useCameraStream() {
  const [stream, setStream] = useState<MediaStream | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isActive, setIsActive] = useState(false)

  const startStream = async (constraints: MediaStreamConstraints = { 
    video: { facingMode: 'environment' } 
  }) => {
    try {
      setError(null)
      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints)
      setStream(mediaStream)
      setIsActive(true)
      return mediaStream
    } catch (err) {
      console.error('Camera error:', err)
      setError('Failed to access camera. Please check permissions.')
      setIsActive(false)
      throw err
    }
  }

  const stopStream = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop())
      setStream(null)
      setIsActive(false)
    }
  }

  useEffect(() => {
    return () => {
      stopStream()
    }
  }, [])

  return {
    stream,
    error,
    isActive,
    startStream,
    stopStream
  }
}