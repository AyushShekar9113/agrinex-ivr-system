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
    # return {"message": "Agent started"}
    exoml = """
            <Response>
                <Say>Welcome to AgriNex AI System. Please wait while we connect you to the AI Agent.</Say>
                    <Connect>
                            <Room>farmer-support</Room>
                    </Connect>
            </Response>
                """
    return Response(content=exoml.strip(), media_type="application/xml")
