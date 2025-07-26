from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    email: str
    message: str
    session_id: Optional[int] = None

class ChatResponse(BaseModel):
    session_id: int
    ai_reply: str
