from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import time

app = FastAPI(
    title="Raichu Web Server (FastAPI)",
    description="Microserviço rápido para análises matemáticas e elétricas",
    version="1.0.0"
)

class StudyTask(BaseModel):
    id: int
    subject: str
    status: str
    priority: Optional[int] = 3

@app.get("/")
def read_root():
    return {
        "status": "ONLINE",
        "service": "Raichu Web Server",
        "timestamp": time.time()
    }

@app.get("/api/studies", response_model=List[StudyTask])
def get_study_tasks():
    return [
        StudyTask(id=1, subject="Matriz Ybus - SEP", status="In Progress", priority=1),
        StudyTask(id=2, subject="EDOs de 2ª ordem", status="Todo", priority=2)
    ]
