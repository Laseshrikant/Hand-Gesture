# AI Hand Gesture Control Web App 🚀

## Features
- Real-time hand detection & tracking with landmarks overlay
- Recognizes: **Thumbs Up**, **Open Palm**, **Victory**, **Fist**, finger counts
- Webcam access via browser
- Start/Stop camera buttons
- Error handling for camera permissions
- Responsive modern UI

## Folder Structure
```
hand_gesture_app/
├── app.py              # Flask backend (OpenCV + MediaPipe)
├── requirements.txt    # Dependencies
├── templates/
│   └── index.html      # Main page
└── static/
    ├── css/style.css   # Styling
    └── js/script.js    # Webcam + detection logic
```

## Step-by-Step Setup & Run (VS Code)

1. **Open project**:
   ```
   cd "c:/Users/Shreee/OneDrive/Desktop/test/info/infom/Assistant/hand_gesture_app"
   ```

2. **Install dependencies** (Python 3.8+ required):
   ```
   pip install -r requirements.txt
   ```

3. **Run the server**:
   ```
   python app.py
   ```
   - Server starts at `http://0.0.0.0:5000`

4. **Open in browser**:
   - Go to `http://127.0.0.1:5000`
   - Click **Start Camera** → Allow mic/camera permission
   - Show hand gestures → See real-time detection + landmarks!

5. **Test gestures**:
   | Gesture | Show |
   |---------|------|
   | Thumbs Up | 👍 |
   | Open Palm | ✋ |
   | Victory | ✌️ |
   | Fist | ✊ |

## Troubleshooting
- **Camera error**: Check browser permissions (HTTPS or localhost ok)
- **ImportError**: Run `pip install -r requirements.txt` again
- **Port busy**: Kill process or change port in app.py
- **Chrome best**: Supports getUserMedia perfectly

**Fully self-contained - no API keys needed!** 🎥✋

