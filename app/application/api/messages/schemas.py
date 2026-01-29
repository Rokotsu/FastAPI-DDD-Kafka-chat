from datetime import datetime

from pydantic import BaseModel, Field


class ChatCreateRequest(BaseModel):
    title: str = Field(..., max_length=255)


class ChatResponse(BaseModel):
    oid: str
    title: str
    created_at: datetime


class MessageCreateRequest(BaseModel):
    text: str


class MessageResponse(BaseModel):
    oid: str
    text: str
    created_at: datetime


class ChatDetailResponse(ChatResponse):
    messages: list[MessageResponse]
