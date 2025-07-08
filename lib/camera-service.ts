import { CAMERA_API_URL } from './constants'

interface CameraConfig {
  lat: number
  lng: number
  name: string
  url: string
}

export async function getCameraConfig(): Promise<CameraConfig> {
  try {
    const response = await fetch(`${CAMERA_API_URL}/config`)
    if (!response.ok) throw new Error('Failed to fetch camera config')
    return response.json()
  } catch (error) {
    console.error('Camera config error:', error)
    return {
      lat: parseFloat(process.env.CAMERA_LAT || '28.6129'),
      lng: parseFloat(process.env.CAMERA_LNG || '77.2295'),
      name: process.env.CAMERA_NAME || 'Main Entrance',
      url: process.env.CAMERA_URL || 'http://192.168.1.50:8080/video'
    }
  }
}

export async function startDetection(encodings: number[][], targetPath: string) {
  try {
    const response = await fetch(`${CAMERA_API_URL}/start`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ encodings, targetPath })
    })
    
    if (!response.ok) throw new Error('Failed to start detection')
    return response.json()
  } catch (error) {
    console.error('Detection start error:', error)
    throw error
  }
}