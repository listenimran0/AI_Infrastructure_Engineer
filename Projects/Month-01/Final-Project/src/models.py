from pydantic import BaseModel, field_validator
from typing import Optional, List

from pydantic_core.core_schema import none_schema

class Message(BaseModel):
    role: str
    content: str
    
class ChatRequest(BaseModel):
    session_id: str
    message: str
    model_name: str = "llama-3" 
    
    @field_validator("message")
    @classmethod
    def message_not_empty(cls,v):
        
        if not v.strip():
            raise ValueError("Message cant be empty")
        return v
    
    @field_validator("model_name")
    @classmethod
    def model_must_be_valid(cls,v):
        
        allowed = ["llama-3", "gpt-4", "claude"]
        if  v not in allowed:
            raise ValueError("Model is not allowed")
        return v
    
    
    
class ChatResponse(BaseModel):
    session_id: str
    job_id: str
    status: str
    message: str
    
    
class JobStatus(BaseModel):
    job_id: str
    status: str
    result: Optional[str] = None
    history: Optional[List[Message]] = None
    
    