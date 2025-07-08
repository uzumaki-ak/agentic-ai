// import * as faceapi from 'face-api.js'

// export async function createFaceEncoding(file: File) {
//   const image = await faceapi.bufferToImage(file)
//   const detections = await faceapi
//     .detectSingleFace(image)
//     .withFaceLandmarks()
//     .withFaceDescriptor()
    
//   if (!detections) throw new Error('No face detected')
//   return Array.from(detections.descriptor)
// }

// export async function processUploads(formData: FormData) {
//   const name = formData.get('name') as string
//   const primaryPhoto = formData.get('primaryPhoto') as File
//   const profilePhoto = formData.get('profilePhoto') as File | null
//   const altPhoto = formData.get('altPhoto') as File | null
  
//   // Load face-api models
//   await faceapi.nets.tinyFaceDetector.loadFromUri('/models')
//   await faceapi.nets.faceLandmark68Net.loadFromUri('/models')
//   await faceapi.nets.faceRecognitionNet.loadFromUri('/models')
  
//   const encodings = [
//     await createFaceEncoding(primaryPhoto),
//     ...(profilePhoto ? [await createFaceEncoding(profilePhoto)] : []),
//     ...(altPhoto ? [await createFaceEncoding(altPhoto)] : [])
//   ]
  
//   return {
//     name,
//     encodings,
//     metadata: {
//       lastLocation: formData.get('lastLocation') || '',
//       timestamp: new Date().toISOString()
//     }
//   }
// }





// import * as faceapi from '@vladmandic/face-api';
// import path from 'path';
// import fs from 'fs';
// import { Image, Canvas, ImageData } from 'canvas';

// faceapi.env.monkeyPatch({ Canvas: Canvas as any, Image: Image as any, ImageData: ImageData as any });

// export async function createFaceEncoding(buffer: Buffer) {
//   const img = await canvasLoadImage(buffer);
//   const detection = await faceapi
//     .detectSingleFace(img as any)
//     .withFaceLandmarks()
//     .withFaceDescriptor();

//   if (!detection) throw new Error('No face detected');
//   return Array.from(detection.descriptor);
// }

// async function canvasLoadImage(buffer: Buffer): Promise<Canvas> {
//   const img = new Image();
//   img.src = buffer;
//   const canvas = new Canvas(img.width, img.height);
//   const ctx = canvas.getContext('2d');
//   ctx.drawImage(img, 0, 0);
//   return canvas;
// }

// export async function processUploads(formData: FormData) {
//   const name = formData.get('name') as string;
//   const primary = formData.get('primaryPhoto') as File;
//   const profile = formData.get('profilePhoto') as File | null;
//   const alt = formData.get('altPhoto') as File | null;

//   const buffer = Buffer.from(await primary.arrayBuffer());
//   const buffer2 = profile ? Buffer.from(await profile.arrayBuffer()) : null;
//   const buffer3 = alt ? Buffer.from(await alt.arrayBuffer()) : null;

//   const modelPath = path.join(process.cwd(), 'models'); // ⬅️ models folder (see below)

//   // Load models from disk (once per function call for simplicity)
//   await faceapi.nets.ssdMobilenetv1.loadFromDisk(modelPath);
//   await faceapi.nets.faceLandmark68Net.loadFromDisk(modelPath);
//   await faceapi.nets.faceRecognitionNet.loadFromDisk(modelPath);

//   const encodings = [
//     await createFaceEncoding(buffer),
//     ...(buffer2 ? [await createFaceEncoding(buffer2)] : []),
//     ...(buffer3 ? [await createFaceEncoding(buffer3)] : []),
//   ];

//   return {
//     name,
//     encodings,
//     metadata: {
//       lastLocation: formData.get('lastLocation') || '',
//       timestamp: new Date().toISOString(),
//     },
//   };
// }









import * as faceapi from 'face-api.js'

export async function createFaceEncoding(file: File) {
  const image = await faceapi.bufferToImage(file)
  const detections = await faceapi
    .detectSingleFace(image)
    .withFaceLandmarks()
    .withFaceDescriptor()
    
  if (!detections) throw new Error('No face detected')
  return Array.from(detections.descriptor)
}

export async function processUploads(formData: FormData) {
  const name = formData.get('name') as string
  const primaryPhoto = formData.get('primaryPhoto') as File
  const profilePhoto = formData.get('profilePhoto') as File | null
  const altPhoto = formData.get('altPhoto') as File | null
  
  if (!primaryPhoto) {
    throw new Error('Primary photo is required')
  }
  
  try {
    // Load face-api models
    await faceapi.nets.tinyFaceDetector.loadFromUri('/models')
    await faceapi.nets.faceLandmark68Net.loadFromUri('/models')
    await faceapi.nets.faceRecognitionNet.loadFromUri('/models')
    
    const encodings = [
      await createFaceEncoding(primaryPhoto),
      ...(profilePhoto ? [await createFaceEncoding(profilePhoto)] : []),
      ...(altPhoto ? [await createFaceEncoding(altPhoto)] : [])
    ]
    
    return {
      name,
      encodings,
      metadata: {
        lastLocation: formData.get('lastLocation') || '',
        timestamp: new Date().toISOString(),
        photosCount: encodings.length
      }
    }
  } catch (error) {
    console.error('Face processing error:', error)
    if (error instanceof Error) {
      throw new Error(`Failed to process face: ${error.message}`)
    } else {
      throw new Error('Failed to process face: Unknown error')
    }
  }
}