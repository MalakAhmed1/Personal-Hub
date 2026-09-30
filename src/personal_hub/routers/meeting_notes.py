from fastapi import APIRouter
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

class MeetingNotesRequest(BaseModel):
    notes: str

class ActionItem(BaseModel):
    task: str
    owner: str

class MeetingNotesResponse(BaseModel):
    decisions: list[str]
    action_items: list[ActionItem]
    follow_up_questions: list[str]

def extract_meeting_notes(notes: str) -> MeetingNotesResponse:
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=f"Extract decisions, action items (with owner), and follow-up questions from these meeting notes:\n\n{notes}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MeetingNotesResponse,
        ),
    )
    assert isinstance(response.parsed, MeetingNotesResponse)
    return response.parsed

router = APIRouter(prefix="/hub/meeting-notes", tags=["meeting-notes"])

@router.get("/")
def status():
    return {"status": "meeting notes module is alive"}

@router.post("/", response_model=MeetingNotesResponse)
def analyze_meeting_notes(request: MeetingNotesRequest):
    result = extract_meeting_notes(request.notes)
    return result