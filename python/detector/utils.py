import os
import json
import requests
from datetime import datetime
import cv2

def send_alert(alert_data):
    """Send detection alert to Next.js API"""
    try:
        nextjs_url = os.getenv('NEXTJS_API_URL', 'http://localhost:3000')
        response = requests.post(
            f"{nextjs_url}/api/alerts",
            json=alert_data,
            headers={'Content-Type': 'application/json'}
        )
        if response.status_code == 201:
            print(f"✅ Alert sent successfully: {alert_data['name']}")
        else:
            print(f"⚠️ Failed to send alert: {response.status_code}")
    except Exception as e:
        print(f"🚨 Alert send error: {str(e)}")

def get_camera_config():
    """Get camera configuration from environment"""
    return {
        'lat': float(os.getenv('CAMERA_LAT', '28.6129')),
        'lng': float(os.getenv('CAMERA_LNG', '77.2295')),
        'name': os.getenv('CAMERA_NAME', 'Main Entrance'),
        'url': os.getenv('CAMERA_URL', 'http://192.168.1.50:8080/video')
    }

def save_snapshot(frame, prefix="detection"):
    """Save detection snapshot to file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"snapshots/{prefix}_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    return filename