Lung Sound Classifier

A full-stack diagnostic application designed to analyze lung sound recordings (.wav) and categorize them into clinical profiles: Normal, Wheeze, or Crackle.

This system uses digital signal processing (DSP) to extract audio features (MFCCs) and an SVM-based machine learning model for automated classification.

Project Architecture

Frontend: A responsive web dashboard hosted on Cloudflare Pages, featuring real-time waveform and spectrogram visualization.

Backend: A FastAPI Python server hosted on Render, handling file processing and model inference.

CI/CD: Automated deployment pipelines via GitHub Actions.

How It Works

Upload: User uploads a .wav file through the dashboard.

Process: The backend normalizes the audio (4000 Hz resample) and performs a Bandpass filter (100–2000 Hz).

Analyze: The system extracts Mel-frequency cepstral coefficients (MFCCs).

Predict: The SVM model compares these features against trained profiles to generate a diagnosis.

Repository Structure

/
├── app/              # FastAPI backend logic
├── .github/          # CI/CD workflows for automated testing
├── Dockerfile        # Container configuration for Render
├── index.html        # Frontend dashboard
├── requirements.txt  # Backend dependencies
└── README.md         # Documentation


Setup & Development

Local Development

To run the project locally, ensure you have Python 3.9+ installed.

Install Dependencies:

pip install -r requirements.txt


Run Backend:

uvicorn app.main:app --reload


Frontend: Open index.html in any modern web browser.

Deployment

Frontend: Automatically deployed to Cloudflare Pages via GitHub integration.

Backend: Automatically built and deployed to Render using the provided Dockerfile.

Credits

Built by Prashanna Paudyal and Aashish Kumar Gami.
