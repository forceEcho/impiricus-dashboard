from typing import Any

from fastapi import APIRouter, HTTPException, Query
from sqlmodel import  select

from app.api.deps import SessionDep
from app.models import Message, MessageCreate, MessagePublic, MessagesPublic
from datetime import datetime

router = APIRouter(prefix="/messages")


@router.get("/", response_model=MessagesPublic)
async def read_messages(
    session: SessionDep,
    physician: int | None = Query(None), 
    fromDate: datetime | None = Query(None),
    toDate: datetime | None = Query(None)
) -> Any:
    """
    Retrieve messages.
    """
    statement = select(Message)
    if physician:
        statement=statement.where(Message.physician_id==physician)
    if fromDate:
        statement=statement.where(Message.timestamp >= fromDate)
    if toDate:
        statement=statement.where(Message.timestamp <= toDate)
    messages = session.exec(statement).all()
    
    messages_public = [MessagePublic.model_validate(m) for m in messages]

    return MessagesPublic(data=messages_public, count=len(messages))


@router.get("/{id}", response_model=Message)
async def read_message(session: SessionDep, id: int) -> Any:
    """
    Get message by ID.
    """
    message = session.get(Message, Message.message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

#not needed but wanted to test

@router.post("/", response_model=MessagePublic)
def create_message(
    *, session: SessionDep, mess_in: MessageCreate
) -> Any:
    
    message = Message.model_validate(mess_in)
    session.add(message)
    session.commit()
    session.refresh(message)
    return message