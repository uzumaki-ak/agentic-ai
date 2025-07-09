# import cv2
# import numpy as np
# import os
# import json
# import requests
# from datetime import datetime
# from camera_processor import CameraProcessor

# # Load face detection model (no dlib required)
# face_proto = "deploy.prototxt.txt"
# face_model = "res10_300x300_ssd_iter_140000.caffemodel"
# face_net = cv2.dnn.readNetFromCaffe(face_proto, face_model)

# # Load face recognition model
# recognizer = cv2.face.LBPHFaceRecognizer_create()

# class FaceDetector:
#     def __init__(self, target_faces):
#         self.target_faces = target_faces
#         self.last_detection = None
#         self.cooldown = 30  # seconds
    
#     def detect_faces(self, frame):
#         (h, w) = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(
#             cv2.resize(frame, (300, 300)), 
#             1.0, 
#             (300, 300),
#             (104.0, 177.0, 123.0)
#         )
        
#         face_net.setInput(blob)
#         detections = face_net.forward()
#         faces = []
        
#         for i in range(0, detections.shape[2]):
#             confidence = detections[0, 0, i, 2]
#             if confidence > 0.7:  # Confidence threshold
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 (startX, startY, endX, endY) = box.astype("int")
#                 face = frame[startY:endY, startX:endX]
#                 faces.append(face)
                
#         return faces
    
#     def recognize_face(self, face):
#         # Convert to grayscale for recognition
#         gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        
#         for name, target_face in self.target_faces.items():
#             # Simple histogram comparison (replace with more advanced method)
#             hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
#             target_hist = cv2.calcHist([target_face], [0], None, [256], [0, 256])
            
#             # Compare histograms
#             match = cv2.compareHist(hist, target_hist, cv2.HISTCMP_CORREL)
            
#             if match > 0.8:  # Similarity threshold
#                 return name, match
        
#         return None, 0
    
#     def process_frame(self, frame):
#         faces = self.detect_faces(frame)
        
#         for face in faces:
#             name, confidence = self.recognize_face(face)
#             if name:
#                 # Check cooldown
#                 current_time = datetime.now()
#                 if (self.last_detection and 
#                    (current_time - self.last_detection).seconds < self.cooldown):
#                     continue
                
#                 self.last_detection = current_time
#                 timestamp = current_time.isoformat()
#                 snapshot_path = f"snapshots/match_{timestamp.replace(':', '-')}.jpg"
#                 cv2.imwrite(snapshot_path, frame)
                
#                 return {
#                     "name": name,
#                     "timestamp": timestamp,
#                     "confidence": confidence * 100,
#                     "snapshot_path": snapshot_path
#                 }
#         return None

# def start_detection(target_faces):
#     detector = FaceDetector(target_faces)
#     processor = CameraProcessor(os.getenv("CAMERA_URL"))
    
#     print(f"🚀 Starting detection for camera: {os.getenv('CAMERA_NAME')}")
#     for frame in processor.stream():
#         result = detector.process_frame(frame)
#         if result:
#             print(f"✅ Match found! Confidence: {result['confidence']:.2f}%")
#             # Send alert to Next.js
#             requests.post(
#                 os.getenv("NEXTJS_API_URL") + "/api/alerts",
#                 json={
#                     **result,
#                     "location": os.getenv("CAMERA_NAME"),
#                     "latitude": json.loads(os.getenv("CAMERA_LOCATION"))["lat"],
#                     "longitude": json.loads(os.getenv("CAMERA_LOCATION"))["lng"]
#                 }
#             )

# if __name__ == "__main__":
#     # Example target faces (load from uploaded images)
#     target_faces = {
#         "John Doe": cv2.imread("targets/john.jpg", cv2.IMREAD_GRAYSCALE),
#         "Jane Smith": cv2.imread("targets/jane.jpg", cv2.IMREAD_GRAYSCALE)
#     }
#     start_detection(target_faces)


# !new


# import cv2
# import numpy as np
# import os
# import json
# import requests
# from datetime import datetime
# from camera_processor import CameraProcessor
# import time
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Ensure directories exist
# os.makedirs("targets", exist_ok=True)
# os.makedirs("snapshots", exist_ok=True)

# class FaceDetector:
#     def __init__(self):
#         # Load face detection model with absolute paths
#         model_dir = os.path.dirname(os.path.abspath(__file__))
#         self.face_net = cv2.dnn.readNetFromCaffe(
#             os.path.join(model_dir, "deploy.prototxt"),
#             os.path.join(model_dir, "res10_300x300_ssd_iter_140000.caffemodel")
#         )
#         self.target_face = None
#         self.last_detection = None
#         self.cooldown = 30  # seconds

#     def set_target_face(self, image_path):
#         """Set target face from uploaded image"""
#         image = cv2.imread(image_path)
#         if image is not None:
#             self.target_face = self._extract_face(image)
#             return True
#         return False

#     def _extract_face(self, image):
#         """Extract largest face from image"""
#         (h, w) = image.shape[:2]
#         blob = cv2.dnn.blobFromImage(
#             cv2.resize(image, (300, 300)), 
#             1.0, (300, 300),
#             (104.0, 177.0, 123.0)
#         )
#         self.face_net.setInput(blob)
#         detections = self.face_net.forward()
        
#         best_face = None
#         best_confidence = 0
        
#         for i in range(0, detections.shape[2]):
#             confidence = detections[0, 0, i, 2]
#             if confidence > 0.7 and confidence > best_confidence:
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 (startX, startY, endX, endY) = box.astype("int")
#                 face = image[startY:endY, startX:endX]
#                 best_face = cv2.resize(face, (100, 100))  # Standard size
#                 best_confidence = confidence
                
#         return best_face

#     def process_frame(self, frame):
#         """Process frame to find target face"""
#         if self.target_face is None:
#             return None

#         (h, w) = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(
#             cv2.resize(frame, (300, 300)), 
#             1.0, (300, 300),
#             (104.0, 177.0, 123.0)
#         )
#         self.face_net.setInput(blob)
#         detections = self.face_net.forward()
        
#         for i in range(0, detections.shape[2]):
#             confidence = detections[0, 0, i, 2]
#             if confidence > 0.7:  # Confidence threshold
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 (startX, startY, endX, endY) = box.astype("int")
#                 face = frame[startY:endY, startX:endX]
                
#                 # Simple comparison
#                 if face.size > 0 and self.target_face.size > 0:
#                     try:
#                         face = cv2.resize(face, (100, 100))
#                         difference = cv2.absdiff(self.target_face, face)
#                         similarity = 100 - (np.mean(difference) / 2.55)
                        
#                         if similarity > 70:  # Similarity threshold
#                             current_time = datetime.now()
#                             if (self.last_detection and 
#                                (current_time - self.last_detection).seconds < self.cooldown):
#                                 continue
                            
#                             self.last_detection = current_time
#                             timestamp = current_time.isoformat()
#                             snapshot_path = f"snapshots/match_{timestamp.replace(':', '-')}.jpg"
#                             cv2.imwrite(snapshot_path, frame)
                            
#                             return {
#                                 "timestamp": timestamp,
#                                 "confidence": similarity,
#                                 "snapshot_path": snapshot_path
#                             }
#                     except cv2.error as e:
#                         print(f"Face processing error: {e}")
#         return None

# def wait_for_upload():
#     """Wait for frontend to upload target image"""
#     print("⏳ Waiting for target face upload...")
#     while True:
#         try:
#             target_path = os.path.join("targets", "current_target.jpg")
#             if os.path.exists(target_path):
#                 return target_path
#         except Exception as e:
#             print(f"Upload check error: {e}")
#         time.sleep(1)

# def start_detection():
#     detector = FaceDetector()
    
#     # Get camera URL from environment
#     camera_url = os.getenv("CAMERA_URL")
#     if not camera_url:
#         print("❌ Error: CAMERA_URL not set in .env file")
#         return

#     processor = CameraProcessor(camera_url)
    
#     # Wait for frontend upload
#     target_path = wait_for_upload()
#     if not detector.set_target_face(target_path):
#         print("❌ Failed to load target face")
#         return

#     print(f"🚀 Starting detection for camera: {os.getenv('CAMERA_NAME')}")
#     try:
#         for frame in processor.stream():
#             result = detector.process_frame(frame)
#             if result:
#                 print(f"✅ Match found! Confidence: {result['confidence']:.2f}%")
#                 alert_data = {
#                     **result,
#                     "location": os.getenv("CAMERA_NAME", "Unknown Camera"),
#                     "latitude": json.loads(os.getenv("CAMERA_LOCATION", '{"lat":0,"lng":0}'))["lat"],
#                     "longitude": json.loads(os.getenv("CAMERA_LOCATION", '{"lat":0,"lng":0}'))["lng"],
#                     "snapshotUrl": f"/snapshots/{os.path.basename(result['snapshot_path'])}"
#                 }
                
#                 # Send to Next.js API
#                 requests.post(
#                     f"{os.getenv('NEXTJS_API_URL', 'http://localhost:3000')}/api/alerts",
#                     json=alert_data
#                 )
#     except KeyboardInterrupt:
#         print("🛑 Detection stopped by user")
#     finally:
#         processor.stop()

# if __name__ == "__main__":
#     start_detection()


# !new prev is good

# import cv2
# import numpy as np
# import os
# import json
# import requests
# from datetime import datetime
# from camera_processor import CameraProcessor
# import time
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Ensure directories exist
# os.makedirs("targets", exist_ok=True)
# os.makedirs("snapshots", exist_ok=True)

# class FaceDetector:
#     def __init__(self):
#         # Load face detection model with absolute paths
#         model_dir = os.path.dirname(os.path.abspath(__file__))
#         self.face_net = cv2.dnn.readNetFromCaffe(
#             os.path.join(model_dir, "deploy.prototxt"),
#             os.path.join(model_dir, "res10_300x300_ssd_iter_140000.caffemodel")
#         )
#         self.target_face = None
#         self.last_detection = None
#         self.cooldown = 30  # seconds

#     def set_target_face(self, image_path):
#         """Set target face from uploaded image"""
#         image = cv2.imread(image_path)
#         if image is None:
#             print(f"❌ Failed to read target image at {image_path}")
#             return False

#         # Extract and set target face
#         self.target_face = self._extract_face(image)
#         # After extracting face
#         if self.target_face is None:
#             print("⚠️ No face found in target image")
#         else:
#             print(f"✅ Target face extracted: {self.target_face.shape}")
#             cv2.imwrite("debug_target_face.jpg", self.target_face)
#         return True

#     def _extract_face(self, image):
#         """Extract largest face from image"""
#         (h, w) = image.shape[:2]
#         blob = cv2.dnn.blobFromImage(
#             cv2.resize(image, (300, 300)), 
#             1.0, (300, 300),
#             (104.0, 177.0, 123.0)
#         )
#         self.face_net.setInput(blob)
#         detections = self.face_net.forward()
        
#         best_face = None
#         best_confidence = 0
        
#         for i in range(0, detections.shape[2]):
#             confidence = detections[0, 0, i, 2]
#             if confidence > 0.7 and confidence > best_confidence:
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 (startX, startY, endX, endY) = box.astype("int")
#                 face = image[startY:endY, startX:endX]
#                 best_face = cv2.resize(face, (100, 100))  # Standard size
#                 best_confidence = confidence
                
#         return best_face

#     def process_frame(self, frame):
#         """Process frame to find target face"""
#         # Check for invalid frame
#         if frame is None:
#             print("⚠️ Empty frame received")
#             return None

#         if self.target_face is None:
#             return None

#         (h, w) = frame.shape[:2]
#         blob = cv2.dnn.blobFromImage(
#             cv2.resize(frame, (300, 300)), 
#             1.0, (300, 300),
#             (104.0, 177.0, 123.0)
#         )
#         self.face_net.setInput(blob)
#         detections = self.face_net.forward()
        
#         for i in range(0, detections.shape[2]):
#             confidence = detections[0, 0, i, 2]
#             if confidence > 0.7:  # Confidence threshold
#                 box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
#                 (startX, startY, endX, endY) = box.astype("int")
#                 face = frame[startY:endY, startX:endX]

#                 # Skip empty face regions
#                 if face.size == 0:
#                     print("⚠️ Empty face region detected")
#                     continue
                
#                 # Simple comparison
#                 if self.target_face.size > 0:
#                     try:
#                         face = cv2.resize(face, (100, 100))
#                         difference = cv2.absdiff(self.target_face, face)
#                         similarity = 100 - (np.mean(difference) / 2.55)
                        
#                         if similarity > 70:  # Similarity threshold
#                             current_time = datetime.now()
#                             if (self.last_detection and 
#                                (current_time - self.last_detection).seconds < self.cooldown):
#                                 continue
                            
#                             self.last_detection = current_time
#                             timestamp = current_time.isoformat()
#                             snapshot_path = f"snapshots/match_{timestamp.replace(':', '-')}.jpg"
#                             cv2.imwrite(snapshot_path, frame)
                            
#                             return {
#                                 "timestamp": timestamp,
#                                 "confidence": similarity,
#                                 "snapshot_path": snapshot_path
#                             }
#                     except cv2.error as e:
#                         print(f"Face processing error: {e}")
#         return None

# def wait_for_upload():
#     """Wait for frontend to upload target image"""
#     print("⏳ Waiting for target face upload...")
#     while True:
#         try:
#             target_path = os.path.join("targets", "current_target.jpg")
#             if os.path.exists(target_path):
#                 return target_path
#         except Exception as e:
#             print(f"Upload check error: {e}")
#         time.sleep(1)

# def start_detection():
#     detector = FaceDetector()
    
#     # Get camera URL from environment
#     camera_url = os.getenv("CAMERA_URL")
#     if not camera_url:
#         print("❌ Error: CAMERA_URL not set in .env file")
#         return

#     processor = CameraProcessor(camera_url)
    
#     # Wait for frontend upload
#     target_path = wait_for_upload()
#     if not detector.set_target_face(target_path):
#         print("❌ Failed to load target face")
#         return

#     print(f"🚀 Starting detection for camera: {os.getenv('CAMERA_NAME')}")
#     try:
#         for frame in processor.stream():
#             result = detector.process_frame(frame)
#             if result:
#                 print(f"✅ Match found! Confidence: {result['confidence']:.2f}%")
#                 alert_data = {
#                     **result,
#                     "location": os.getenv("CAMERA_NAME", "Unknown Camera"),
#                     "latitude": json.loads(os.getenv("CAMERA_LOCATION", "{'lat':0,'lng':0}"))["lat"],
#                     "longitude": json.loads(os.getenv("CAMERA_LOCATION", "{'lat':0,'lng':0}"))["lng"],
#                     "snapshotUrl": f"/snapshots/{os.path.basename(result['snapshot_path'])}"
#                 }
                
#                 # Send to Next.js API
#                 requests.post(
#                     f"{os.getenv('NEXTJS_API_URL', 'http://localhost:3000')}/api/alerts",
#                     json=alert_data
#                 )
#     except KeyboardInterrupt:
#         print("🛑 Detection stopped by user")
#     finally:
#         processor.stop()

# if __name__ == "__main__":
#     start_detection()


# !new prev is good++

# import cv2
# import numpy as np
# import os
# import json
# import requests
# from datetime import datetime
# import time
# import mediapipe as mp
# from camera_processor import RequestCameraProcessor  # We'll create this
# import google.generativeai as genai
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Initialize MediaPipe Face Detection
# mp_face_detection = mp.solutions.face_detection
# mp_face_mesh = mp.solutions.face_mesh
# face_detection = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5)
# face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, min_detection_confidence=0.5)

# # Initialize Gemini
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# if GEMINI_API_KEY:
#     genai.configure(api_key=GEMINI_API_KEY)
#     vision_model = genai.GenerativeModel('gemini-pro-vision')

# class FaceRecognizer:
#     def __init__(self):
#         self.target_embedding = None
#         self.target_image = None
#         self.last_detection = None
#         self.cooldown = 30  # seconds
#         self.threshold = 0.8  # Similarity threshold

#     def set_target_face(self, image_path):
#         """Set target face from uploaded image"""
#         self.target_image = cv2.imread(image_path)
#         if self.target_image is not None:
#             self.target_embedding = self._get_face_embedding(self.target_image)
#             return True
#         return False

#     def _get_face_embedding(self, image):
#         """Get face embedding using MediaPipe"""
#         # Convert to RGB
#         rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
#         # Detect face landmarks
#         results = face_mesh.process(rgb_image)
        
#         if results.multi_face_landmarks:
#             # Get face landmarks
#             landmarks = results.multi_face_landmarks[0].landmark
            
#             # Create embedding from key landmarks
#             embedding = []
#             for landmark in [landmarks[1], landmarks[33], landmarks[61], landmarks[199], landmarks[291], landmarks[62]]:
#                 embedding.extend([landmark.x, landmark.y, landmark.z])
                
#             return np.array(embedding)
#         return None

#     def _compare_faces(self, embedding1, embedding2):
#         """Calculate cosine similarity between embeddings"""
#         if embedding1 is None or embedding2 is None:
#             return 0
            
#         dot_product = np.dot(embedding1, embedding2)
#         norm1 = np.linalg.norm(embedding1)
#         norm2 = np.linalg.norm(embedding2)
#         return dot_product / (norm1 * norm2)

#     def process_frame(self, frame):
#         """Process frame to find target face"""
#         if self.target_embedding is None:
#             return None

#         # Convert to RGB for MediaPipe
#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
#         # Detect faces
#         results = face_detection.process(rgb_frame)
        
#         if results.detections:
#             for detection in results.detections:
#                 # Extract face bounding box
#                 bboxC = detection.location_data.relative_bounding_box
#                 ih, iw, _ = frame.shape
#                 x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
#                               int(bboxC.width * iw), int(bboxC.height * ih)
                
#                 # Expand the bounding box a bit
#                 x, y, w, h = max(0, x-10), max(0, y-10), min(iw, w+20), min(ih, h+20)
#                 face_roi = frame[y:y+h, x:x+w]
                
#                 # Get embedding for detected face
#                 face_embedding = self._get_face_embedding(face_roi)
                
#                 if face_embedding is not None:
#                     # Compare with target
#                     similarity = self._compare_faces(self.target_embedding, face_embedding)
                    
#                     if similarity > self.threshold:
#                         current_time = datetime.now()
#                         if (self.last_detection and 
#                            (current_time - self.last_detection).seconds < self.cooldown):
#                             continue
                        
#                         self.last_detection = current_time
#                         timestamp = current_time.isoformat()
#                         snapshot_path = f"snapshots/match_{timestamp.replace(':', '-')}.jpg"
#                         cv2.imwrite(snapshot_path, frame)
                        
#                         # Generate AI description if available
#                         ai_description = ""
#                         if GEMINI_API_KEY:
#                             try:
#                                 prompt = "Describe this person's appearance including gender, approximate age, clothing, accessories, and distinctive features."
#                                 response = vision_model.generate_content([
#                                     prompt,
#                                     genai.types.Image(cv2.imencode('.jpg', face_roi)[1].tobytes())
#                                 ])
#                                 ai_description = response.text
#                             except Exception as e:
#                                 print(f"Gemini error: {str(e)}")
#                             except Exception as e:
#                                 print(f"Gemini error: {str(e)}")
                        
#                         return {
#                             "timestamp": timestamp,
#                             "confidence": similarity * 100,
#                             "snapshot_path": snapshot_path,
#                             "ai_description": ai_description,
#                             "face_roi": face_roi  # For debugging
#                         }
#         return None

# def start_detection():
#     recognizer = FaceRecognizer()
    
#     # Wait for frontend upload
#     target_path = os.path.join("targets", "current_target.jpg")
#     while not os.path.exists(target_path):
#         print("⏳ Waiting for target face upload...")
#         time.sleep(1)
    
#     if not recognizer.set_target_face(target_path):
#         print("❌ Failed to load target face")
#         return

#     # Get camera URL from environment
#     camera_url = os.getenv("CAMERA_URL")
#     if not camera_url:
#         print("❌ Error: CAMERA_URL not set in .env file")
#         return

#     processor = RequestCameraProcessor(camera_url)
    
#     print(f"🚀 Starting detection for camera: {os.getenv('CAMERA_NAME')}")
#     try:
#         for frame in processor.stream():
#             result = recognizer.process_frame(frame)
#             if result:
#                 print(f"✅ Match found! Confidence: {result['confidence']:.2f}%")
#                 alert_data = {
#                     "timestamp": result["timestamp"],
#                     "confidence": result["confidence"],
#                     "snapshot_path": result["snapshot_path"],
#                     "location": os.getenv("CAMERA_NAME", "Unknown Camera"),
#                     "latitude": json.loads(os.getenv("CAMERA_LOCATION", '{"lat":0,"lng":0}'))["lat"],
#                     "longitude": json.loads(os.getenv("CAMERA_LOCATION", '{"lat":0,"lng":0}'))["lng"],
#                     "ai_description": result.get("ai_description", "")
#                 }
                
#                 # Send to Next.js API
#                 requests.post(
#                     f"{os.getenv('NEXTJS_API_URL', 'http://localhost:3000')}/api/alerts",
#                     json=alert_data
#                 )
#     except KeyboardInterrupt:
#         print("🛑 Detection stopped by user")
#     finally:
#         processor.stop()

# if __name__ == "__main__":
#     # Create necessary directories
#     os.makedirs("targets", exist_ok=True)
#     os.makedirs("snapshots", exist_ok=True)
#     start_detection()


#! new deepface lib

# import cv2
# import numpy as np
# import os
# import json
# import requests
# from datetime import datetime
# from camera_processor import CameraProcessor
# import time
# from dotenv import load_dotenv
# from deepface import DeepFace
# import logging

# # Suppress DeepFace warnings
# logging.getLogger('deepface').setLevel(logging.ERROR)

# # Load environment variables
# load_dotenv()

# # Ensure directories exist
# os.makedirs("targets", exist_ok=True)
# os.makedirs("snapshots", exist_ok=True)

# class DeepFaceDetector:
#     def __init__(self):
#         self.target_image_path = None
#         self.last_detection = None
#         self.cooldown = 30  # seconds
        
#         # DeepFace parameters
#         self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
#         self.detection_backend = os.getenv("DETECTION_BACKEND", "opencv")
#         self.recognition_model = os.getenv("RECOGNITION_MODEL", "VGG-Face")
        
#         # Available models: VGG-Face, Facenet, OpenFace, DeepFace, DeepID, ArcFace
#         print(f"🤖 Using model: {self.recognition_model}")
#         print(f"📊 Similarity threshold: {self.similarity_threshold}")

#     def set_target_face(self, image_path):
#         """Set target face image"""
#         if not os.path.exists(image_path):
#             print(f"❌ Target image not found: {image_path}")
#             return False
        
#         try:
#             # Test if DeepFace can detect face in target image
#             result = DeepFace.analyze(
#                 img_path=image_path,
#                 actions=['age'],  # Simple test
#                 detector_backend=self.detection_backend,
#                 enforce_detection=True
#             )
            
#             self.target_image_path = image_path
#             print("✅ Target face set successfully")
#             print(f"📷 Target analysis: Age ~{result[0]['age']}")
#             return True
            
#         except Exception as e:
#             print(f"❌ Error setting target face: {e}")
#             return False

#     def process_frame(self, frame):
#         """Process frame to find target face"""
#         if frame is None or self.target_image_path is None:
#             return None

#         try:
#             # Save current frame temporarily
#             temp_frame_path = "temp_frame.jpg"
#             cv2.imwrite(temp_frame_path, frame)
            
#             # Use DeepFace to verify faces
#             result = DeepFace.verify(
#                 img1_path=self.target_image_path,
#                 img2_path=temp_frame_path,
#                 model_name=self.recognition_model,
#                 detector_backend=self.detection_backend,
#                 enforce_detection=False  # Don't fail if no face detected
#             )
            
#             # Clean up temp file
#             if os.path.exists(temp_frame_path):
#                 os.remove(temp_frame_path)
            
#             # Check if faces match
#             if result['verified'] and result['distance'] < (1 - self.similarity_threshold):
#                 similarity = (1 - result['distance']) * 100
                
#                 print(f"🔍 Face similarity: {similarity:.1f}%")
                
#                 # Check cooldown
#                 current_time = datetime.now()
#                 if (self.last_detection and 
#                    (current_time - self.last_detection).seconds < self.cooldown):
#                     print("⏳ Cooldown active, skipping detection")
#                     return None
                
#                 self.last_detection = current_time
#                 timestamp = current_time.isoformat()
#                 snapshot_path = f"snapshots/match_{timestamp.replace(':', '-')}.jpg"
                
#                 # Save snapshot
#                 cv2.imwrite(snapshot_path, frame)
                
#                 return {
#                     "timestamp": timestamp,
#                     "confidence": similarity,
#                     "snapshot_path": snapshot_path,
#                     "distance": result['distance'],
#                     "method": "DeepFace"
#                 }
                
#         except Exception as e:
#             # This is normal when no face is detected
#             if "Face could not be detected" not in str(e):
#                 print(f"⚠️ Processing error: {e}")
            
#         return None

# def wait_for_upload():
#     """Wait for frontend to upload target image"""
#     print("⏳ Waiting for target face upload...")
#     while True:
#         try:
#             target_path = os.path.join("targets", "current_target.jpg")
#             if os.path.exists(target_path):
#                 return target_path
#         except Exception as e:
#             print(f"Upload check error: {e}")
#         time.sleep(1)

# def start_detection():
#     detector = DeepFaceDetector()
    
#     # Get camera URL from environment
#     camera_url = os.getenv("CAMERA_URL")
#     if not camera_url:
#         print("❌ Error: CAMERA_URL not set in .env file")
#         return

#     processor = CameraProcessor(camera_url)
    
#     # Wait for frontend upload
#     target_path = wait_for_upload()
#     if not detector.set_target_face(target_path):
#         print("❌ Failed to load target face")
#         return

#     print(f"🚀 Starting DeepFace detection")
#     print(f"📷 Camera: {os.getenv('CAMERA_NAME', 'Unknown')}")
    
#     try:
#         frame_count = 0
#         for frame in processor.stream():
#             frame_count += 1
            
#             # Process every 5th frame for better performance
#             if frame_count % 5 != 0:
#                 continue
                
#             result = detector.process_frame(frame)
#             if result:
#                 print(f"🎯 MATCH DETECTED!")
#                 print(f"   Confidence: {result['confidence']:.1f}%")
#                 print(f"   Distance: {result['distance']:.3f}")
#                 print(f"   Snapshot: {result['snapshot_path']}")
                
#                 alert_data = {
#                     **result,
#                     "location": os.getenv("CAMERA_NAME", "Unknown Camera"),
#                     "latitude": json.loads(os.getenv("CAMERA_LOCATION", "{'lat':0,'lng':0}"))["lat"],
#                     "longitude": json.loads(os.getenv("CAMERA_LOCATION", "{'lat':0,'lng':0}"))["lng"],
#                     "snapshotUrl": f"/snapshots/{os.path.basename(result['snapshot_path'])}"
#                 }
                
#                 # Send to Next.js API
#                 try:
#                     response = requests.post(
#                         f"{os.getenv('NEXTJS_API_URL', 'http://localhost:3000')}/api/alerts",
#                         json=alert_data,
#                         timeout=5
#                     )
#                     if response.status_code == 200:
#                         print("✅ Alert sent to frontend")
#                     else:
#                         print(f"⚠️ Alert failed: {response.status_code}")
#                 except Exception as e:
#                     print(f"❌ Failed to send alert: {e}")
                    
#     except KeyboardInterrupt:
#         print("🛑 Detection stopped by user")
#     finally:
#         processor.stop()

# if __name__ == "__main__":
#     start_detection()


# gemini



# import cv2
# import numpy as np
# import os
# import json
# import requests
# from datetime import datetime
# from camera_processor import CameraProcessor
# import time
# from dotenv import load_dotenv
# import base64
# import google.generativeai as genai
# from PIL import Image
# import io

# # Load environment variables
# load_dotenv()

# # Configure Gemini
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Ensure directories exist
# os.makedirs("targets", exist_ok=True)
# os.makedirs("snapshots", exist_ok=True)

# class GeminiFaceDetector:
#     def __init__(self):
#         self.target_image_path = None
#         self.target_description = None
#         self.last_detection = None
#         self.cooldown = 30  # seconds
        
#         # Initialize Gemini model
#         self.model = genai.GenerativeModel('gemini-1.5-flash')
        
#         print(f"🤖 Using Gemini AI Face Recognition")
#         print(f"📊 Cooldown: {self.cooldown} seconds")

#     def image_to_base64(self, image_path):
#         """Convert image to base64 for Gemini API"""
#         try:
#             with open(image_path, "rb") as image_file:
#                 return base64.b64encode(image_file.read()).decode('utf-8')
#         except Exception as e:
#             print(f"❌ Error converting image: {e}")
#             return None

#     def frame_to_pil(self, frame):
#         """Convert OpenCV frame to PIL Image"""
#         try:
#             # Convert BGR to RGB
#             rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             return Image.fromarray(rgb_frame)
#         except Exception as e:
#             print(f"❌ Error converting frame: {e}")
#             return None

#     def set_target_face(self, image_path):
#         """Set target face image and get description from Gemini"""
#         if not os.path.exists(image_path):
#             print(f"❌ Target image not found: {image_path}")
#             return False
        
#         try:
#             # Load target image
#             target_image = Image.open(image_path)
            
#             # Get detailed description from Gemini
#             prompt = """
#             Analyze this person's face very carefully and provide a detailed description including:
#             1. Gender (male/female)
#             2. Approximate age range
#             3. Hair color and style
#             4. Eye color if visible
#             5. Facial structure (round/oval/square face)
#             6. Any distinctive features (glasses, beard, mustache, etc.)
#             7. Skin tone
#             8. Any visible accessories
            
#             Be very specific and detailed as this will be used for person identification.
#             """
            
#             response = self.model.generate_content([prompt, target_image])
#             self.target_description = response.text
#             self.target_image_path = image_path
            
#             print("✅ Target face set successfully")
#             print(f"📝 Target description: {self.target_description[:200]}...")
#             return True
            
#         except Exception as e:
#             print(f"❌ Error setting target face: {e}")
#             return False

#     def process_frame(self, frame):
#         """Process frame to find target face using Gemini"""
#         if frame is None or self.target_description is None:
#             return None

#         try:
#             # Convert frame to PIL Image
#             frame_image = self.frame_to_pil(frame)
#             if frame_image is None:
#                 return None
            
#             # Create comparison prompt
#             comparison_prompt = f"""
#             I'm looking for a specific person. Here is the detailed description of the target person:
            
#             {self.target_description}
            
#             Please analyze the current image and determine:
#             1. Are there any people visible in this image?
#             2. If yes, does any person match the target description above?
#             3. Provide a confidence score (0-100) for any potential matches
#             4. Explain your reasoning
            
#             Respond in JSON format:
#             {{
#                 "people_detected": true/false,
#                 "match_found": true/false,
#                 "confidence": 0-100,
#                 "reasoning": "explanation",
#                 "match_details": "specific details about the match"
#             }}
#             """
            
#             # Get analysis from Gemini
#             response = self.model.generate_content([comparison_prompt, frame_image])
#             result_text = response.text
            
#             # Extract JSON from response
#             try:
#                 # Clean up the response to extract JSON
#                 if "```json" in result_text:
#                     json_start = result_text.find("```json") + 7
#                     json_end = result_text.find("```", json_start)
#                     result_text = result_text[json_start:json_end]
                
#                 result = json.loads(result_text)
                
#                 if result.get("match_found", False) and result.get("confidence", 0) > 70:
#                     confidence = result.get("confidence", 0)
                    
#                     print(f"🔍 Gemini analysis confidence: {confidence}%")
#                     print(f"📝 Reasoning: {result.get('reasoning', 'N/A')}")
                    
#                     # Check cooldown
#                     current_time = datetime.now()
#                     if (self.last_detection and 
#                        (current_time - self.last_detection).seconds < self.cooldown):
#                         print("⏳ Cooldown active, skipping detection")
#                         return None
                    
#                     self.last_detection = current_time
#                     timestamp = current_time.isoformat()
#                     snapshot_path = f"snapshots/match_{timestamp.replace(':', '-')}.jpg"
                    
#                     # Save snapshot
#                     cv2.imwrite(snapshot_path, frame)
                    
#                     return {
#                         "timestamp": timestamp,
#                         "confidence": confidence,
#                         "snapshot_path": snapshot_path,
#                         "reasoning": result.get("reasoning", ""),
#                         "match_details": result.get("match_details", ""),
#                         "method": "Gemini"
#                     }
                    
#             except json.JSONDecodeError:
#                 print(f"⚠️ Could not parse Gemini response: {result_text}")
                
#         except Exception as e:
#             print(f"⚠️ Gemini processing error: {e}")
            
#         return None

# def wait_for_upload():
#     """Wait for frontend to upload target image"""
#     print("⏳ Waiting for target face upload...")
#     while True:
#         try:
#             target_path = os.path.join("targets", "current_target.jpg")
#             if os.path.exists(target_path):
#                 return target_path
#         except Exception as e:
#             print(f"Upload check error: {e}")
#         time.sleep(1)

# def start_detection():
#     detector = GeminiFaceDetector()
    
#     # Get camera URL from environment
#     camera_url = os.getenv("CAMERA_URL")
#     if not camera_url:
#         print("❌ Error: CAMERA_URL not set in .env file")
#         return

#     processor = CameraProcessor(camera_url)
    
#     # Wait for frontend upload
#     target_path = wait_for_upload()
#     if not detector.set_target_face(target_path):
#         print("❌ Failed to load target face")
#         return

#     print(f"🚀 Starting Gemini detection")
#     print(f"📷 Camera: {os.getenv('CAMERA_NAME', 'Unknown')}")
    
#     try:
#         frame_count = 0
#         for frame in processor.stream():
#             frame_count += 1
            
#             # Process every 10th frame for Gemini (API rate limits)
#             if frame_count % 10 != 0:
#                 continue
                
#             result = detector.process_frame(frame)
#             if result:
#                 print(f"🎯 MATCH DETECTED!")
#                 print(f"   Confidence: {result['confidence']:.1f}%")
#                 print(f"   Reasoning: {result['reasoning']}")
#                 print(f"   Snapshot: {result['snapshot_path']}")
                
#                 alert_data = {
#                     **result,
#                     "location": os.getenv("CAMERA_NAME", "Unknown Camera"),
#                     "latitude": json.loads(os.getenv("CAMERA_LOCATION", "{'lat':0,'lng':0}"))["lat"],
#                     "longitude": json.loads(os.getenv("CAMERA_LOCATION", "{'lat':0,'lng':0}"))["lng"],
#                     "snapshotUrl": f"/snapshots/{os.path.basename(result['snapshot_path'])}"
#                 }
                
#                 # Send to Flask API
#                 try:
#                     response = requests.post(
#                         f"{os.getenv('FLASK_API_URL', 'http://localhost:5000')}/api/alerts",
#                         json=alert_data,
#                         timeout=5
#                     )
#                     if response.status_code == 200:
#                         print("✅ Alert sent to frontend")
#                     else:
#                         print(f"⚠️ Alert failed: {response.status_code}")
#                 except Exception as e:
#                     print(f"❌ Failed to send alert: {e}")
                    
#     except KeyboardInterrupt:
#         print("🛑 Detection stopped by user")
#     finally:
#         processor.stop()

# if __name__ == "__main__":
#     start_detection()


#!!!!! firebade strng


import cv2
import numpy as np
import os
import json
import requests
from datetime import datetime
from camera_processor import CameraProcessor
import time
from dotenv import load_dotenv
import base64
import google.generativeai as genai
from PIL import Image
import io
from firebase_client import firebase_client

# Load environment variables from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Ensure directories exist
os.makedirs("targets", exist_ok=True)
os.makedirs("snapshots", exist_ok=True)

class GeminiFaceDetector:
    def __init__(self):
        self.target_image_path = None
        self.target_description = None
        self.last_detection = None
        self.cooldown = 30  # seconds
        self.current_target_name = "Unknown Person"
        
        # Initialize Gemini model
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        print(f"🤖 Using Gemini AI Face Recognition")
        print(f"📊 Cooldown: {self.cooldown} seconds")

    def frame_to_pil(self, frame):
        """Convert OpenCV frame to PIL Image"""
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return Image.fromarray(rgb_frame)
        except Exception as e:
            print(f"❌ Error converting frame: {e}")
            return None

    def set_target_face(self, image_path, person_name="Unknown Person"):
        """Set target face image and get description from Gemini"""
        if not os.path.exists(image_path):
            print(f"❌ Target image not found: {image_path}")
            return False
        
        try:
            target_image = Image.open(image_path)
            self.current_target_name = person_name
            
            prompt = """
            Analyze this person's face very carefully and provide a detailed description including:
            1. Gender (male/female)
            2. Approximate age range
            3. Hair color and style
            4. Eye color if visible
            5. Facial structure (round/oval/square face)
            6. Any distinctive features (glasses, beard, mustache, etc.)
            7. Skin tone
            8. Any visible accessories
            
            Be very specific and detailed as this will be used for person identification.
            """
            
            response = self.model.generate_content([prompt, target_image])
            self.target_description = response.text
            self.target_image_path = image_path
            
            print("✅ Target face set successfully")
            print(f"📝 Target description: {self.target_description[:200]}...")
            return True
            
        except Exception as e:
            print(f"❌ Error setting target face: {e}")
            return False

    def process_frame(self, frame):
        """Process frame to find target face using Gemini"""
        if frame is None or self.target_description is None:
            return None
        
        try:
            frame_image = self.frame_to_pil(frame)
            if frame_image is None:
                return None
            
            comparison_prompt = f"""
            I'm looking for a specific person. Here is the detailed description of the target person:
            
            {self.target_description}
            
            Please analyze the current image and determine:
            1. Are there any people visible in this image?
            2. If yes, does any person match the target description above?
            3. Provide a confidence score (0-100) for any potential matches
            4. Explain your reasoning
            
            Respond in JSON format:
            {{
                "people_detected": true/false,
                "match_found": true/false,
                "confidence": 0-100,
                "reasoning": "explanation",
                "match_details": "specific details about the match"
            }}
            """
            
            response = self.model.generate_content([comparison_prompt, frame_image])
            result_text = response.text
            
            try:
                if "```json" in result_text:
                    json_start = result_text.find("```json") + 7
                    json_end = result_text.find("```", json_start)
                    result_text = result_text[json_start:json_end]
                
                result = json.loads(result_text)
                
                if result.get("match_found", False) and result.get("confidence", 0) > 70:
                    confidence = result.get("confidence", 0)
                    
                    print(f"🔍 Gemini analysis confidence: {confidence}%")
                    print(f"📝 Reasoning: {result.get('reasoning', 'N/A')}")
                    
                    # Check cooldown
                    current_time = datetime.now()
                    if (self.last_detection and
                        (current_time - self.last_detection).seconds < self.cooldown):
                        print("⏳ Cooldown active, skipping detection")
                        return None
                    
                    self.last_detection = current_time
                    timestamp = current_time.isoformat()
                    snapshot_filename = f"match_{timestamp.replace(':', '-')}.jpg"
                    snapshot_path = f"snapshots/{snapshot_filename}"
                    
                    # Save snapshot locally
                    cv2.imwrite(snapshot_path, frame)
                    
                    # Upload to Firebase Storage
                    remote_path = f"matched_frames/{snapshot_filename}"
                    image_url = firebase_client.upload_image(snapshot_path, remote_path)
                    
                    if not image_url:
                        print("⚠️ Failed to upload image to Firebase")
                        image_url = f"/snapshots/{snapshot_filename}"
                    
                    return {
                        "timestamp": timestamp,
                        "confidence": confidence,
                        "snapshot_path": snapshot_path,
                        "image_url": image_url,
                        "reasoning": result.get("reasoning", ""),
                        "match_details": result.get("match_details", ""),
                        "method": "Gemini",
                        "person_name": self.current_target_name
                    }
                    
            except json.JSONDecodeError:
                print(f"⚠️ Could not parse Gemini response: {result_text}")
                
        except Exception as e:
            print(f"⚠️ Gemini processing error: {e}")
        
        return None

def wait_for_upload():
    """Wait for frontend to upload target image"""
    print("⏳ Waiting for target face upload...")
    while True:
        try:
            target_path = os.path.join("targets", "current_target.jpg")
            if os.path.exists(target_path):
                return target_path
        except Exception as e:
            print(f"Upload check error: {e}")
        time.sleep(1)

def start_detection():
    detector = GeminiFaceDetector()
    
    # Get camera URL from environment
    camera_url = os.getenv("CAMERA_URL")
    if not camera_url:
        print("❌ Error: CAMERA_URL not set in .env file")
        return
    
    processor = CameraProcessor(camera_url)
    
    # Wait for frontend upload
    target_path = wait_for_upload()
    
    # Try to get person name from a metadata file
    person_name = "Unknown Person"
    try:
        metadata_path = os.path.join("targets", "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                person_name = metadata.get('name', 'Unknown Person')
    except:
        pass
    
    if not detector.set_target_face(target_path, person_name):
        print("❌ Failed to load target face")
        return
    
    print(f"🚀 Starting Gemini detection for: {person_name}")
    print(f"📷 Camera: {os.getenv('CAMERA_NAME', 'Unknown')}")
    
    try:
        frame_count = 0
        for frame in processor.stream():
            frame_count += 1
            
            # Process every 10th frame for Gemini (API rate limits)
            if frame_count % 10 != 0:
                continue
            
            result = detector.process_frame(frame)
            if result:
                print(f"🎯 MATCH DETECTED!")
                print(f"   Person: {result['person_name']}")
                print(f"   Confidence: {result['confidence']:.1f}%")
                print(f"   Reasoning: {result['reasoning']}")
                print(f"   Snapshot: {result['snapshot_path']}")
                
                # Get camera location
                try:
                    camera_location = json.loads(os.getenv("CAMERA_LOCATION", '{"lat":28.6129,"lng":77.2295}'))
                except:
                    camera_location = {"lat": 28.6129, "lng": 77.2295}
                
                # Prepare detection data for Firebase
                detection_data = {
                    "timestamp": datetime.fromisoformat(result['timestamp'].replace('Z', '+00:00')),
                    "lat": float(camera_location["lat"]),
                    "lng": float(camera_location["lng"]),
                    "image_url": result['image_url'],
                    "camera_id": os.getenv('CAMERA_NAME', 'unknown-camera'),
                    "person_name": result['person_name'],
                    "confidence": result['confidence'],
                    "reasoning": result['reasoning'],
                    "match_details": result['match_details'],
                    "method": result['method'],
                    "status": "active"
                }
                
                # Save to Firebase
                detection_id = firebase_client.save_detection(detection_data)
                
                # Prepare alert data for frontend
                alert_data = {
                    "type": "NEW_ALERT",
                    "alert": {
                        "id": detection_id or str(int(time.time())),
                        "name": result['person_name'],
                        "timestamp": result['timestamp'],
                        "location": {
                            "lat": camera_location["lat"],
                            "lng": camera_location["lng"]
                        },
                        "confidence": result['confidence'],
                        "snapshotUrl": result['image_url'],
                        "aiDescription": result['reasoning'],
                        "severity": "high" if result['confidence'] > 85 else "medium",
                        "anomaly_type": "person_found",
                        "zone": os.getenv('CAMERA_NAME', 'Unknown Zone'),
                        "description": f"Missing person {result['person_name']} detected with {result['confidence']:.1f}% confidence",
                        "resolved": False
                    }
                }
                
                # Send to Next.js API
                try:
                    # Send to alerts API
                    alerts_response = requests.post(
                        f"{os.getenv('NEXT_PUBLIC_APP_URL', 'http://localhost:3000')}/api/alerts",
                        json=alert_data["alert"],
                        timeout=5
                    )
                    
                    # Broadcast via SSE
                    broadcast_response = requests.post(
                        f"{os.getenv('NEXT_PUBLIC_APP_URL', 'http://localhost:3000')}/api/stream/broadcast",
                        json=alert_data,
                        timeout=5
                    )
                    
                    if alerts_response.status_code in [200, 201]:
                        print("✅ Alert sent to frontend")
                    else:
                        print(f"⚠️ Alert API failed: {alerts_response.status_code}")
                    
                    if broadcast_response.status_code == 200:
                        print("✅ Alert broadcasted via SSE")
                    else:
                        print(f"⚠️ Broadcast failed: {broadcast_response.status_code}")
                        
                except Exception as e:
                    print(f"❌ Failed to send alert: {e}")
                
    except KeyboardInterrupt:
        print("🛑 Detection stopped by user")
    finally:
        processor.stop()

if __name__ == "__main__":
    start_detection()
