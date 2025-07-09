// export interface Alert {
//   id: string
//   timestamp: Date
//   anomaly_type: string
//   confidence: number
//   description: string
//   severity: "low" | "medium" | "high"
//   zone: string
//   camera: string
//   name: string,
//   location: {
//     lat: number
//     lng: number
//   }
//   snapshot_url?: string
//   resolved: boolean
//   resolvedAt?: Date
//   latitude: number
//   longitude: number
//     aiDescription?: string
//   lastSeenWearing?: string
//   snapshotUrl?: string
  
// }

// export interface CameraConfig {
//   lat: number
//   lng: number
//   name: string
//   url: string
// }

// export interface FaceDetectionResult {
//   faces: {
//     encoding: number[]
//     location: {
//       top: number
//       right: number
//       bottom: number
//       left: number
//     }
//     landmarks: {
//       [key: string]: { x: number; y: number }[]
//     }
//     descriptor: number[]
//   }[]
//   image: HTMLImageElement
// }



// firebase 


export interface Alert {
  id: string
  name: string
  timestamp: Date
  location: {
    lat: number
    lng: number
  }
  confidence: number
  anomaly_type: string
  description: string
  severity: "low" | "medium" | "high"
  zone: string
  camera: string
  resolved: boolean
  resolvedAt?: Date

  latitude: number
  longitude: number

  aiDescription?: string
  lastSeenWearing?: string

  // Optional image fields (retain both for compatibility)
  snapshot_url?: string
  snapshotUrl?: string
}
