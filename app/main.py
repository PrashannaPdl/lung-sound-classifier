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

def is_valid_lung_sound(y, sr):
    """
    Runs signal processing heuristics to detect non-lung sounds 
    (like silence, speech, or music) before ML inference.
    """
    # 1. Silence check: Average RMS energy
    rms = np.mean(librosa.feature.rms(y=y))
    if rms < 0.0005:  
        return False, "Audio is too quiet or silent. Please upload a clearer recording."
        
    # 2. Speech/Music check: Spectral Centroid
    # Lung sounds are low-frequency. High centroid usually indicates speech or music.
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    if centroid > 2500:
        return False, "High-frequency noise detected (likely speech or music). Please upload a pure respiratory sound."
        
    # 3. Environmental noise check: Zero-Crossing Rate
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=y))
    if zcr > 0.2:
        return False, "Audio pattern resembles background static or speech, not breathing."
        
    return True, "Valid"

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

def extract_features(y, target_sr=4410):
    """
    Standardizes the audio and extracts the 13 MFCCs 
    matching exactly how the model was trained in Colab.
    """
    # Standardize amplitude (Normalization)
    y = y / (np.max(np.abs(y)) + 1e-6)
    
    # Apply Bandpass Filter (100 - 2000 Hz)
    y_filtered = bandpass_filter(y, 100, 2000, target_sr)
    
    # Extract MFCCs (13 coefficients)
    mfccs = librosa.feature.mfcc(y=y_filtered, sr=target_sr, n_mfcc=13)
    
    # Return mean of MFCC values across the time axes
    return np.mean(mfccs.T, axis=0)


# --- API Endpoints ---

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model is not loaded on the server. Check server logs.")
        
    if not file.filename.endswith('.wav'):
        raise HTTPException(status_code=400, detail="Only .wav files are supported")
        
    try:
        # 1. Read the uploaded file
        audio_data = await file.read()
        
        # Load audio directly from memory to the target sample rate used in training
        target_sr = 4410
        y, sr = librosa.load(io.BytesIO(audio_data), sr=target_sr)
        
        if len(y) == 0:
            raise HTTPException(status_code=422, detail="Audio file is empty")

        # 2. Heuristic Validation (Invalid Audio Check)
        is_valid, error_msg = is_valid_lung_sound(y, sr)
        if not is_valid:
            # This specific 422 status code is intercepted by the frontend to show the Red Profile
            raise HTTPException(status_code=422, detail=error_msg)
        
        # 3. Extract features using our DSP pipeline
        features = extract_features(y, target_sr)
        
        # 4. Reshape and scale features for the SVM
        features_scaled = scaler.transform(features.reshape(1, -1))
        
        # 5. Predict the clinical profile
        prediction = model.predict(features_scaled)[0]
        
        return {"filename": file.filename, "prediction": str(prediction)}
        
    except HTTPException:
        # Re-raise HTTPExceptions so they don't get swallowed by the generic Exception block
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
