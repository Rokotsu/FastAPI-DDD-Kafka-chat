from datetime import datetime
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.logic.commands.messages import CreateChatCommand
from app.logic.exceptions.messages import CheckWithThatTitleAlreadyExistsException
from app.logic.init import init_mediator
from app.logic.mediator import Mediator

router = APIRouter(prefix="/api/chats", tags=["chats"])


class ChatCreateRequest(BaseModel):
    title: str


class ChatResponse(BaseModel):
    oid: str
    title: str
    created_at: datetime


class ChatService:
    def __init__(self, mediator: Mediator):
        self._mediator = mediator

    async def create_chat(self, title: str) -> ChatResponse:
        results = await self._mediator.handle_command(CreateChatCommand(title=title))
        chat = results[0]
        return ChatResponse(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
        )


@lru_cache
def get_mediator() -> Mediator:
    mediator = Mediator()
    init_mediator(mediator=mediator)
    return mediator


def get_chat_service(mediator: Mediator = Depends(get_mediator)) -> ChatService:
    return ChatService(mediator=mediator)


@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    payload: ChatCreateRequest,
    service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    try:
        return await service.create_chat(payload.title)
    except CheckWithThatTitleAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.message,
        ) from exc
