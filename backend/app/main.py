from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base, User, ConversationSession, Message
from schemas import ChatRequest, ChatResponse
from llm import get_ai_response

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if req.session_id:
        session = db.query(ConversationSession)\
                    .filter_by(id=req.session_id, user_id=user.id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
    else:
        session = ConversationSession(user_id=user.id)
        db.add(session)
        db.commit()
        db.refresh(session)

    user_msg = Message(session_id=session.id, sender="user", content=req.message)
    db.add(user_msg)
    db.commit()

    ai_reply = get_ai_response(req.message)

    ai_msg = Message(session_id=session.id, sender="ai", content=ai_reply)
    db.add(ai_msg)
    db.commit()

    return ChatResponse(session_id=session.id, ai_reply=ai_reply)
