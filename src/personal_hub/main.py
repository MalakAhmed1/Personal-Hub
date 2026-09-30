from personal_hub.routers import meeting_notes
from fastapi import FastAPI

app = FastAPI()

app.include_router(meeting_notes.router)
