import firebase_admin
from firebase_admin import credentials, firestore, storage
import os
from datetime import datetime
import json
from dotenv import load_dotenv

load_dotenv()

class FirebaseClient:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._initialize_firebase()
            FirebaseClient._initialized = True
    
    def _initialize_firebase(self):
        try:
            # Check if Firebase is already initialized
            firebase_admin.get_app()
            print("✅ Firebase already initialized")
        except ValueError:
            # Initialize Firebase
            private_key = os.getenv('FIREBASE_PRIVATE_KEY', '').replace('\\n', '\n')
            
            cred_dict = {
                "type": "service_account",
                "project_id": os.getenv('FIREBASE_PROJECT_ID'),
                "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
                "private_key": private_key,
                "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
                "client_id": os.getenv('FIREBASE_CLIENT_ID'),
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{os.getenv('FIREBASE_CLIENT_EMAIL')}"
            }
            
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred, {
                'storageBucket': f"{os.getenv('FIREBASE_PROJECT_ID')}.appspot.com"
            })
            print("✅ Firebase initialized successfully")
        
        self.db = firestore.client()
        self.bucket = storage.bucket()
    
    def upload_image(self, local_path, remote_path):
        """Upload image to Firebase Storage and return public URL"""
        try:
            blob = self.bucket.blob(remote_path)
            blob.upload_from_filename(local_path)
            blob.make_public()
            return blob.public_url
        except Exception as e:
            print(f"❌ Upload error: {e}")
            return None
    
    def save_detection(self, detection_data):
        """Save detection to Firestore"""
        try:
            doc_ref = self.db.collection('detections').document()
            detection_data['id'] = doc_ref.id
            detection_data['created_at'] = datetime.utcnow()
            doc_ref.set(detection_data)
            print(f"✅ Detection saved: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            print(f"❌ Firestore save error: {e}")
            return None
    
    def save_missing_person(self, person_data):
        """Save missing person report to Firestore"""
        try:
            doc_ref = self.db.collection('missing_persons').document()
            person_data['id'] = doc_ref.id
            person_data['created_at'] = datetime.utcnow()
            person_data['status'] = 'active'
            doc_ref.set(person_data)
            print(f"✅ Missing person saved: {doc_ref.id}")
            return doc_ref.id
        except Exception as e:
            print(f"❌ Missing person save error: {e}")
            return None

# Global instance
firebase_client = FirebaseClient()
