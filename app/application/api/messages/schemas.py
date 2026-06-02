from datetime import datetime

from pydantic import BaseModel, Field


class ChatCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)


class ChatResponse(BaseModel):
    oid: str
    title: str
    created_at: datetime


class MessageCreateRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)


class MessageResponse(BaseModel):
    oid: str
    text: str
    created_at: datetime


class ChatDetailResponse(ChatResponse):
    messages: list[MessageResponse]
