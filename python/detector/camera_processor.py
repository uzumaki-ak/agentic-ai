# import cv2
# import time
# import threading
# from queue import Queue

# class CameraProcessor:
#     def __init__(self, camera_url, frame_queue_size=5):
#         self.camera_url = camera_url
#         self.cap = None
#         self.frame_queue = Queue(maxsize=frame_queue_size)
#         self.running = False
#         self.process_thread = None
        
#     def connect(self):
#         try:
#             self.cap = cv2.VideoCapture(self.camera_url)
#             if self.cap.isOpened():
#                 print(f"📹 Connected to camera: {self.camera_url}")
#                 return True
#             return False
#         except Exception as e:
#             print(f"⚠️ Camera connection error: {str(e)}")
#             return False
            
#     def start_capture(self):
#         self.running = True
#         print("🎥 Starting video capture...")
        
#         while self.running:
#             if not self.cap or not self.cap.isOpened():
#                 if not self.connect():
#                     time.sleep(1)
#                     continue
                    
#             ret, frame = self.cap.read()
#             if not ret:
#                 print("❌ Frame read error, reconnecting...")
#                 self.cap.release()
#                 self.connect()
#                 continue
                
#             if not self.frame_queue.full():
#                 self.frame_queue.put(frame)
                
#         if self.cap:
#             self.cap.release()
            
#     def start_processing(self, detector, interval=0.1):
#         self.process_thread = threading.Thread(
#             target=self._process_frames,
#             args=(detector, interval),
#             daemon=True
#         )
#         self.process_thread.start()
        
#     def _process_frames(self, detector, interval):
#         while self.running:
#             if not self.frame_queue.empty():
#                 frame = self.frame_queue.get()
#                 detector.process_frame(frame)
#             time.sleep(interval)
                
#     def stop(self):
#         self.running = False
#         if self.process_thread:
#             self.process_thread.join(timeout=1.0)
#         if self.cap:
#             self.cap.release()
#         print("🛑 Camera processing stopped")
        
#     def get_frame(self):
#         if not self.frame_queue.empty():
#             return self.frame_queue.get()
#         return None

#     def stream(self):
#         self.start_capture()
#         try:
#             while self.running:
#                 frame = self.get_frame()
#                 if frame is not None:
#                     yield frame
#                 time.sleep(0.033)  # ~30fps
#         finally:
#             self.stop()


# new


import cv2
import time
import threading
from queue import Queue
import logging

logger = logging.getLogger("CameraProcessor")

class CameraProcessor:
    def __init__(self, camera_url, frame_queue_size=5):
        self.camera_url = camera_url
        self.cap = None
        self.frame_queue = Queue(maxsize=frame_queue_size)
        self.running = False
        self.capture_thread = None
        self.frame_count = 0
        
    def connect(self):
        try:
            # Try different backends
            for backend in [cv2.CAP_FFMPEG, cv2.CAP_ANY]:
                self.cap = cv2.VideoCapture(self.camera_url, backend)
                if self.cap.isOpened():
                    logger.info(f"📹 Connected with backend {backend}")
                    # Set lower resolution for better performance
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    return True
            return False
        except Exception as e:
            logger.error(f"Connection error: {str(e)}")
            return False
            
    def start_capture(self):
        self.running = True
        logger.info("🎥 Starting video capture...")
        self.capture_thread = threading.Thread(target=self._capture_frames, daemon=True)
        self.capture_thread.start()
        
    def _capture_frames(self):
        while self.running:
            if not self.cap or not self.cap.isOpened():
                if not self.connect():
                    time.sleep(1)
                    continue
                    
            try:
                ret, frame = self.cap.read()
                if not ret:
                    logger.warning("Frame read error. Reconnecting...")
                    self.cap.release()
                    self.cap = None
                    continue
                    
                self.frame_count += 1
                
                # Only process every 3rd frame to reduce load
                if self.frame_count % 3 == 0:
                    if not self.frame_queue.full():
                        self.frame_queue.put(frame)
                    else:
                        # Drop old frames if queue is full
                        try:
                            self.frame_queue.get_nowait()
                        except:
                            pass
                        self.frame_queue.put(frame)
            except Exception as e:
                logger.error(f"Capture error: {str(e)}")
                self.cap = None
                
    def stop(self):
        self.running = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2.0)
        if self.cap:
            self.cap.release()
        logger.info("🛑 Camera processing stopped")
        
    def get_frame(self):
        if not self.frame_queue.empty():
            return self.frame_queue.get()
        return None

    def stream(self):
        self.start_capture()
        try:
            while self.running:
                frame = self.get_frame()
                if frame is not None:
                    yield frame
                else:
                    time.sleep(0.01)  # Prevent busy waiting
        finally:
            self.stop()


# !new prev good

# import requests
# import cv2
# import numpy as np
# from PIL import Image
# import io
# import time
# import logging

# logger = logging.getLogger("CameraProcessor")

# class RequestCameraProcessor:
#     def __init__(self, camera_url):
#         self.camera_url = camera_url
#         self.session = requests.Session()
#         self.running = False
#         self.frame_timeout = 5
#         self.max_retries = 3
        
#     def _get_frame(self):
#         """Get a single frame with retry logic"""
#         for _ in range(self.max_retries):
#             try:
#                 response = self.session.get(self.camera_url, timeout=self.frame_timeout)
#                 if response.status_code == 200:
#                     image = Image.open(io.BytesIO(response.content))
#                     return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#             except Exception as e:
#                 logger.warning(f"Frame fetch error: {str(e)}")
#                 time.sleep(0.5)
#         return None
        
#     def stream(self):
#         self.running = True
#         logger.info("Starting camera stream")
        
#         try:
#             while self.running:
#                 frame = self._get_frame()
#                 if frame is not None:
#                     yield frame
#                 else:
#                     logger.warning("Failed to get frame, retrying...")
#                     time.sleep(1)
#         finally:
#             self.running = False
#             logger.info("Camera stream stopped")
            
#     def stop(self):
#         self.running = False 