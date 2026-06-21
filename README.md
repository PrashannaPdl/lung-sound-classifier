🫁 Lung Sound Classifier

A full-stack diagnostic application designed to analyze lung sound recordings (.wav) and categorize them into clinical profiles: Normal, Wheeze, or Crackle.

This system uses digital signal processing (DSP) to extract audio features (MFCCs) and an SVM-based machine learning model for automated classification.

🌐 Try It Live

Access our live diagnostic dashboard here:
👉 lungtest.paudyalprashanna.workers.dev

Simply upload a respiratory audio file and click "Diagnose" to see the AI in action! The system includes automatic invalid audio detection to reject background noise or speech.

🏗️ Project Architecture

Frontend: A responsive web dashboard hosted on Cloudflare Workers/Pages, featuring real-time waveform and spectrogram visualization.

Backend: A FastAPI Python server hosted on Render, handling file processing and model inference.

CI/CD: Automated deployment pipelines via GitHub Actions.

⚙️ How It Works

Upload: User uploads a .wav file through the dashboard.

Process: The backend normalizes the audio (4410 Hz resample) and performs a Bandpass filter (100–2000 Hz).

Analyze: The system runs a heuristic check (to filter out silence/music) and extracts Mel-frequency cepstral coefficients (MFCCs).

Predict: The SVM model compares these features against trained profiles to generate a diagnosis.

📂 Repository Structure

/
├── app/              # FastAPI backend logic (main.py)
├── .github/          # CI/CD workflows for automated testing
├── Dockerfile        # Container configuration for Render
├── dashboard.html    # Frontend interactive dashboard
├── requirements.txt  # Backend Python dependencies
└── README.md         # Documentation


🛠️ Setup & Development

Local Development

To run the project locally, ensure you have Python 3.9+ installed.

Install Dependencies:

pip install -r requirements.txt


Run Backend:

uvicorn app.main:app --reload


Frontend: Open dashboard.html in any modern web browser. (Note: Update API_URL in the HTML file to http://localhost:8000/predict if testing locally).

Deployment

Frontend: Deployed globally via Cloudflare.

Backend: Automatically built and deployed to Render using the provided Dockerfile.

👨‍💻 Credits

Built by Prashanna Paudyal and Aashish Kumar Gami.
