# 🫁 Lung Sound Classifier

An intelligent respiratory diagnostic tool that listens to audio recordings of breathing and detects clinical anomalies. Built by Prashanna Paudyal and Aashish Kumar Gami.

## 🧠 What It Is (The Layman Version)
Think of this as a digital stethoscope powered by AI. You upload a recording of someone breathing, and the system instantly analyzes the sound waves. It acts as a screening tool to tell you if the breathing is **Normal**, or if it contains abnormal patterns like a **Wheeze** (often linked to asthma) or a **Crackle** (often linked to fluid in the lungs).

## ⚙️ How It Works (The Technical Version)
Behind the simple dashboard lies a robust machine learning and audio engineering pipeline:

* **Digital Signal Processing (DSP) & Heuristics:** Before the AI even looks at the file, the backend runs a sanity check. It measures the *Spectral Centroid* and *Zero-Crossing Rate* to filter out invalid audio. If you upload a song or speech, the system rejects it immediately to prevent false medical predictions.
* **Feature Extraction (MFCCs):** The raw audio is passed through a *Bandpass Filter* (100–2000 Hz) to isolate respiratory frequencies. Then, we extract 13 *Mel-frequency cepstral coefficients (MFCCs)*, which mathematically represent the "acoustic fingerprint" of the patient's vocal tract and airways.
* **Machine Learning Inference (SVM):** The extracted features are scaled and fed into a pre-trained *Support Vector Machine (SVM)*. This model plots the data in high-dimensional space to accurately classify the lung sound into its clinical profile.

## 🛠️ Tech Stack
* **Frontend:** Pure HTML, JavaScript, and Tailwind CSS (Zero framework bloat, interactive canvas graphs).
* **Backend:** Python and FastAPI (Lightning-fast API routing).
* **Audio Processing:** Librosa and NumPy.
* **Deployment:** Containerized via Docker and hosted live on Render.

## 🚀 Quick Start Guide

### 1. Try the Live Demo
Simply open `dashboard.html` in your web browser. It is already wired to our live production backend!

### 2. Run the Backend Locally
If you want to run the prediction server on your own machine:

1. Clone the repository.
2. Install the core dependencies:
   `pip install -r requirements.txt`
3. Spin up the FastAPI server:
   `uvicorn app.main:app --reload`
4. Open `dashboard.html`, change the `API_URL` variable to `http://localhost:8000/predict`, and start diagnosing.

---
*Disclaimer: This is an experimental machine learning project and is not a substitute for professional medical advice or clinical diagnosis.*
