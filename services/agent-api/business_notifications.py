from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api/business", tags=["business"])


class LeadNotification(BaseModel):
    source: str = "portfolio"
    name: str
    email: str
    company: str | None = None
    project_type: str | None = None
    budget: str | None = None
    message: str | None = None


@router.post("/lead")
async def receive_lead(lead: LeadNotification):
    timestamp = datetime.now().isoformat()

    lead_data = {
        "type": "new_lead",
        "timestamp": timestamp,
        "source": lead.source,
        "name": lead.name,
        "email": lead.email,
        "company": lead.company,
        "project_type": lead.project_type,
        "budget": lead.budget,
        "message": lead.message,
    }

    return {
        "success": True,
        "message": "Lead received by JARVIS.",
        "lead": lead_data,
    }