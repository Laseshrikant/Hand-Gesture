from flask import Flask, render_template, request, jsonify, Response
import cv2
import mediapipe as mp
import numpy as np
import base64
from PIL import Image
import io
import eventlet
import eventlet.wsgi

app = Flask(__name__)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

def process_frame(image):
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)
    
    gesture = "No hand"
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Simple gesture recognition using landmarks
            landmarks = hand_landmarks.landmark
            thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP.value]
            index_tip = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP.value]
            middle_tip = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP.value]
            ring_tip = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP.value]
            pinky_tip = landmarks[mp_hands.HandLandmark.PINKY_TIP.value]
            
            # Count raised fingers
            raised_fingers = 0
            if thumb_tip.y < landmarks[mp_hands.HandLandmark.THUMB_IP.value].y:
                raised_fingers += 1  # Thumbs up (simplified)
            if index_tip.y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP.value].y:
                raised_fingers += 1
            if middle_tip.y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP.value].y:
                raised_fingers += 1
            if ring_tip.y < landmarks[mp_hands.HandLandmark.RING_FINGER_PIP.value].y:
                raised_fingers += 1
            if pinky_tip.y < landmarks[mp_hands.HandLandmark.PINKY_PIP.value].y:
                raised_fingers += 1
            
            if raised_fingers == 5:
                gesture = "Open Palm"
            elif raised_fingers == 2 and landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP.value].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP.value].y and landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP.value].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP.value].y:
                gesture = "Victory"
            elif raised_fingers == 1 and thumb_tip.y < landmarks[mp_hands.HandLandmark.THUMB_IP.value].y:
                gesture = "Thumbs Up"
            elif raised_fingers == 0:
                gesture = "Fist"
            else:
                gesture = f"{raised_fingers} Fingers"
    
    return image, gesture

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    try:
        data = request.json['image']
        # Decode base64 image
        img_data = base64.b64decode(data.split(',')[1])
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        processed_img, gesture = process_frame(img)
        
        # Encode processed image back to base64
        _, buffer = cv2.imencode('.jpg', processed_img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        
        return jsonify({
            'image': f'data:image/jpeg;base64,{img_base64}',
            'gesture': gesture
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=True)

