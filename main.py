from fastapi import FastAPI, BackgroundTasks
from models import voice # your 1100+ line AI agent
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AgriNex IVR is live! 🚜🎉"}

@app.post("/start-agent/")
async def start_agent(background_tasks: BackgroundTasks):
    with ThreadPoolExecutor() as pool:
        background_tasks.add_task(voice.main)  # this triggers your FULL agent
    return {"message": "Agent started"}
