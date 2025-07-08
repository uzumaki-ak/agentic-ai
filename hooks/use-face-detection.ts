import { useState, useEffect } from 'react'
import * as faceapi from 'face-api.js'

export function useFaceDetection() {
  const [modelsLoaded, setModelsLoaded] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadModels = async () => {
      try {
        setIsLoading(true)
        
        // Load models from public directory
        await Promise.all([
          faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
          faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
          faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
          faceapi.nets.faceExpressionNet.loadFromUri('/models'),
        ])
        
        setModelsLoaded(true)
        setError(null)
      } catch (err) {
        console.error('Failed to load face models:', err)
        setError('Failed to initialize face detection')
      } finally {
        setIsLoading(false)
      }
    }

    if (!modelsLoaded) {
      loadModels()
    }
  }, [])

  const detectFaces = async (image: HTMLImageElement) => {
    if (!modelsLoaded) {
      throw new Error('Face detection models not loaded')
    }

    try {
      return await faceapi
        .detectAllFaces(image, new faceapi.TinyFaceDetectorOptions())
        .withFaceLandmarks()
        .withFaceExpressions()
        .withFaceDescriptors()
    } catch (err) {
      console.error('Face detection error:', err)
      throw new Error('Failed to detect faces')
    }
  }

  return {
    modelsLoaded,
    isLoading,
    error,
    detectFaces
  }
}