# 🫁 Lung Sound Classifier

An AI-powered respiratory diagnostic web application. Leveraging digital signal processing and a Support Vector Machine, the system analyzes audio recordings to instantly classify lung sounds into normal, wheeze, or crackle profiles via an interactive clinical dashboard.

## 🌐 Try It Live

Access our live diagnostic dashboard here: [https://lungtest.paudyalprashanna.workers.dev](https://www.google.com/search?q=https://lungtest.paudyalprashanna.workers.dev)

### How to Use the System:

1. Open the live dashboard link above.
2. Click "Choose File" to upload a respiratory .wav audio file.
3. Click "Diagnose" to initiate the AI analysis.
4. View your results on the interactive waveform and spectrogram! You can use your mouse wheel to zoom in and drag to pan across the timeline.

(Note: The system includes a smart heuristic filter that automatically rejects non-respiratory sounds like background noise, music, or speech.)

## 📂 Repository Structure

Here is a quick overview of the files powering this project:

/
├── app/              # FastAPI backend logic handling audio processing and AI inference
├── .github/          # Automated GitHub Actions deployment workflows
├── Dockerfile        # Container configuration for deploying the backend to Render
├── dashboard.html    # The interactive frontend dashboard UI (HTML/JS/Tailwind)
├── requirements.txt  # List of Python dependencies for the backend
└── README.md         # Project documentation

## 👨‍💻 Credits

Built by Prashanna Paudyal and Aashish Kumar Gami.
