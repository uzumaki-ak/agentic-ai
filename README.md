# 🔍 Project Drishti - AI Video Anomaly Detection System

A comprehensive real-time video processing and anomaly detection system using AI-powered computer vision for security monitoring.

## ✅ **CHECKPOINT VERIFICATION**

### 🔄 **Real-time Sync**
- ✅ **Firestore Real-time Listener**: Uses `onSnapshot()` for live updates (no polling)
- ✅ **Live Dashboard Updates**: Automatic UI refresh when new alerts are detected
- ✅ **Real-time Map Markers**: Instant marker updates on anomaly detection

### 🧠 **Gemini Integration** 
- ✅ **Gemini Vision API**: Uses `gemini-1.5-flash` (free tier) for image analysis
- ✅ **JPEG Buffer Processing**: Converts OpenCV frames to PIL Images for Gemini
- ✅ **Structured JSON Responses**: Proper prompt engineering for consistent outputs
- ✅ **Confidence Scoring**: AI provides 0.0-1.0 confidence ratings

### 📷 **Stream Connectivity**
- ✅ **IP Webcam Integration**: Connects to `http://<yourip>/video`
- ✅ **OpenCV Video Capture**: Robust frame capture with error handling
- ✅ **5-Second Intervals**: Processes 1 frame every 5 seconds as specified
- ✅ **Connection Monitoring**: Auto-retry on connection failures

### ☁️ **Firebase Setup**
- ✅ **Firebase Admin SDK**: Server-side operations for Python backend
- ✅ **Firebase Web SDK**: Client-side real-time listeners in Next.js
- ✅ **Firestore Database**: Structured alert storage with timestamps
- ✅ **Firebase Storage**: Image upload with public URLs

### 🗺️ **Map Visualization**
- ✅ **Leaflet.js Integration**: Interactive map with custom markers
- ✅ **Color-coded Severity**: Green (low), Yellow (medium), Red (high)
- ✅ **Emoji Markers**: Fire 🔥, Smoke 💨, Crowd 👥, Suspicious 👁️
- ✅ **Rich Popups**: Detailed alert information with snapshots

### 💬 **AI Chatbot**
- ✅ **Natural Language Queries**: "Any anomalies in Zone A?"
- ✅ **Time-based Analysis**: "Summarize last hour alerts"
- ✅ **Zone-specific Reports**: Location-based anomaly analysis
- ✅ **Intelligent Responses**: Context-aware AI assistant

### 📧 **Email Notifications**
- ✅ **Resend API Integration**: Professional HTML email alerts
- ✅ **Rich Email Templates**: Severity colors, emojis, and styling
- ✅ **Snapshot Links**: Direct links to captured images
- ✅ **Contextual Information**: Full alert details in email

---

## 🚀 **Features**

- **Real-time Video Processing**: Connects to IP webcam streams and processes frames every 5 seconds
- **AI-Powered Anomaly Detection**: Uses Gemini Vision API to detect fire, smoke, crowd panic, and suspicious activities
- **Interactive Map Dashboard**: Real-time visualization of alerts with location markers
- **Intelligent Chatbot**: Query system status and anomalies using natural language
- **Email Notifications**: Automatic alerts sent to security teams
- **Modern Dark UI**: Responsive design with dark blue theme
- **Real-time Updates**: Live data synchronization using Firebase

## 🛠️ **Tech Stack**

### Backend
- **Python + OpenCV**: Video capture and processing
- **Gemini Vision API**: AI-powered anomaly detection (Free Tier)
- **Firebase Admin SDK**: Data storage and file uploads
- **Resend API**: Email notifications

### Frontend
- **Next.js 15**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Modern UI components
- **Leaflet.js**: Interactive maps
- **Firebase Web SDK**: Real-time data synchronization

## 📋 **Prerequisites**

1. **IP Webcam App**: Install on Android device
2. **Firebase Project**: Set up Firestore and Storage
3. **Gemini API Key**: Get from Google AI Studio (Free)
4. **Resend Account**: For email notifications (optional)

## 🔧 **Installation**

### 1. Clone and Install Dependencies

\`\`\`bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
\`\`\`

### 2. Environment Setup

Copy `.env.local` and fill in your credentials:

\`\`\`bash
# Firebase Web Config (from Firebase Console)
NEXT_PUBLIC_FIREBASE_API_KEY=your_api_key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your_project_id
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=your_project.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
NEXT_PUBLIC_FIREBASE_APP_ID=your_app_id

# Firebase Admin (Service Account)
FIREBASE_PRIVATE_KEY_ID=your_private_key_id
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_CLIENT_EMAIL=your_service_account@your_project.iam.gserviceaccount.com
FIREBASE_CLIENT_ID=your_client_id
FIREBASE_PROJECT_ID=your_project_id

# Gemini API (Free Tier)
GEMINI_API_KEY=your_gemini_api_key

# IP Webcam
CAMERA_STREAM_URL=http://<>/video

# Email (Optional)
RESEND_API_KEY=your_resend_api_key
ALERT_EMAIL_TO=security@example.com
ALERT_EMAIL_FROM=alerts@drishti.ai

# Default Map Location
NEXT_PUBLIC_DEFAULT_LAT=28.6139
NEXT_PUBLIC_DEFAULT_LNG=77.2090
\`\`\`

### 3. Firebase Setup

1. Create a new Firebase project
2. Enable Firestore Database
3. Enable Firebase Storage
4. Create a service account and download the JSON key
5. Extract the required fields for environment variables

### 4. IP Webcam Setup

1. Install "IP Webcam" app on Android
2. Start the server in the app
3. Note the IP address (e.g., http://)
4. Update `CAMERA_STREAM_URL` in your environment

## 🚀 **Running the Application**

### Start the Frontend Dashboard

\`\`\`bash
npm run dev
\`\`\`

Visit `http://localhost:3000` to see the dashboard.

### Start the Video Processing Backend

\`\`\`bash
# Make sure your IP webcam is running
python scripts/video_processor.py
\`\`\`

## 📱 **Usage**

### Dashboard Features

1. **Live Map**: View real-time anomaly locations with color-coded severity markers
2. **Alerts List**: Browse recent alerts with filtering options
3. **Stats Cards**: Monitor system status and alert counts
4. **Filter Controls**: Filter alerts by severity, type, status, and time range

### AI Chatbot Queries

Ask the chatbot questions like:
- "Are there any anomalies in Zone A?"
- "What happened in the last hour?"
- "Show me high-severity alerts"
- "Any fire incidents today?"
- "System status overview"

### Alert Management

- Click "View Image" to see the captured frame
- Click "Resolve" to mark alerts as resolved
- Use filters to focus on specific alert types

## 🔍 **Anomaly Types Detected**

- **🔥 Fire**: Flames and fire incidents
- **💨 Smoke**: Smoke detection
- **👥 Crowd Panic**: Unusual crowd behavior
- **👁️ Suspicious Activity**: Potentially dangerous activities
- **⚡ Violence**: Physical altercations

## 📊 **System Architecture**

\`\`\`
IP Webcam → Python Backend → Gemini Vision API → Firebase Storage/Firestore
                                                        ↓
Next.js Dashboard ← Real-time Updates ← Firebase Web SDK
\`\`\`

## 🛡️ **Security Features**

- Real-time monitoring with 5-second intervals
- Confidence scoring for each detection
- Severity classification (Low/Medium/High)
- Automatic email notifications
- Historical data tracking
- Resolution workflow

## 🎨 **UI Features**

- **Dark Blue Theme**: Modern, professional appearance
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live data without page refresh
- **Interactive Maps**: Click markers for detailed information
- **Filtering System**: Advanced search and filter capabilities

## 📈 **Performance**

- **Processing Speed**: 1 frame every 5 seconds
- **Response Time**: Near real-time alert generation
- **Scalability**: Supports multiple camera feeds
- **Storage**: Efficient image compression and storage

## 🔧 **Customization**

### Adding New Anomaly Types

1. Update the Gemini prompt in `video_processor.py`
2. Add new types to the filter controls
3. Update the chatbot analysis logic

### Changing Detection Frequency

Modify the `time.sleep(5)` value in `video_processor.py`

### Custom Map Styling

Update the Leaflet configuration in `map-view.tsx`

## 🐛 **Troubleshooting**

### Common Issues

1. **Camera Connection Failed**: Check IP webcam app is running and IP is correct
2. **Firebase Errors**: Verify all environment variables are set correctly
3. **Gemini API Errors**: Check API key and quota limits
4. **Map Not Loading**: Ensure Leaflet CSS is loaded correctly

### Debug Mode

Add console logs in the Python script to monitor processing:

\`\`\`python
print(f"Frame captured: {ret}")
print(f"Gemini response: {response.text}")
\`\`\`

## 📄 **License**

This project is licensed under the MIT License.

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 **Support**

For issues and questions:
1. Check the troubleshooting section
2. Review Firebase and Gemini API documentation
3. Open an issue on GitHub

---

**Project Drishti** - Empowering security through intelligent video analysis 🔍👁️

*Built with ❤️ using Next.js 15, TypeScript, Tailwind CSS, Firebase, and Gemini AI*
