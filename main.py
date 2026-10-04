from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, HTMLResponse
import os
from config import Config
from orchestrator import MasterOrchestrator
from registry import AgentRegistry

app = FastAPI(title="Agent Factory Master")

# Setup templates and static files
templates = Jinja2Templates(directory=Config.BASE_DIR)

orchestrator = MasterOrchestrator()
registry = AgentRegistry()

@app.get("/static/styles.css")
async def styles():
    return FileResponse(os.path.join(Config.BASE_DIR, "styles.css"), media_type="text/css")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    agents = registry.get_all_agents()
    return templates.TemplateResponse("index.html", {"request": request, "agents": agents})

@app.post("/generate")
async def generate_agents(request: Request, instruction: str = Form(...)):
    # Run the orchestrator process
    result = orchestrator.process_instruction(instruction)
    
    # Reload agents for dashboard
    agents = registry.get_all_agents()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "agents": agents,
        "last_result": result
    })