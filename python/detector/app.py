from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import threading
import subprocess
import signal
import sys

app = Flask(__name__)
CORS(app)

# Global variables
detection_process = None
detection_running = False

# Create directories
os.makedirs('targets', exist_ok=True)
os.makedirs('snapshots', exist_ok=True)

@app.route('/target_status', methods=['GET'])
def target_status():
    target_path = os.path.join('targets', 'current_target.jpg')
    return jsonify({
        'has_target': os.path.exists(target_path),
        'target_path': target_path if os.path.exists(target_path) else None,
        'detection_running': detection_running
    })

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global detection_process, detection_running
    
    target_path = os.path.join('targets', 'current_target.jpg')
    
    if not os.path.exists(target_path):
        return jsonify({'error': 'No target image found'}), 400
    
    if detection_running:
        return jsonify({'message': 'Detection already running'})
    
    try:
        # Start your main.py as a subprocess
        detection_process = subprocess.Popen([sys.executable, 'main.py'])
        detection_running = True
        return jsonify({'message': 'Detection started'})
    except Exception as e:
        return jsonify({'error': f'Failed to start detection: {str(e)}'}), 500

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global detection_process, detection_running
    
    if detection_process:
        try:
            detection_process.terminate()
            detection_process.wait(timeout=5)
        except:
            detection_process.kill()
        detection_process = None
    
    detection_running = False
    return jsonify({'message': 'Detection stopped'})

@app.route('/snapshots/<filename>')
def get_snapshot(filename):
    return send_from_directory('snapshots', filename)

def cleanup():
    """Clean up on exit"""
    global detection_process
    if detection_process:
        detection_process.terminate()

# Register cleanup function
import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    print("🚀 Starting Flask backend...")
    print("📁 Directories: targets, snapshots")
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        cleanup()