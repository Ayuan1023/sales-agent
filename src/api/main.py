# -*- coding: utf-8 -*-
"""FastAPI主应用 - 智能销售Agent"""
import os, sys
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

RESEARCH_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if RESEARCH_ROOT not in sys.path:
    sys.path.insert(0, RESEARCH_ROOT)

from src.agent.agent import SalesAgent
from src.api.models import LeadRequest, ReplyRequest, MeetingRequest, HealthResponse

app = FastAPI(title="智能销售Agent", version="1.0.0")
agent = SalesAgent()


@app.get("/api/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", modules={
        "enricher": True, "scorer": True, "email_generator": True,
        "followup": True, "reply_handler": True, "meeting": True,
        "crm": True, "dashboard": True,
    })


@app.post("/api/lead/new")
async def new_lead(req: LeadRequest):
    return agent.process_new_lead(req.company_name, req.contact_name)


@app.post("/api/lead/reply")
async def handle_reply(req: ReplyRequest):
    return agent.handle_reply(req.lead_id, req.reply_text)


@app.post("/api/lead/meeting")
async def schedule_meeting(req: MeetingRequest):
    return agent.schedule_meeting(req.lead_id, req.slot_id)


@app.post("/api/lead/followup/{lead_id}")
async def send_followup(lead_id: str):
    return agent.send_followup(lead_id)


@app.get("/api/leads")
async def list_leads(grade: str = None):
    return {"leads": agent.get_leads(grade)}


@app.get("/api/lead/{lead_id}")
async def lead_detail(lead_id: str):
    return agent.get_lead_detail(lead_id)


@app.get("/api/roi")
async def roi_stats():
    return agent.get_roi_stats()


@app.get("/api/sync-log")
async def sync_log():
    return {"logs": agent.crm.get_sync_log(30)}


static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "static")
static_dir = os.path.normpath(static_dir)
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def index():
    return FileResponse(os.path.join(static_dir, "index.html"))


@app.get("/dashboard")
async def dashboard():
    return FileResponse(os.path.join(static_dir, "dashboard.html"))
