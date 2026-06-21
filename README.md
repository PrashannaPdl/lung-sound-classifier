🫁 Lung Sound ClassifierAn AI-powered respiratory diagnostic web application. Leveraging digital signal processing and a Support Vector Machine, the system analyzes audio recordings to instantly classify lung sounds into normal, wheeze, or crackle profiles via an interactive clinical dashboard.🌐 Try It LiveAccess our live diagnostic dashboard here: 👉 lungtest.paudyalprashanna.workers.devHow to Use the System:Open the live dashboard link above.Click "Choose File" to upload a respiratory .wav audio file.Click "Diagnose" to initiate the AI analysis.View your results on the interactive waveform and spectrogram! You can use your mouse wheel to zoom in and drag to pan across the timeline.(Note: The system includes a smart heuristic filter that automatically rejects non-respiratory sounds like background noise, music, or speech.)📂 Repository StructureHere is a quick overview of the files powering this project:/
├── app/              # FastAPI backend logic handling audio processing and AI inference
├── .github/          # Automated GitHub Actions deployment workflows
├── Dockerfile        # Container configuration for deploying the backend to Render
├── index.html        # The interactive frontend dashboard UI (HTML/JS/Tailwind)
├── requirements.txt  # List of Python dependencies for the backend
└── README.md         # Project documentation
👨‍💻 CreditsBuilt by Prashanna Paudyal and Aashish Kumar Gami.
