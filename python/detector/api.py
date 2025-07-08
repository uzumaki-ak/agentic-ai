from flask import Flask, jsonify
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'targets'

@app.route('/target_status', methods=['GET'])
def target_status():
    target_path = os.path.join(app.config['UPLOAD_FOLDER'], 'current_target.jpg')
    return jsonify({
        'has_target': os.path.exists(target_path),
        'target_path': target_path if os.path.exists(target_path) else None
    })

if __name__ == '__main__':
    os.makedirs('targets', exist_ok=True)
    os.makedirs('snapshots', exist_ok=True)
    app.run(port=5000)