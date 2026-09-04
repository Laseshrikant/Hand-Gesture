const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const gestureSpan = document.getElementById('gesture');
const errorDiv = document.getElementById('error');

let stream = null;
let animationId = null;

startBtn.addEventListener('click', startCamera);
stopBtn.addEventListener('click', stopCamera);

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 } 
        });
        video.srcObject = stream;
        video.play();
        
        startBtn.disabled = true;
        stopBtn.disabled = false;
        canvas.classList.add('detecting');
        errorDiv.classList.add('hidden');
        
        video.addEventListener('loadedmetadata', processFrame);
    } catch (err) {
        showError('Camera access denied or not available: ' + err.message);
    }
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (animationId) {
        cancelAnimationFrame(animationId);
    }
    
    startBtn.disabled = false;
    stopBtn.disabled = true;
    canvas.classList.remove('detecting');
    gestureSpan.textContent = 'No gesture detected';
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

async function processFrame() {
    if (video.videoWidth === 0) {
        animationId = requestAnimationFrame(processFrame);
        return;
    }
    
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // Capture canvas as base64
    const frameData = canvas.toDataURL('image/jpeg', 0.8);
    
    try {
        const response = await fetch('/detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ image: frameData })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.error) {
                showError(data.error);
            } else {
                // Draw processed image with landmarks
                const img = new Image();
                img.onload = () => ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
                img.src = data.image;
                
                gestureSpan.textContent = data.gesture;
            }
        }
    } catch (err) {
        console.error('Detection error:', err);
    }
    
    animationId = requestAnimationFrame(processFrame);
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

