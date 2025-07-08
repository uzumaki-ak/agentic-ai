// Environment-based configuration
export const CAMERA_API_URL = process.env.PYTHON_API_URL || 'http://localhost:5000'
export const GEMINI_API_URL = process.env.GEMINI_API_URL || 'https://generativelanguage.googleapis.com/v1/models/gemini-pro-vision'
export const GEMINI_API_KEY = process.env.GEMINI_API_KEY || ''

// Default values
export const DEFAULT_CAMERA_LOCATION = {
  lat: parseFloat(process.env.CAMERA_LAT || '28.6129'),
  lng: parseFloat(process.env.CAMERA_LNG || '77.2295')
}

export const FACE_MATCH_THRESHOLD = parseFloat(
  process.env.FACE_MATCH_THRESHOLD || '0.6'
)