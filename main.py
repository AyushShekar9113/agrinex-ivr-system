from fastapi import FastAPI, BackgroundTasks
from models import voice # your 1100+ line AI agent
from concurrent.futures import ThreadPoolExecutor

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
