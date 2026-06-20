from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import librosa
from scipy.signal import butter, lfilter
import joblib
import io
import os

app = FastAPI()

# Enable CORS for your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load the trained model and scaler ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), "svm_lung_model.joblib")
try:
    pipeline = joblib.load(MODEL_PATH)
    scaler = pipeline['scaler']
    model = pipeline['model']
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    scaler = None
    model = None

# --- Digital Signal Processing Functions ---
def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def extract_features_from_bytes(audio_bytes, target_sr=4410):
    # Load audio directly from memory
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=target_sr)
    if len(y) == 0:
        raise ValueError("Audio file is empty")
        
    # Standardize and Filter
    y = y / (np.max(np.abs(y)) + 1e-6)
    y_filtered = bandpass_filter(y, 100, 2000, target_sr)
    
    # Extract MFCCs
    mfccs = librosa.feature.mfcc(y=y_filtered, sr=target_sr, n_mfcc=13)
    return np.mean(mfccs.T, axis=0)

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model is not loaded on the server.")
        
    try:
        # 1. Read the uploaded file
        audio_data = await file.read()
        
        # 2. Extract features using our DSP pipeline
        features = extract_features_from_bytes(audio_data)
        
        # 3. Reshape and scale features for the SVM
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # 4. Predict the clinical profile
        prediction = model.predict(features_scaled)[0]
        
        return {"filename": file.filename, "prediction": str(prediction)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
