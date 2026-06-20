from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Enable CORS so your Cloudflare frontend can communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    # 1. Read the uploaded file
    # audio_data = await file.read()
    
    # 2. Add your ML model inference logic here
    # Placeholder response to test the connection:
    return {"filename": file.filename, "prediction": "NORMAL"}

if __name__ == "__main__":
    import uvicorn
    # This ensures the app binds to the correct port when hosted on Render
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
