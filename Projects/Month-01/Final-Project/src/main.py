import json
import uuid
import os

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from src.redis_client import r
from src.models import ChatRequest, ChatResponse, JobStatus
from src.worker import process_chat_job


app = FastAPI(title="🤖 Mini Chat Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def root():
    return {"message": "🤖 Mini Chat Backend চালু আছে!"}
    
    
@app.get("/health")
async def health():
    try:
        r.ping()
        return {"status": "ok", "redis": "connected ✅"}
    except:
        return {"status": "error", "redis": "disconnected ❌"}
    

@app.post("/chats", response_model = ChatResponse)
async def chat(
    request : ChatRequest,
    background_task : BackgroundTasks
):
    
    job_id = f"job:{uuid.uuid4().hex[:8]}"
    
    job_data = {
        "job_id": job_id,
        "session_id": request.session_id,
        "message": request.message,
        "model_name": request.model_name,
        "status": "queued",
        "result": None,
        "history": []
    }
    
    r.set(f"job:{job_id}", json.dumps(job_data))
    
    background_task.add_task(process_chat_job, job_id)
    
    return ChatResponse(
        session_id= request.session_id,
        job_id= job_id,
        status="queued",
        message="Processing message..."
    )


@app.get("/chat/{job_id}", response_model=JobStatus)
async def get_chat_result(job_id: str):
    """Job এর result দেখো"""

    data = r.get(f"job:{job_id}")
    if not data:
        raise HTTPException(
            status_code=404,
            detail="Job পাওয়া যায়নি!"
        )

    parsed = json.loads(data)
    return JobStatus(
        job_id=job_id,
        status=parsed["status"],
        result=parsed.get("result"),
        history=parsed.get("history", [])
    )


@app.get("/session/{session_id}")
async def get_session_history(session_id: str):
    """Session এর পুরো history দেখো"""

    history_raw = r.get(f"session:{session_id}")
    if not history_raw:
        return {"session_id": session_id, "history": []}

    return {
        "session_id": session_id,
        "history": json.loads(history_raw)
    }


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Session clear করো"""

    r.delete(f"session:{session_id}")
    return {"message": f"Session {session_id} clear হয়েছে ✅"}