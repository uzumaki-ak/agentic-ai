# import cv2
# import base64
# import json
# import time
# import requests
# import os
# from datetime import datetime
# import firebase_admin
# from firebase_admin import credentials, firestore, storage
# import google.generativeai as genai
# import io
# from PIL import Image
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# def initialize_firebase():
#     """Initialize Firebase Admin SDK"""
#     if not firebase_admin._apps:
#         try:
#             # Create credentials from environment variables
#             cred_dict = {
#                 "type": "service_account",
#                 "project_id": os.getenv('FIREBASE_PROJECT_ID'),
#                 "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
#                 "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
#                 "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
#                 "client_id": os.getenv('FIREBASE_CLIENT_ID'),
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://oauth2.googleapis.com/token",
#             }
            
#             cred = credentials.Certificate(cred_dict)
#             firebase_admin.initialize_app(cred, {
#                 'storageBucket': os.getenv('NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET')
#             })
#             print("✅ Firebase Admin SDK initialized successfully")
#         except Exception as e:
#             print(f"❌ Firebase initialization error: {e}")
#             return None
    
#     return firestore.client()

# def initialize_gemini():
#     """Initialize Gemini AI with free tier model"""
#     try:
#         genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
#         # Using free tier model gemini-1.5-flash
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         print("✅ Gemini AI initialized successfully (Free Tier)")
#         return model
#     except Exception as e:
#         print(f"❌ Gemini initialization error: {e}")
#         return None

# def send_email_alert(alert_data):
#     """Send email alert using Resend API"""
#     try:
#         resend_api_key = os.getenv('RESEND_API_KEY')
#         if not resend_api_key:
#             print("⚠️ No Resend API key found, skipping email")
#             return
        
#         url = "https://api.resend.com/emails"
#         headers = {
#             "Authorization": f"Bearer {resend_api_key}",
#             "Content-Type": "application/json"
#         }
        
#         # Create email with rich HTML content
#         severity_colors = {
#             'low': '#22c55e',
#             'medium': '#f59e0b', 
#             'high': '#ef4444'
#         }
        
#         severity_emojis = {
#             'low': '🟢',
#             'medium': '🟡',
#             'high': '🔴'
#         }
        
#         anomaly_emojis = {
#             'fire': '🔥',
#             'smoke': '💨',
#             'crowd_panic': '👥',
#             'suspicious_activity': '👁️',
#             'violence': '⚡'
#         }
        
#         data = {
#             "from": os.getenv('ALERT_EMAIL_FROM', 'alerts@drishti.ai'),
#             "to": [os.getenv('ALERT_EMAIL_TO', 'security@example.com')],
#             "subject": f"🚨 DRISHTI ALERT: {alert_data['anomaly_type'].replace('_', ' ').title()} Detected",
#             "html": f"""
#             <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8fafc; padding: 20px;">
#                 <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
#                     <h1 style="margin: 0; font-size: 24px;">🔍 Project Drishti Security Alert</h1>
#                     <p style="margin: 5px 0 0 0; opacity: 0.9;">Real-time Anomaly Detection System</p>
#                 </div>
                
#                 <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
#                     <div style="background: {severity_colors[alert_data['severity']]}; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
#                         <h2 style="margin: 0; font-size: 20px;">
#                             {anomaly_emojis.get(alert_data['anomaly_type'], '⚠️')} {alert_data['anomaly_type'].replace('_', ' ').upper()} DETECTED
#                         </h2>
#                         <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">
#                             {severity_emojis[alert_data['severity']]} {alert_data['severity'].upper()} SEVERITY
#                         </p>
#                     </div>
                    
#                     <div style="margin-bottom: 20px;">
#                         <h3 style="color: #374151; margin-bottom: 10px;">📋 Alert Details</h3>
#                         <table style="width: 100%; border-collapse: collapse;">
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Description:</td>
#                                 <td style="padding: 8px 0; color: #374151;">{alert_data['description']}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Confidence:</td>
#                                 <td style="padding: 8px 0; color: #374151;">{alert_data['confidence']:.1%}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Location:</td>
#                                 <td style="padding: 8px 0; color: #374151;">📍 {alert_data['zone']}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Camera:</td>
#                                 <td style="padding: 8px 0; color: #374151;">📹 {alert_data['camera']}</td>
#                             </tr>
#                             <tr>
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Time:</td>
#                                 <td style="padding: 8px 0; color: #374151;">⏰ {alert_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</td>
#                             </tr>
#                         </table>
#                     </div>
                    
#                     {f'''
#                     <div style="text-align: center; margin: 20px 0;">
#                         <a href="{alert_data['snapshot_url']}" 
#                            style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; 
#                                   text-decoration: none; border-radius: 6px; font-weight: bold;">
#                             📸 View Snapshot Image
#                         </a>
#                     </div>
#                     ''' if alert_data.get('snapshot_url') else ''}
                    
#                     <div style="background: #f3f4f6; padding: 15px; border-radius: 6px; margin-top: 20px;">
#                         <p style="margin: 0; font-size: 14px; color: #6b7280;">
#                             🤖 This alert was automatically generated by Project Drishti's AI-powered video analysis system.
#                             Please investigate and take appropriate action if necessary.
#                         </p>
#                     </div>
#                 </div>
                
#                 <div style="text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px;">
#                     <p>Project Drishti - Intelligent Security Monitoring</p>
#                 </div>
#             </div>
#             """
#         }
        
#         response = requests.post(url, headers=headers, json=data)
#         if response.status_code == 200:
#             print("📧 Email alert sent successfully")
#         else:
#             print(f"❌ Failed to send email: {response.status_code} - {response.text}")
            
#     except Exception as e:
#         print(f"❌ Error sending email: {e}")

# def capture_and_analyze():
#     """Main function to capture video and analyze for anomalies"""
#     print("🚀 Starting Project Drishti Video Processor...")
    
#     # Initialize services
#     db = initialize_firebase()
#     model = initialize_gemini()
    
#     if not db or not model:
#         print("❌ Failed to initialize required services. Exiting...")
#         return
    
#     # Connect to camera stream
#     camera_url = os.getenv('CAMERA_STREAM_URL', 'http://192.168.31.220:8080/video')
#     print(f"📹 Connecting to camera: {camera_url}")
    
#     cap = cv2.VideoCapture(camera_url)
    
#     if not cap.isOpened():
#         print(f"❌ Error: Could not connect to camera at {camera_url}")
#         print("💡 Make sure IP Webcam app is running on your phone")
#         return
    
#     print("✅ Connected to camera stream successfully!")
#     print("🔍 Starting real-time anomaly detection...")
#     print("⏰ Processing 1 frame every 5 seconds...")
    
#     frame_count = 0
    
#     while True:
#         try:
#             # Capture frame
#             ret, frame = cap.read()
#             if not ret:
#                 print("⚠️ Failed to capture frame, retrying...")
#                 time.sleep(5)
#                 continue
            
#             frame_count += 1
#             print(f"\n📸 Processing frame #{frame_count}...")
            
#             # Convert frame to PIL Image for Gemini
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             pil_image = Image.fromarray(frame_rgb)
            
#             # Enhanced prompt for better anomaly detection
#             prompt = """
#             You are an advanced AI security analyst. Analyze this surveillance image for potential security threats and anomalies.

#             Look specifically for:
#             🔥 FIRE: Any flames, burning objects, or fire-related incidents
#             💨 SMOKE: Visible smoke, haze, or burning indicators  
#             👥 CROWD PANIC: Unusual crowd behavior, running, panic, overcrowding
#             👁️ SUSPICIOUS ACTIVITY: Unusual behavior, potential threats, unauthorized access
#             ⚡ VIOLENCE: Fighting, aggressive behavior, weapons, physical altercations
            
#             Respond ONLY in valid JSON format:
#             {
#                 "anomaly_detected": true/false,
#                 "anomaly_type": "fire|smoke|crowd_panic|suspicious_activity|violence|none",
#                 "confidence": 0.0-1.0,
#                 "description": "Detailed description of what you observe",
#                 "severity": "low|medium|high",
#                 "zone": "Brief description of the area/location in the image"
#             }
            
#             Be precise and only flag genuine security concerns. Normal activities should return anomaly_detected: false.
#             """
            
#             # Send to Gemini Vision API
#             response = model.generate_content([prompt, pil_image])
            
#             # Parse response
#             try:
#                 response_text = response.text.strip()
                
#                 # Clean JSON response
#                 if response_text.startswith('```json'):
#                     response_text = response_text[7:-3]
#                 elif response_text.startswith('```'):
#                     response_text = response_text[3:-3]
                
#                 analysis = json.loads(response_text)
                
#                 print(f"🤖 AI Analysis Complete:")
#                 print(f"   Anomaly Detected: {analysis.get('anomaly_detected', False)}")
#                 print(f"   Type: {analysis.get('anomaly_type', 'none')}")
#                 print(f"   Confidence: {analysis.get('confidence', 0):.1%}")
                
#                 # If anomaly detected, process and store
#                 if analysis.get('anomaly_detected', False):
#                     print(f"🚨 ANOMALY DETECTED: {analysis['anomaly_type']} (Severity: {analysis.get('severity', 'medium')})")
                    
#                     # Upload frame to Firebase Storage
#                     try:
#                         bucket = storage.bucket()
#                         timestamp = datetime.now().isoformat().replace(':', '-')
#                         filename = f"anomalies/{timestamp}_{analysis['anomaly_type']}.jpg"
                        
#                         # Convert frame to bytes
#                         _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
#                         blob = bucket.blob(filename)
#                         blob.upload_from_string(buffer.tobytes(), content_type='image/jpeg')
#                         blob.make_public()
                        
#                         snapshot_url = blob.public_url
#                         print(f"📸 Snapshot uploaded: {snapshot_url}")
                        
#                     except Exception as e:
#                         print(f"⚠️ Failed to upload snapshot: {e}")
#                         snapshot_url = None
                    
#                     # Prepare alert data for Firestore
#                     alert_data = {
#                         'timestamp': datetime.now(),
#                         'anomaly_type': analysis.get('anomaly_type', 'unknown'),
#                         'confidence': float(analysis.get('confidence', 0.0)),
#                         'description': analysis.get('description', 'Anomaly detected'),
#                         'severity': analysis.get('severity', 'medium'),
#                         'zone': analysis.get('zone', 'Zone A - Mobile Camera'),
#                         'camera': 'zone-a-mobile-cam',
#                         'location': {
#                             'lat': float(os.getenv('NEXT_PUBLIC_DEFAULT_LAT', 28.6139)),
#                             'lng': float(os.getenv('NEXT_PUBLIC_DEFAULT_LNG', 77.2090))
#                         },
#                         'snapshot_url': snapshot_url,
#                         'resolved': False
#                     }
                    
#                     # Store in Firestore
#                     try:
#                         doc_ref = db.collection('alerts').add(alert_data)
#                         print(f"💾 Alert stored in Firestore with ID: {doc_ref[1].id}")
                        
#                         # Send email notification
#                         send_email_alert(alert_data)
                        
#                     except Exception as e:
#                         print(f"❌ Failed to store alert in Firestore: {e}")
                
#                 else:
#                     print("✅ No anomalies detected - All clear")
                    
#             except json.JSONDecodeError as e:
#                 print(f"❌ Error parsing Gemini response: {e}")
#                 print(f"Raw response: {response.text}")
#             except Exception as e:
#                 print(f"❌ Error processing Gemini response: {e}")
            
#         except Exception as e:
#             print(f"❌ Error in main processing loop: {e}")
#             print("🔄 Continuing monitoring...")
        
#         # Wait 5 seconds before next capture
#         print("⏳ Waiting 5 seconds before next frame...")
#         time.sleep(5)

# if __name__ == "__main__":
#     print("🔍 Project Drishti - AI-Powered Video Anomaly Detection")
#     print("=" * 60)
    
#     # Check required environment variables
#     required_vars = [
#         'GEMINI_API_KEY',
#         'FIREBASE_PROJECT_ID', 
#         'FIREBASE_PRIVATE_KEY',
#         'FIREBASE_CLIENT_EMAIL',
#         'CAMERA_STREAM_URL'
#     ]
    
#     missing_vars = [var for var in required_vars if not os.getenv(var)]
    
#     if missing_vars:
#         print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
#         print("💡 Please check your .env file and ensure all variables are set")
#         exit(1)
    
#     try:
#         capture_and_analyze()
#     except KeyboardInterrupt:
#         print("\n🛑 Stopping video processor...")
#         print("👋 Goodbye!")
#     except Exception as e:
#         print(f"❌ Fatal error: {e}")


#! new
# 
# 

# import cv2
# import base64
# import json
# import time
# import requests
# import os
# from datetime import datetime
# import firebase_admin
# from firebase_admin import credentials, firestore, storage
# import google.generativeai as genai
# import io
# from PIL import Image
# from dotenv import load_dotenv
# import ssl
# import certifi
# import urllib3

# # Load environment variables
# load_dotenv()

# # Fix SSL certificate issues
# import os
# os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
# os.environ['SSL_CERT_FILE'] = certifi.where()

# # Disable SSL warnings
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# def initialize_firebase():
#     """Initialize Firebase Admin SDK with SSL fix"""
#     if not firebase_admin._apps:
#         try:
#             # Create credentials from environment variables
#             cred_dict = {
#                 "type": "service_account",
#                 "project_id": os.getenv('FIREBASE_PROJECT_ID'),
#                 "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
#                 "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
#                 "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
#                 "client_id": os.getenv('FIREBASE_CLIENT_ID'),
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://oauth2.googleapis.com/token",
#                 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#                 "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
#             }
            
#             cred = credentials.Certificate(cred_dict)
#             firebase_admin.initialize_app(cred, {
#                 'storageBucket': os.getenv('NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET')
#             })
#             print("✅ Firebase Admin SDK initialized successfully")
#         except Exception as e:
#             print(f"❌ Firebase initialization error: {e}")
#             return None
    
#     return firestore.client()

# def initialize_gemini():
#     """Initialize Gemini AI with free tier model"""
#     try:
#         genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
#         # Using free tier model gemini-1.5-flash
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         print("✅ Gemini AI initialized successfully (Free Tier)")
#         return model
#     except Exception as e:
#         print(f"❌ Gemini initialization error: {e}")
#         return None

# def send_email_alert(alert_data):
#     """Send email alert using Resend API"""
#     try:
#         resend_api_key = os.getenv('RESEND_API_KEY')
#         if not resend_api_key:
#             print("⚠️ No Resend API key found, skipping email")
#             return
        
#         url = "https://api.resend.com/emails"
#         headers = {
#             "Authorization": f"Bearer {resend_api_key}",
#             "Content-Type": "application/json"
#         }
        
#         # Create email with rich HTML content
#         severity_colors = {
#             'low': '#22c55e',
#             'medium': '#f59e0b', 
#             'high': '#ef4444'
#         }
        
#         severity_emojis = {
#             'low': '🟢',
#             'medium': '🟡',
#             'high': '🔴'
#         }
        
#         anomaly_emojis = {
#             'fire': '🔥',
#             'smoke': '💨',
#             'crowd_panic': '👥',
#             'suspicious_activity': '👁️',
#             'violence': '⚡'
#         }
        
#         data = {
#             "from": os.getenv('ALERT_EMAIL_FROM', 'alerts@drishti.ai'),
#             "to": [os.getenv('ALERT_EMAIL_TO', 'security@example.com')],
#             "subject": f"🚨 DRISHTI ALERT: {alert_data['anomaly_type'].replace('_', ' ').title()} Detected",
#             "html": f"""
#             <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8fafc; padding: 20px;">
#                 <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
#                     <h1 style="margin: 0; font-size: 24px;">🔍 Project Drishti Security Alert</h1>
#                     <p style="margin: 5px 0 0 0; opacity: 0.9;">Real-time Anomaly Detection System</p>
#                 </div>
                
#                 <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
#                     <div style="background: {severity_colors[alert_data['severity']]}; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
#                         <h2 style="margin: 0; font-size: 20px;">
#                             {anomaly_emojis.get(alert_data['anomaly_type'], '⚠️')} {alert_data['anomaly_type'].replace('_', ' ').upper()} DETECTED
#                         </h2>
#                         <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">
#                             {severity_emojis[alert_data['severity']]} {alert_data['severity'].upper()} SEVERITY
#                         </p>
#                     </div>
                    
#                     <div style="margin-bottom: 20px;">
#                         <h3 style="color: #374151; margin-bottom: 10px;">📋 Alert Details</h3>
#                         <table style="width: 100%; border-collapse: collapse;">
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Description:</td>
#                                 <td style="padding: 8px 0; color: #374151;">{alert_data['description']}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Confidence:</td>
#                                 <td style="padding: 8px 0; color: #374151;">{alert_data['confidence']:.1%}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Location:</td>
#                                 <td style="padding: 8px 0; color: #374151;">📍 {alert_data['zone']}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Camera:</td>
#                                 <td style="padding: 8px 0; color: #374151;">📹 {alert_data['camera']}</td>
#                             </tr>
#                             <tr>
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Time:</td>
#                                 <td style="padding: 8px 0; color: #374151;">⏰ {alert_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</td>
#                             </tr>
#                         </table>
#                     </div>
                    
#                     {f'''
#                     <div style="text-align: center; margin: 20px 0;">
#                         <a href="{alert_data['snapshot_url']}" 
#                            style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; 
#                                   text-decoration: none; border-radius: 6px; font-weight: bold;">
#                             📸 View Snapshot Image
#                         </a>
#                     </div>
#                     ''' if alert_data.get('snapshot_url') else ''}
                    
#                     <div style="background: #f3f4f6; padding: 15px; border-radius: 6px; margin-top: 20px;">
#                         <p style="margin: 0; font-size: 14px; color: #6b7280;">
#                             🤖 This alert was automatically generated by Project Drishti's AI-powered video analysis system.
#                             Please investigate and take appropriate action if necessary.
#                         </p>
#                     </div>
#                 </div>
                
#                 <div style="text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px;">
#                     <p>Project Drishti - Intelligent Security Monitoring</p>
#                 </div>
#             </div>
#             """
#         }
        
#         response = requests.post(url, headers=headers, json=data)
#         if response.status_code == 200:
#             print("📧 Email alert sent successfully")
#         else:
#             print(f"❌ Failed to send email: {response.status_code} - {response.text}")
            
#     except Exception as e:
#         print(f"❌ Error sending email: {e}")

# def capture_and_analyze():
#     """Main function to capture video and analyze for anomalies"""
#     print("🚀 Starting Project Drishti Video Processor...")
    
#     # Initialize services
#     db = initialize_firebase()
#     model = initialize_gemini()
    
#     if not db or not model:
#         print("❌ Failed to initialize required services. Exiting...")
#         return
    
#     # Connect to camera stream
#     camera_url = os.getenv('CAMERA_STREAM_URL', 'http://192.168.31.220:8080/video')
#     print(f"📹 Connecting to camera: {camera_url}")
    
#     cap = cv2.VideoCapture(camera_url)
    
#     if not cap.isOpened():
#         print(f"❌ Error: Could not connect to camera at {camera_url}")
#         print("💡 Make sure IP Webcam app is running on your phone")
#         return
    
#     print("✅ Connected to camera stream successfully!")
#     print("🔍 Starting real-time anomaly detection...")
#     print("⏰ Processing 1 frame every 30 seconds to conserve API quota...")
    
#     frame_count = 0
#     consecutive_errors = 0
    
#     while True:
#         try:
#             # Capture frame
#             ret, frame = cap.read()
#             if not ret:
#                 print("⚠️ Failed to capture frame, retrying...")
#                 time.sleep(5)
#                 continue
            
#             frame_count += 1
#             print(f"\n📸 Processing frame #{frame_count}...")
            
#             # Convert frame to PIL Image for Gemini
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             pil_image = Image.fromarray(frame_rgb)
            
#             # Enhanced prompt for better anomaly detection
#             prompt = """
#             You are an advanced AI security analyst. Analyze this surveillance image for potential security threats and anomalies.

#             Look specifically for:
#             🔥 FIRE: Any flames, burning objects, or fire-related incidents
#             💨 SMOKE: Visible smoke, haze, or burning indicators  
#             👥 CROWD PANIC: Unusual crowd behavior, running, panic, overcrowding
#             👁️ SUSPICIOUS ACTIVITY: Unusual behavior, potential threats, unauthorized access
#             ⚡ VIOLENCE: Fighting, aggressive behavior, weapons, physical altercations
            
#             Respond ONLY in valid JSON format without any markdown formatting:
#             {
#                 "anomaly_detected": true,
#                 "anomaly_type": "fire",
#                 "confidence": 0.95,
#                 "description": "Detailed description of what you observe",
#                 "severity": "high",
#                 "zone": "Brief description of the area/location in the image"
#             }
            
#             Be precise and only flag genuine security concerns. Normal activities should return anomaly_detected: false.
#             """
            
#             # Send to Gemini Vision API with error handling
#             try:
#                 response = model.generate_content([prompt, pil_image])
#                 consecutive_errors = 0  # Reset error counter on success
#             except Exception as api_error:
#                 if "429" in str(api_error) or "quota" in str(api_error).lower():
#                     print("⚠️ Gemini API quota exceeded. Waiting 60 seconds...")
#                     print("💡 Free tier allows 50 requests per day. Consider upgrading for production use.")
#                     time.sleep(60)
#                     continue
#                 else:
#                     raise api_error
            
#             # Parse response with improved cleaning
#             try:
#                 response_text = response.text.strip()
                
#                 # More robust JSON cleaning
#                 if response_text.startswith('```json'):
#                     response_text = response_text[7:]
#                 if response_text.startswith('```'):
#                     response_text = response_text[3:]
#                 if response_text.endswith('```'):
#                     response_text = response_text[:-3]
                
#                 # Remove any remaining backticks
#                 response_text = response_text.replace('```', '').strip()
                
#                 print(f"🧹 Cleaned response: {response_text[:100]}...")
                
#                 analysis = json.loads(response_text)
                
#                 print(f"🤖 AI Analysis Complete:")
#                 print(f"   Anomaly Detected: {analysis.get('anomaly_detected', False)}")
#                 print(f"   Type: {analysis.get('anomaly_type', 'none')}")
#                 print(f"   Confidence: {analysis.get('confidence', 0):.1%}")
                
#                 # If anomaly detected, process and store
#                 if analysis.get('anomaly_detected', False):
#                     print(f"🚨 ANOMALY DETECTED: {analysis['anomaly_type']} (Severity: {analysis.get('severity', 'medium')})")
                    
#                     # Upload frame to Firebase Storage
#                     try:
#                         bucket = storage.bucket()
#                         timestamp = datetime.now().isoformat().replace(':', '-')
#                         filename = f"anomalies/{timestamp}_{analysis['anomaly_type']}.jpg"
                        
#                         # Convert frame to bytes
#                         _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
#                         blob = bucket.blob(filename)
                        
#                         # Upload with retry mechanism
#                         try:
#                             blob.upload_from_string(buffer.tobytes(), content_type='image/jpeg')
#                             blob.make_public()
#                             snapshot_url = blob.public_url
#                             print(f"📸 Snapshot uploaded: {snapshot_url}")
#                         except Exception as upload_error:
#                             print(f"⚠️ Upload failed, saving locally: {upload_error}")
#                             # Save locally as backup
#                             local_path = f"snapshots/{filename}"
#                             os.makedirs("snapshots", exist_ok=True)
#                             cv2.imwrite(local_path, frame)
#                             snapshot_url = f"local://{local_path}"
#                             print(f"📸 Snapshot saved locally: {local_path}")
                            
#                     except Exception as e:
#                         print(f"⚠️ Failed to process snapshot: {e}")
#                         snapshot_url = None
                    
#                     # Prepare alert data for Firestore
#                     alert_data = {
#                         'timestamp': datetime.now(),
#                         'anomaly_type': analysis.get('anomaly_type', 'unknown'),
#                         'confidence': float(analysis.get('confidence', 0.0)),
#                         'description': analysis.get('description', 'Anomaly detected'),
#                         'severity': analysis.get('severity', 'medium'),
#                         'zone': analysis.get('zone', 'Zone A - Mobile Camera'),
#                         'camera': 'zone-a-mobile-cam',
#                         'location': {
#                             'lat': float(os.getenv('NEXT_PUBLIC_DEFAULT_LAT', 28.6139)),
#                             'lng': float(os.getenv('NEXT_PUBLIC_DEFAULT_LNG', 77.2090))
#                         },
#                         'snapshot_url': snapshot_url,
#                         'resolved': False
#                     }
                    
#                     # Store in Firestore
#                     try:
#                         doc_ref = db.collection('alerts').add(alert_data)
#                         print(f"💾 Alert stored in Firestore with ID: {doc_ref[1].id}")
                        
#                         # Send email notification
#                         send_email_alert(alert_data)
                        
#                     except Exception as e:
#                         print(f"❌ Failed to store alert in Firestore: {e}")
                
#                 else:
#                     print("✅ No anomalies detected - All clear")
                    
#             except json.JSONDecodeError as e:
#                 print(f"❌ Error parsing Gemini response: {e}")
#                 print(f"Raw response: {response.text}")
#                 consecutive_errors += 1
                
#                 # If too many parsing errors, there might be a systematic issue
#                 if consecutive_errors >= 3:
#                     print("⚠️ Multiple parsing errors detected. Checking response format...")
#                     print(f"Full response: {response.text}")
#                     consecutive_errors = 0  # Reset to continue monitoring
                    
#             except Exception as e:
#                 print(f"❌ Error processing Gemini response: {e}")
            
#         except Exception as e:
#             print(f"❌ Error in main processing loop: {e}")
#             print("🔄 Continuing monitoring...")
        
#         # Wait 30 seconds to conserve API quota (instead of 5 seconds)
#         print("⏳ Waiting 30 seconds before next frame (quota conservation)...")
#         time.sleep(30)

# if __name__ == "__main__":
#     print("🔍 Project Drishti - AI-Powered Video Anomaly Detection")
#     print("=" * 60)
    
#     # Check required environment variables
#     required_vars = [
#         'GEMINI_API_KEY',
#         'FIREBASE_PROJECT_ID', 
#         'FIREBASE_PRIVATE_KEY',
#         'FIREBASE_CLIENT_EMAIL',
#         'CAMERA_STREAM_URL'
#     ]
    
#     missing_vars = [var for var in required_vars if not os.getenv(var)]
    
#     if missing_vars:
#         print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
#         print("💡 Please check your .env file and ensure all variables are set")
#         exit(1)
    
#     try:
#         capture_and_analyze()
#     except KeyboardInterrupt:
#         print("\n🛑 Stopping video processor...")
#         print("👋 Goodbye!")
#     except Exception as e:
#         print(f"❌ Fatal error: {e}")
 


# !new deep 

# import cv2
# import base64
# import json
# import time
# import requests
# import os
# from datetime import datetime
# import firebase_admin
# from firebase_admin import credentials, firestore, storage
# import google.generativeai as genai
# import io
# from PIL import Image
# from dotenv import load_dotenv
# import certifi
# import ssl

# # Load environment variables
# load_dotenv()

# # Configure SSL certificates globally
# os.environ["SSL_CERT_FILE"] = certifi.where()
# ssl_context = ssl.create_default_context(cafile=certifi.where())
# print(f"🔐 Using SSL certificates from: {certifi.where()}")

# def initialize_firebase():
#     """Initialize Firebase Admin SDK with SSL fix"""
#     if not firebase_admin._apps:
#         try:
#             # Create credentials from environment variables
#             cred_dict = {
#                 "type": "service_account",
#                 "project_id": os.getenv('FIREBASE_PROJECT_ID'),
#                 "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
#                 "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
#                 "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
#                 "client_id": os.getenv('FIREBASE_CLIENT_ID'),
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://oauth2.googleapis.com/token",
#                 "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#                 "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
#             }
            
#             cred = credentials.Certificate(cred_dict)
#             firebase_admin.initialize_app(cred, {
#                 'storageBucket': os.getenv('NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET'),
#                 'httpClientOptions': {
#                     'ssl_context': ssl_context  # Add custom SSL context
#                 }
#             })
#             print("✅ Firebase Admin SDK initialized successfully with SSL")
#             return firestore.client()
#         except Exception as e:
#             print(f"❌ Firebase initialization error: {e}")
#             return None
    
#     return firestore.client()

# def initialize_gemini():
#     """Initialize Gemini AI with free tier model"""
#     try:
#         genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
#         # Using free tier model gemini-1.5-flash
#         model = genai.GenerativeModel('gemini-1.5-flash')
#         print("✅ Gemini AI initialized successfully (Free Tier)")
#         return model
#     except Exception as e:
#         print(f"❌ Gemini initialization error: {e}")
#         return None

# def send_email_alert(alert_data):
#     """Send email alert using Resend API"""
#     try:
#         resend_api_key = os.getenv('RESEND_API_KEY')
#         if not resend_api_key:
#             print("⚠️ No Resend API key found, skipping email")
#             return
        
#         url = "https://api.resend.com/emails"
#         headers = {
#             "Authorization": f"Bearer {resend_api_key}",
#             "Content-Type": "application/json"
#         }
        
#         # Create email with rich HTML content
#         severity_colors = {
#             'low': '#22c55e',
#             'medium': '#f59e0b', 
#             'high': '#ef4444'
#         }
        
#         severity_emojis = {
#             'low': '🟢',
#             'medium': '🟡',
#             'high': '🔴'
#         }
        
#         anomaly_emojis = {
#             'fire': '🔥',
#             'smoke': '💨',
#             'crowd_panic': '👥',
#             'suspicious_activity': '👁️',
#             'violence': '⚡'
#         }
        
#         data = {
#             "from": os.getenv('ALERT_EMAIL_FROM', 'alerts@drishti.ai'),
#             "to": [os.getenv('ALERT_EMAIL_TO', 'security@example.com')],
#             "subject": f"🚨 DRISHTI ALERT: {alert_data['anomaly_type'].replace('_', ' ').title()} Detected",
#             "html": f"""
#             <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8fafc; padding: 20px;">
#                 <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
#                     <h1 style="margin: 0; font-size: 24px;">🔍 Project Drishti Security Alert</h1>
#                     <p style="margin: 5px 0 0 0; opacity: 0.9;">Real-time Anomaly Detection System</p>
#                 </div>
                
#                 <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
#                     <div style="background: {severity_colors[alert_data['severity']]}; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
#                         <h2 style="margin: 0; font-size: 20px;">
#                             {anomaly_emojis.get(alert_data['anomaly_type'], '⚠️')} {alert_data['anomaly_type'].replace('_', ' ').upper()} DETECTED
#                         </h2>
#                         <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">
#                             {severity_emojis[alert_data['severity']]} {alert_data['severity'].upper()} SEVERITY
#                         </p>
#                     </div>
                    
#                     <div style="margin-bottom: 20px;">
#                         <h3 style="color: #374151; margin-bottom: 10px;">📋 Alert Details</h3>
#                         <table style="width: 100%; border-collapse: collapse;">
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Description:</td>
#                                 <td style="padding: 8px 0; color: #374151;">{alert_data['description']}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Confidence:</td>
#                                 <td style="padding: 8px 0; color: #374151;">{alert_data['confidence']:.1%}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Location:</td>
#                                 <td style="padding: 8px 0; color: #374151;">📍 {alert_data['zone']}</td>
#                             </tr>
#                             <tr style="border-bottom: 1px solid #e5e7eb;">
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Camera:</td>
#                                 <td style="padding: 8px 0; color: #374151;">📹 {alert_data['camera']}</td>
#                             </tr>
#                             <tr>
#                                 <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Time:</td>
#                                 <td style="padding: 8px 0; color: #374151;">⏰ {alert_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</td>
#                             </tr>
#                         </table>
#                     </div>
                    
#                     {f'''
#                     <div style="text-align: center; margin: 20px 0;">
#                         <a href="{alert_data['snapshot_url']}" 
#                            style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; 
#                                   text-decoration: none; border-radius: 6px; font-weight: bold;">
#                             📸 View Snapshot Image
#                         </a>
#                     </div>
#                     ''' if alert_data.get('snapshot_url') else ''}
                    
#                     <div style="background: #f3f4f6; padding: 15px; border-radius: 6px; margin-top: 20px;">
#                         <p style="margin: 0; font-size: 14px; color: #6b7280;">
#                             🤖 This alert was automatically generated by Project Drishti's AI-powered video analysis system.
#                             Please investigate and take appropriate action if necessary.
#                         </p>
#                     </div>
#                 </div>
                
#                 <div style="text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px;">
#                     <p>Project Drishti - Intelligent Security Monitoring</p>
#                 </div>
#             </div>
#             """
#         }
        
#         response = requests.post(url, headers=headers, json=data)
#         if response.status_code == 200:
#             print("📧 Email alert sent successfully")
#         else:
#             print(f"❌ Failed to send email: {response.status_code} - {response.text}")
            
#     except Exception as e:
#         print(f"❌ Error sending email: {e}")

# def capture_and_analyze():
#     """Main function to capture video and analyze for anomalies"""
#     print("🚀 Starting Project Drishti Video Processor...")
    
#     # Initialize services
#     db = initialize_firebase()
#     model = initialize_gemini()
    
#     if not db or not model:
#         print("❌ Failed to initialize required services. Exiting...")
#         return
    
#     # Connect to camera stream
#     camera_url = os.getenv('CAMERA_STREAM_URL', 'http://192.168.31.220:8080/video')
#     print(f"📹 Connecting to camera: {camera_url}")
    
#     cap = cv2.VideoCapture(camera_url)
    
#     if not cap.isOpened():
#         print(f"❌ Error: Could not connect to camera at {camera_url}")
#         print("💡 Make sure IP Webcam app is running on your phone")
#         return
    
#     print("✅ Connected to camera stream successfully!")
#     print("🔍 Starting real-time anomaly detection...")
#     print("⏰ Processing 1 frame every 5 seconds...")
    
#     frame_count = 0
    
#     while True:
#         try:
#             # Capture frame
#             ret, frame = cap.read()
#             if not ret:
#                 print("⚠️ Failed to capture frame, retrying...")
#                 time.sleep(5)
#                 continue
            
#             frame_count += 1
#             print(f"\n📸 Processing frame #{frame_count}...")
            
#             # Convert frame to PIL Image for Gemini
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             pil_image = Image.fromarray(frame_rgb)
            
#             # Enhanced prompt for better anomaly detection
#             prompt = """
#             You are an advanced AI security analyst. Analyze this surveillance image for potential security threats and anomalies.

#             Look specifically for:
#             🔥 FIRE: Any flames, burning objects, or fire-related incidents
#             💨 SMOKE: Visible smoke, haze, or burning indicators  
#             👥 CROWD PANIC: Unusual crowd behavior, running, panic, overcrowding
#             👁️ SUSPICIOUS ACTIVITY: Unusual behavior, potential threats, unauthorized access
#             ⚡ VIOLENCE: Fighting, aggressive behavior, weapons, physical altercations
            
#             Respond ONLY in valid JSON format:
#             {
#                 "anomaly_detected": true/false,
#                 "anomaly_type": "fire|smoke|crowd_panic|suspicious_activity|violence|none",
#                 "confidence": 0.0-1.0,
#                 "description": "Detailed description of what you observe",
#                 "severity": "low|medium|high",
#                 "zone": "Brief description of the area/location in the image"
#             }
            
#             Be precise and only flag genuine security concerns. Normal activities should return anomaly_detected: false.
#             """
            
#             # Send to Gemini Vision API
#             response = model.generate_content([prompt, pil_image])
            
#             # Parse response
#             try:
#                 response_text = response.text.strip()
                
#                 # Clean JSON response
#                 if response_text.startswith('```json'):
#                     response_text = response_text[7:-3]
#                 elif response_text.startswith('```'):
#                     response_text = response_text[3:-3]
                
#                 analysis = json.loads(response_text)
                
#                 print(f"🤖 AI Analysis Complete:")
#                 print(f"   Anomaly Detected: {analysis.get('anomaly_detected', False)}")
#                 print(f"   Type: {analysis.get('anomaly_type', 'none')}")
#                 print(f"   Confidence: {analysis.get('confidence', 0):.1%}")
                
#                 # If anomaly detected, process and store
#                 if analysis.get('anomaly_detected', False):
#                     print(f"🚨 ANOMALY DETECTED: {analysis['anomaly_type']} (Severity: {analysis.get('severity', 'medium')})")
                    
#                     # Upload frame to Firebase Storage
#                     try:
#                         bucket = storage.bucket()
#                         timestamp = datetime.now().isoformat().replace(':', '-')
#                         filename = f"anomalies/{timestamp}_{analysis['anomaly_type']}.jpg"
                        
#                         # Convert frame to bytes
#                         _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
#                         blob = bucket.blob(filename)
                        
#                         # Upload with retry logic
#                         for attempt in range(3):
#                             try:
#                                 blob.upload_from_string(
#                                     buffer.tobytes(), 
#                                     content_type='image/jpeg',
#                                     timeout=30
#                                 )
#                                 blob.make_public()
#                                 snapshot_url = blob.public_url
#                                 print(f"📸 Snapshot uploaded: {snapshot_url}")
#                                 break
#                             except Exception as upload_error:
#                                 if attempt == 2:  # Final attempt failed
#                                     print(f"⚠️ All upload attempts failed: {upload_error}")
#                                     snapshot_url = None
#                                     # Save locally as backup
#                                     local_path = f"snapshots/{filename}"
#                                     os.makedirs("snapshots", exist_ok=True)
#                                     cv2.imwrite(local_path, frame)
#                                     print(f"📸 Saved locally: {local_path}")
#                                 else:
#                                     print(f"⚠️ Upload attempt {attempt+1} failed, retrying...")
#                                     time.sleep(2)
                        
#                     except Exception as e:
#                         print(f"⚠️ Failed to process snapshot: {e}")
#                         snapshot_url = None
                    
#                     # Prepare alert data for Firestore
#                     alert_data = {
#                         'timestamp': datetime.now(),
#                         'anomaly_type': analysis.get('anomaly_type', 'unknown'),
#                         'confidence': float(analysis.get('confidence', 0.0)),
#                         'description': analysis.get('description', 'Anomaly detected'),
#                         'severity': analysis.get('severity', 'medium'),
#                         'zone': analysis.get('zone', 'Zone A - Mobile Camera'),
#                         'camera': 'zone-a-mobile-cam',
#                         'location': {
#                             'lat': float(os.getenv('NEXT_PUBLIC_DEFAULT_LAT', 28.6139)),
#                             'lng': float(os.getenv('NEXT_PUBLIC_DEFAULT_LNG', 77.2090))
#                         },
#                         'snapshot_url': snapshot_url,
#                         'resolved': False
#                     }
                    
#                     # Store in Firestore
#                     try:
#                         doc_ref = db.collection('alerts').add(alert_data)
#                         print(f"💾 Alert stored in Firestore with ID: {doc_ref[1].id}")
                        
#                         # Send email notification
#                         send_email_alert(alert_data)
                        
#                     except Exception as e:
#                         print(f"❌ Failed to store alert in Firestore: {e}")
                
#                 else:
#                     print("✅ No anomalies detected - All clear")
                    
#             except json.JSONDecodeError as e:
#                 print(f"❌ Error parsing Gemini response: {e}")
#                 print(f"Raw response: {response.text}")
#             except Exception as e:
#                 print(f"❌ Error processing Gemini response: {e}")
            
#         except Exception as e:
#             print(f"❌ Error in main processing loop: {e}")
#             print("🔄 Continuing monitoring...")
        
#         # Wait 5 seconds before next capture
#         print("⏳ Waiting 5 seconds before next frame...")
#         time.sleep(5)

# if __name__ == "__main__":
#     print("🔍 Project Drishti - AI-Powered Video Anomaly Detection")
#     print("=" * 60)
    
#     # Check required environment variables
#     required_vars = [
#         'GEMINI_API_KEY',
#         'FIREBASE_PROJECT_ID', 
#         'FIREBASE_PRIVATE_KEY',
#         'FIREBASE_CLIENT_EMAIL',
#         'CAMERA_STREAM_URL'
#     ]
    
#     missing_vars = [var for var in required_vars if not os.getenv(var)]
    
#     if missing_vars:
#         print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
#         print("💡 Please check your .env file and ensure all variables are set")
#         exit(1)
    
#     try:
#         capture_and_analyze()
#     except KeyboardInterrupt:
#         print("\n🛑 Stopping video processor...")
#         print("👋 Goodbye!")
#     except Exception as e:
#         print(f"❌ Fatal error: {e}")


# !new cld 
import cv2
import base64
import json
import time
import requests
import os
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, storage
import google.generativeai as genai
import io
from PIL import Image
from dotenv import load_dotenv
import certifi
import ssl

# Load environment variables
load_dotenv()

# Configure SSL certificates globally - FIXED
cert_path = certifi.where()
os.environ["SSL_CERT_FILE"] = cert_path
os.environ["REQUESTS_CA_BUNDLE"] = cert_path
os.environ["CURL_CA_BUNDLE"] = cert_path

# Create SSL context
ssl_context = ssl.create_default_context(cafile=cert_path)
print(f"🔐 Using SSL certificates from: {cert_path}")

def initialize_firebase():
    """Initialize Firebase Admin SDK with SSL fix"""
    if not firebase_admin._apps:
        try:
            # Create credentials from environment variables
            cred_dict = {
                "type": "service_account",
                "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
                "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
            }
            
            cred = credentials.Certificate(cred_dict)
            
            # Initialize Firebase with SSL context - FIXED
            firebase_admin.initialize_app(cred, {
                'storageBucket': os.getenv('NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET')
            })
            
            print("✅ Firebase Admin SDK initialized successfully with SSL")
            return firestore.client()
        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
            return None
    
    return firestore.client()

def initialize_gemini():
    """Initialize Gemini AI with free tier model"""
    try:
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        # Using free tier model gemini-1.5-flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini AI initialized successfully (Free Tier)")
        return model
    except Exception as e:
        print(f"❌ Gemini initialization error: {e}")
        return None

def send_email_alert(alert_data):
    """Send email alert using Resend API"""
    try:
        resend_api_key = os.getenv('RESEND_API_KEY')
        if not resend_api_key:
            print("⚠️ No Resend API key found, skipping email")
            return
        
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {resend_api_key}",
            "Content-Type": "application/json"
        }
        
        # Create email with rich HTML content
        severity_colors = {
            'low': '#22c55e',
            'medium': '#f59e0b', 
            'high': '#ef4444'
        }
        
        severity_emojis = {
            'low': '🟢',
            'medium': '🟡',
            'high': '🔴'
        }
        
        anomaly_emojis = {
            'fire': '🔥',
            'smoke': '💨',
            'crowd_panic': '👥',
            'suspicious_activity': '👁️',
            'violence': '⚡'
        }
        
        data = {
            "from": os.getenv('ALERT_EMAIL_FROM', 'alerts@drishti.ai'),
            "to": [os.getenv('ALERT_EMAIL_TO', 'security@example.com')],
            "subject": f"🚨 DRISHTI ALERT: {alert_data['anomaly_type'].replace('_', ' ').title()} Detected",
            "html": f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; background: #f8fafc; padding: 20px;">
                <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); color: white; padding: 20px; border-radius: 10px 10px 0 0;">
                    <h1 style="margin: 0; font-size: 24px;">🔍 Project Drishti Security Alert</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">Real-time Anomaly Detection System</p>
                </div>
                
                <div style="background: white; padding: 30px; border-radius: 0 0 10px 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <div style="background: {severity_colors[alert_data['severity']]}; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
                        <h2 style="margin: 0; font-size: 20px;">
                            {anomaly_emojis.get(alert_data['anomaly_type'], '⚠️')} {alert_data['anomaly_type'].replace('_', ' ').upper()} DETECTED
                        </h2>
                        <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">
                            {severity_emojis[alert_data['severity']]} {alert_data['severity'].upper()} SEVERITY
                        </p>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <h3 style="color: #374151; margin-bottom: 10px;">📋 Alert Details</h3>
                        <table style="width: 100%; border-collapse: collapse;">
                            <tr style="border-bottom: 1px solid #e5e7eb;">
                                <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Description:</td>
                                <td style="padding: 8px 0; color: #374151;">{alert_data['description']}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #e5e7eb;">
                                <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Confidence:</td>
                                <td style="padding: 8px 0; color: #374151;">{alert_data['confidence']:.1%}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #e5e7eb;">
                                <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Location:</td>
                                <td style="padding: 8px 0; color: #374151;">📍 {alert_data['zone']}</td>
                            </tr>
                            <tr style="border-bottom: 1px solid #e5e7eb;">
                                <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Camera:</td>
                                <td style="padding: 8px 0; color: #374151;">📹 {alert_data['camera']}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold; color: #6b7280;">Time:</td>
                                <td style="padding: 8px 0; color: #374151;">⏰ {alert_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</td>
                            </tr>
                        </table>
                    </div>
                    
                    {f'''
                    <div style="text-align: center; margin: 20px 0;">
                        <a href="{alert_data['snapshot_url']}" 
                           style="display: inline-block; background: #3b82f6; color: white; padding: 12px 24px; 
                                  text-decoration: none; border-radius: 6px; font-weight: bold;">
                            📸 View Snapshot Image
                        </a>
                    </div>
                    ''' if alert_data.get('snapshot_url') else ''}
                    
                    <div style="background: #f3f4f6; padding: 15px; border-radius: 6px; margin-top: 20px;">
                        <p style="margin: 0; font-size: 14px; color: #6b7280;">
                            🤖 This alert was automatically generated by Project Drishti's AI-powered video analysis system.
                            Please investigate and take appropriate action if necessary.
                        </p>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 20px; color: #6b7280; font-size: 12px;">
                    <p>Project Drishti - Intelligent Security Monitoring</p>
                </div>
            </div>
            """
        }
        
        # Use requests with SSL verification - FIXED
        response = requests.post(url, headers=headers, json=data, verify=cert_path, timeout=30)
        if response.status_code == 200:
            print("📧 Email alert sent successfully")
        else:
            print(f"❌ Failed to send email: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error sending email: {e}")

def save_local_backup(frame, filename):
    """Save frame locally as backup - FIXED"""
    try:
        # Create full directory structure
        local_dir = os.path.join("snapshots", "anomalies")
        os.makedirs(local_dir, exist_ok=True)
        
        # Full local path
        local_path = os.path.join(local_dir, filename)
        
        # Save the image
        success = cv2.imwrite(local_path, frame)
        if success:
            print(f"📸 Saved locally: {local_path}")
            return local_path
        else:
            print(f"❌ Failed to save locally: {local_path}")
            return None
            
    except Exception as e:
        print(f"❌ Error saving local backup: {e}")
        return None

def capture_and_analyze():
    """Main function to capture video and analyze for anomalies"""
    print("🚀 Starting Project Drishti Video Processor...")
    
    # Initialize services
    db = initialize_firebase()
    model = initialize_gemini()
    
    if not model:
        print("❌ Failed to initialize Gemini AI. Exiting...")
        return
    
    if not db:
        print("⚠️ Firebase initialization failed. Will save alerts locally only.")
    
    # Connect to camera stream
    camera_url = os.getenv('CAMERA_STREAM_URL', 'http://192.168.31.220:8080/video')
    print(f"📹 Connecting to camera: {camera_url}")
    
    cap = cv2.VideoCapture(camera_url)
    
    if not cap.isOpened():
        print(f"❌ Error: Could not connect to camera at {camera_url}")
        print("💡 Make sure IP Webcam app is running on your phone")
        return
    
    print("✅ Connected to camera stream successfully!")
    print("🔍 Starting real-time anomaly detection...")
    print("⏰ Processing 1 frame every 5 seconds...")
    
    frame_count = 0
    
    while True:
        try:
            # Capture frame
            ret, frame = cap.read()
            if not ret:
                print("⚠️ Failed to capture frame, retrying...")
                time.sleep(5)
                continue
            
            frame_count += 1
            print(f"\n📸 Processing frame #{frame_count}...")
            
            # Convert frame to PIL Image for Gemini
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(frame_rgb)
            
            # Enhanced prompt for better anomaly detection
            prompt = """
            You are an advanced AI security analyst. Analyze this surveillance image for potential security threats and anomalies.

            Look specifically for:
            🔥 FIRE: Any flames, burning objects, or fire-related incidents
            💨 SMOKE: Visible smoke, haze, or burning indicators  
            👥 CROWD PANIC: Unusual crowd behavior, running, panic, overcrowding
            👁️ SUSPICIOUS ACTIVITY: Unusual behavior, potential threats, unauthorized access
            ⚡ VIOLENCE: Fighting, aggressive behavior, weapons, physical altercations
            
            Respond ONLY in valid JSON format:
            {
                "anomaly_detected": true/false,
                "anomaly_type": "fire|smoke|crowd_panic|suspicious_activity|violence|none",
                "confidence": 0.0-1.0,
                "description": "Detailed description of what you observe",
                "severity": "low|medium|high",
                "zone": "Brief description of the area/location in the image"
            }
            
            Be precise and only flag genuine security concerns. Normal activities should return anomaly_detected: false.
            """
            
            # Send to Gemini Vision API
            response = model.generate_content([prompt, pil_image])
            
            # Parse response
            try:
                response_text = response.text.strip()
                
                # Clean JSON response
                if response_text.startswith('```json'):
                    response_text = response_text[7:-3]
                elif response_text.startswith('```'):
                    response_text = response_text[3:-3]
                
                analysis = json.loads(response_text)
                
                print(f"🤖 AI Analysis Complete:")
                print(f"   Anomaly Detected: {analysis.get('anomaly_detected', False)}")
                print(f"   Type: {analysis.get('anomaly_type', 'none')}")
                print(f"   Confidence: {analysis.get('confidence', 0):.1%}")
                
                # If anomaly detected, process and store
                if analysis.get('anomaly_detected', False):
                    print(f"🚨 ANOMALY DETECTED: {analysis['anomaly_type']} (Severity: {analysis.get('severity', 'medium')})")
                    
                    # Generate filename
                    timestamp = datetime.now().isoformat().replace(':', '-')
                    filename = f"{timestamp}_{analysis['anomaly_type']}.jpg"
                    
                    # Save locally first as backup - FIXED
                    local_path = save_local_backup(frame, filename)
                    
                    # Try to upload to Firebase Storage
                    snapshot_url = None
                    if db:
                        try:
                            bucket = storage.bucket()
                            blob_path = f"anomalies/{filename}"
                            
                            # Convert frame to bytes
                            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
                            blob = bucket.blob(blob_path)
                            
                            # Upload with retry logic
                            for attempt in range(3):
                                try:
                                    blob.upload_from_string(
                                        buffer.tobytes(), 
                                        content_type='image/jpeg',
                                        timeout=30
                                    )
                                    blob.make_public()
                                    snapshot_url = blob.public_url
                                    print(f"☁️ Snapshot uploaded to Firebase: {snapshot_url}")
                                    break
                                except Exception as upload_error:
                                    if attempt == 2:  # Final attempt failed
                                        print(f"⚠️ All Firebase upload attempts failed: {upload_error}")
                                        snapshot_url = None
                                    else:
                                        print(f"⚠️ Upload attempt {attempt+1} failed, retrying...")
                                        time.sleep(2)
                            
                        except Exception as e:
                            print(f"⚠️ Failed to upload to Firebase: {e}")
                            snapshot_url = None
                    
                    # Prepare alert data
                    alert_data = {
                        'timestamp': datetime.now(),
                        'anomaly_type': analysis.get('anomaly_type', 'unknown'),
                        'confidence': float(analysis.get('confidence', 0.0)),
                        'description': analysis.get('description', 'Anomaly detected'),
                        'severity': analysis.get('severity', 'medium'),
                        'zone': analysis.get('zone', 'Zone A - Mobile Camera'),
                        'camera': 'zone-a-mobile-cam',
                        'location': {
                            'lat': float(os.getenv('NEXT_PUBLIC_DEFAULT_LAT', 28.6139)),
                            'lng': float(os.getenv('NEXT_PUBLIC_DEFAULT_LNG', 77.2090))
                        },
                        'snapshot_url': snapshot_url or local_path,
                        'local_path': local_path,
                        'resolved': False
                    }
                    
                    # Store in Firestore if available
                    if db:
                        try:
                            doc_ref = db.collection('alerts').add(alert_data)
                            print(f"💾 Alert stored in Firestore with ID: {doc_ref[1].id}")
                        except Exception as e:
                            print(f"❌ Failed to store alert in Firestore: {e}")
                            # Save alert data locally as JSON backup
                            alerts_dir = os.path.join("snapshots", "alerts")
                            os.makedirs(alerts_dir, exist_ok=True)
                            
                            # Convert datetime to string for JSON serialization
                            alert_data_json = alert_data.copy()
                            alert_data_json['timestamp'] = alert_data['timestamp'].isoformat()
                            
                            alert_file = os.path.join(alerts_dir, f"{filename.replace('.jpg', '')}_alert.json")
                            with open(alert_file, 'w') as f:
                                json.dump(alert_data_json, f, indent=2)
                            print(f"💾 Alert saved locally as JSON: {alert_file}")
                    
                    # Send email notification
                    try:
                        send_email_alert(alert_data)
                    except Exception as e:
                        print(f"❌ Failed to send email alert: {e}")
                
                else:
                    print("✅ No anomalies detected - All clear")
                    
            except json.JSONDecodeError as e:
                print(f"❌ Error parsing Gemini response: {e}")
                print(f"Raw response: {response.text}")
            except Exception as e:
                print(f"❌ Error processing Gemini response: {e}")
            
        except Exception as e:
            print(f"❌ Error in main processing loop: {e}")
            print("🔄 Continuing monitoring...")
        
        # Wait 5 seconds before next capture
        print("⏳ Waiting 5 seconds before next frame...")
        time.sleep(5)

if __name__ == "__main__":
    print("🔍 Project Drishti - AI-Powered Video Anomaly Detection")
    print("=" * 60)
    
    # Check required environment variables
    required_vars = [
        'GEMINI_API_KEY',
        'CAMERA_STREAM_URL'
    ]
    
    # Optional Firebase vars
    firebase_vars = [
        'FIREBASE_PROJECT_ID', 
        'FIREBASE_PRIVATE_KEY',
        'FIREBASE_CLIENT_EMAIL',
        'NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET'
    ]
    
    missing_required = [var for var in required_vars if not os.getenv(var)]
    missing_firebase = [var for var in firebase_vars if not os.getenv(var)]
    
    if missing_required:
        print(f"❌ Missing required environment variables: {', '.join(missing_required)}")
        print("💡 Please check your .env file and ensure all variables are set")
        exit(1)
    
    if missing_firebase:
        print(f"⚠️ Missing Firebase environment variables: {', '.join(missing_firebase)}")
        print("💡 Firebase features will be disabled. Alerts will be saved locally only.")
    
    try:
        capture_and_analyze()
    except KeyboardInterrupt:
        print("\n🛑 Stopping video processor...")
        print("👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()