from functools import lru_cache

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.api.messages.schemas import ChatCreateRequest, ChatResponse
from app.domain.exceptions import messages as domain_exceptions
from app.infra.repositories.messages import MemoryChatRepository
from app.logic.commands.messages import CreateChatCommand
from app.logic.exceptions.messages import CheckWithThatTitleAlreadyExistsException
from app.logic.init import init_mediator
from app.logic.mediator import Mediator

router = APIRouter(prefix="/api/chats", tags=["chats"])


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
    except CheckWithThatTitleAlreadyExistsException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.message,
        ) from exc
    except domain_exceptions.EmptyTextException as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=exc.message,
        ) from exc
    except (
        domain_exceptions.TextTooLongException,
        domain_exceptions.TitleTooLongException,
    ) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=exc.message,
        ) from exc
