// import { NextResponse } from 'next/server'
// import fs from 'fs'
// import path from 'path'
// import { processUploads } from '@/lib/face-recognition'

// export async function POST(req: Request) {
//   const formData = await req.formData()
  
//   try {
//     const { name, encodings, metadata } = await processUploads(formData)
    
//     // Save target image
//     const file = formData.get('primaryPhoto') as File
//     const buffer = Buffer.from(await file.arrayBuffer())
//     const targetPath = path.join(process.cwd(), 'public', 'targets', `${Date.now()}.jpg`)
//     fs.writeFileSync(targetPath, buffer)
    
//     // Start camera monitoring
//     const cameraStatus = await fetch(`${process.env.PYTHON_API_URL}/start`, {
//       method: 'POST',
//       body: JSON.stringify({ encodings, targetPath })
//     })
    
//     return NextResponse.json({
//       success: true,
//       message: 'Search started',
//       data: { name, ...metadata }
//     })
//   } catch (error) {
//     return NextResponse.json(
//       { error: 'Failed to process upload' },
//       { status: 500 }
//     )
//   }
// }



// export const runtime = 'nodejs';

// import { NextResponse } from 'next/server';
// import fs from 'fs';
// import path from 'path';
// import { processUploads } from '@/lib/face-recognition';

// export async function POST(req: Request) {
//   const formData = await req.formData();

//   try {
//     const { name, encodings, metadata } = await processUploads(formData);

//     const file = formData.get('primaryPhoto') as File;
//     const buffer = Buffer.from(await file.arrayBuffer());
//     const targetPath = path.join(process.cwd(), 'public', 'targets', `${Date.now()}.jpg`);
//     fs.writeFileSync(targetPath, buffer);

//     const response = await fetch(`${process.env.PYTHON_API_URL}/start`, {
//       method: 'POST',
//       headers: { 'Content-Type': 'application/json' },
//       body: JSON.stringify({ encodings, targetPath }),
//     });

//     if (!response.ok) throw new Error('Failed to start detection');

//     return NextResponse.json({
//       success: true,
//       message: 'Search started',
//       data: { name, ...metadata },
//     });
//   } catch (error) {
//     console.error('Upload error:', error);
//     return NextResponse.json(
//       { error: 'Failed to process upload', details: (error as Error).message },
//       { status: 500 }
//     );
//   }
// }





// import { NextResponse } from 'next/server'
// import fs from 'fs'
// import path from 'path'

// export async function POST(req: Request) {
//   try {
//     const formData = await req.formData()
//     const file = formData.get('primaryPhoto') as File
//     const name = formData.get('name') as string
    
//     if (!file) {
//       return NextResponse.json(
//         { error: 'No file provided' },
//         { status: 400 }
//       )
//     }

//     console.log('Processing upload:', { fileName: file.name, name })
    
//     // Create directories if they don't exist
//     const targetsDir = path.join(process.cwd(), 'python-backend', 'targets')
//     if (!fs.existsSync(targetsDir)) {
//       fs.mkdirSync(targetsDir, { recursive: true })
//     }
    
//     // Save the uploaded file
//     const buffer = Buffer.from(await file.arrayBuffer())
//     const targetPath = path.join(targetsDir, 'current_target.jpg')
//     fs.writeFileSync(targetPath, buffer)
    
//     console.log('File saved to:', targetPath)
    
//     // Try to notify Python backend (optional - your main.py will detect the file)
//     try {
//       const pythonApiUrl = process.env.PYTHON_API_URL || 'http://localhost:5000'
//       const response = await fetch(`${pythonApiUrl}/target_status`, {
//         method: 'GET',
//         headers: { 'Content-Type': 'application/json' }
//       })
      
//       if (response.ok) {
//         const data = await response.json()
//         console.log('Python backend status:', data)
//       }
//     } catch (pythonError) {
//       if (pythonError instanceof Error) {
//         console.log('Python backend not available (this is ok):', pythonError.message)
//       } else {
//         console.log('Python backend not available (this is ok):', pythonError)
//       }
//     }
    
//     return NextResponse.json({
//       success: true,
//       message: 'Upload successful, detection started',
//       data: { 
//         name,
//         targetPath: 'current_target.jpg',
//         timestamp: new Date().toISOString()
//       }
//     })
    
//   } catch (error) {
//     console.error('Upload error:', error)
//     return NextResponse.json(
//       { error: 'Failed to process upload', details: (error as Error).message },
//       { status: 500 }
//     )
//   }
// }








// import { NextResponse } from 'next/server'
// import fs from 'fs'
// import path from 'path'
// import { processUploads } from '@/lib/face-recognition'

// export async function POST(req: Request) {
//   try {
//     const formData = await req.formData()
//     const file = formData.get('primaryPhoto') as File
//     const name = formData.get('name') as string
    
//     if (!file) {
//       return NextResponse.json(
//         { error: 'No file provided' },
//         { status: 400 }
//       )
//     }

//     console.log('Processing upload:', { fileName: file.name, name })
    
//     // Create directories if they don't exist
//     const targetsDir = path.join(process.cwd(), 'python-backend', 'targets')
//     if (!fs.existsSync(targetsDir)) {
//       fs.mkdirSync(targetsDir, { recursive: true })
//     }
    
//     // Save the uploaded file for Python backend
//     const buffer = Buffer.from(await file.arrayBuffer())
//     const targetPath = path.join(targetsDir, 'current_target.jpg')
//     fs.writeFileSync(targetPath, buffer)
    
//     console.log('File saved to:', targetPath)
    
//     // Also process with face-api.js (optional - for enhanced features)
//     let faceData = null
//     try {
//       faceData = await processUploads(formData)
//       console.log('Face processing successful:', faceData.name)
//     } catch (faceError) {
//       if (faceError instanceof Error) {
//         console.log('Face-api processing failed (using basic detection):', faceError.message)
//       } else {
//         console.log('Face-api processing failed (using basic detection):', String(faceError))
//       }
//     }
    
//     // Try to start detection via Python backend
//     try {
//       const pythonApiUrl = process.env.PYTHON_API_URL || 'http://localhost:5000'
//       const response = await fetch(`${pythonApiUrl}/start_detection`, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' }
//       })
      
//       if (response.ok) {
//         const data = await response.json()
//         console.log('Python backend response:', data)
//       }
//     } catch (pythonError) {
//       if (pythonError instanceof Error) {
//         console.log('Python backend not available, detection will start automatically:', pythonError.message)
//       } else {
//         console.log('Python backend not available, detection will start automatically:', String(pythonError))
//       }
//     }
    
//     return NextResponse.json({
//       success: true,
//       message: 'Upload successful, detection started',
//       data: { 
//         name,
//         targetPath: 'current_target.jpg',
//         timestamp: new Date().toISOString(),
//         faceData: faceData?.metadata || null
//       }
//     })
    
//   } catch (error) {
//     console.error('Upload error:', error)
//     return NextResponse.json(
//       { 
//         error: 'Failed to process upload', 
//         details: error instanceof Error ? error.message : String(error) 
//       },
//       { status: 500 }
//     )
//   }
// }



// firease store 


import { NextResponse } from "next/server"
import fs from "fs"
import path from "path"
import { db, storage } from "@/lib/firebase"
import { collection, addDoc, Timestamp } from "firebase/firestore"
import { ref, uploadBytes, getDownloadURL } from "firebase/storage"

export async function POST(req: Request) {
  try {
    const formData = await req.formData()
    const file = formData.get("primaryPhoto") as File
    const name = formData.get("name") as string
    const lastLocation = (formData.get("lastLocation") as string) || ""

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 })
    }

    console.log("Processing upload:", { fileName: file.name, name })

    // Create directories if they don't exist - Updated path
    const targetsDir = path.join(process.cwd(), "python", "detector", "targets")
    if (!fs.existsSync(targetsDir)) {
      fs.mkdirSync(targetsDir, { recursive: true })
    }

    // Save the uploaded file for Python backend
    const buffer = Buffer.from(await file.arrayBuffer())
    const targetPath = path.join(targetsDir, "current_target.jpg")
    fs.writeFileSync(targetPath, buffer)

    // Save metadata for Python backend - Updated path
    const metadata = {
      name,
      lastLocation,
      timestamp: new Date().toISOString(),
      fileName: file.name,
    }
    const metadataPath = path.join(targetsDir, "metadata.json")
    fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2))

    console.log("File saved to:", targetPath)

    // Upload to Firebase Storage
    try {
      const storageRef = ref(storage, `missing-persons/${Date.now()}_${file.name}`)
      const uploadResult = await uploadBytes(storageRef, buffer)
      const downloadURL = await getDownloadURL(uploadResult.ref)

      // Save missing person data to Firestore
      const missingPersonData = {
        name,
        lastLocation,
        primaryPhotoUrl: downloadURL,
        timestamp: Timestamp.now(),
        status: "active",
        fileName: file.name,
        targetPath: "current_target.jpg",
      }

      const docRef = await addDoc(collection(db, "missing_persons"), missingPersonData)
      console.log("Missing person saved to Firebase:", docRef.id)
    } catch (firebaseError) {
      console.error("Firebase upload error:", firebaseError)
      // Continue even if Firebase fails
    }

    // Try to start detection via Python backend
    try {
      const pythonApiUrl = process.env.PYTHON_API_URL || "http://localhost:5000"
      const response = await fetch(`${pythonApiUrl}/start_detection`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      })

      if (response.ok) {
        const data = await response.json()
        console.log("Python backend response:", data)
      }
    } catch (pythonError) {
      console.log("Python backend not available, detection will start automatically")
    }

    return NextResponse.json({
      success: true,
      message: "Upload successful, detection started",
      data: {
        name,
        targetPath: "current_target.jpg",
        timestamp: new Date().toISOString(),
      },
    })
  } catch (error) {
    console.error("Upload error:", error)
    return NextResponse.json(
      {
        error: "Failed to process upload",
        details: error instanceof Error ? error.message : String(error),
      },
      { status: 500 },
    )
  }
}
