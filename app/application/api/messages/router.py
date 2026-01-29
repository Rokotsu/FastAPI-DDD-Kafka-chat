from datetime import datetime
from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.domain.exceptions.messages import ApplicationException
from app.infra.repositories.messages import MemoryChatRepository
from app.logic.commands.messages import (
    CreateChatCommand,
    CreateMessageCommand,
    GetChatCommand,
    ListChatsCommand,
)
from app.logic.exceptions.messages import (
    ChatNotFoundException,
    CheckWithThatTitleAlreadyExistsException,
)
from app.logic.init import init_mediator
from app.logic.mediator import Mediator

router = APIRouter(prefix="/api/chats", tags=["chats"])


class ChatCreateRequest(BaseModel):
    title: str


class MessageCreateRequest(BaseModel):
    text: str


class ChatResponse(BaseModel):
    oid: str
    title: str
    created_at: datetime


class MessageResponse(BaseModel):
    oid: str
    text: str
    created_at: datetime


class ChatDetailResponse(ChatResponse):
    messages: list[MessageResponse]


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

    async def list_chats(self) -> list[ChatResponse]:
        results = await self._mediator.handle_command(ListChatsCommand())
        chats = results[0]
        return [
            ChatResponse(
                oid=chat.oid,
                title=chat.title.as_generic_type(),
                created_at=chat.created_at,
            )
            for chat in chats
        ]

    async def get_chat(self, chat_oid: str) -> ChatDetailResponse:
        results = await self._mediator.handle_command(GetChatCommand(chat_oid=chat_oid))
        chat = results[0]
        return ChatDetailResponse(
            oid=chat.oid,
            title=chat.title.as_generic_type(),
            created_at=chat.created_at,
            messages=[
                MessageResponse(
                    oid=message.oid,
                    text=message.text.as_generic_type(),
                    created_at=message.created_at,
                )
                for message in sorted(chat.messages, key=lambda item: item.created_at)
            ],
        )

    async def create_message(self, chat_oid: str, text: str) -> MessageResponse:
        results = await self._mediator.handle_command(
            CreateMessageCommand(chat_oid=chat_oid, text=text)
        )
        message = results[0]
        return MessageResponse(
            oid=message.oid,
            text=message.text.as_generic_type(),
            created_at=message.created_at,
        )


@lru_cache
def get_mediator() -> Mediator:
    mediator = Mediator()
    chat_repository = MemoryChatRepository()
    init_mediator(mediator=mediator, chat_repository=chat_repository)
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
    except ApplicationException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message,
        ) from exc
    except CheckWithThatTitleAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.message,
        ) from exc


@router.get("", response_model=list[ChatResponse])
async def list_chats(
    service: ChatService = Depends(get_chat_service),
) -> list[ChatResponse]:
    return await service.list_chats()


@router.get("/{chat_oid}", response_model=ChatDetailResponse)
async def get_chat(
    chat_oid: str,
    service: ChatService = Depends(get_chat_service),
) -> ChatDetailResponse:
    try:
        return await service.get_chat(chat_oid)
    except ChatNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        ) from exc


@router.post("/{chat_oid}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_oid: str,
    payload: MessageCreateRequest,
    service: ChatService = Depends(get_chat_service),
) -> MessageResponse:
    try:
        return await service.create_message(chat_oid, payload.text)
    except ChatNotFoundException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.message,
        ) from exc
    except ApplicationException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message,
        ) from exc
