from fastapi import FastAPI, BackgroundTasks,Request
from models import voice # your 1100+ line AI agent
from concurrent.futures import ThreadPoolExecutor
from gtts import gTTS
from fastapi.responses import Response
import os
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AgriNex IVR is live! 🚜🎉"}

# @app.api_route("/start-agent/", methods=["GET", "POST"])
@app.post("/start-agent/")
async def start_agent(background_tasks: BackgroundTasks):
    # 1. Trigger AI Agent logic in background
    background_tasks.add_task(voice.main)

    # 2. Send XML back to Exotel so it doesn't cut the call
    exoml = """
    <Response>
        <Say>Welcome to AgriNex AI System. Please wait while we connect you.</Say>
        <Connect>
            <Room>farmer-support</Room>
        </Connect>
    </Response>
    """
    return Response(content=exoml.strip(), media_type="application/xml")
# Endpoint to handle asking the agent
@app.post("/ask-agent/")
async def ask_agent(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    # Call the process_message_and_generate_audio function from voice.py
    ai_response, audio_file_name = voice.process_message_and_generate_audio(user_message)
    
    # Construct the URL for the audio file
    audio_url = f"https://your-backend-url/audio/{audio_file_name}"
    
    return {"reply": ai_response, "audio_url": audio_url}

# Endpoint to serve the generated audio files
@app.get("/audio/{audio_file_name}")
async def get_audio(audio_file_name: str):
    audio_file_path = os.path.join("audio", audio_file_name)
    return FileResponse(audio_file_path, media_type="audio/mp3")
