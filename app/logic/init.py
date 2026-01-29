import os

from app.infra.repositories.messages import BaseChatRepository, MongoChatRepository
from app.logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from app.logic.mediator import Mediator

def init_mediator(mediator: Mediator) -> None:
    chat_repository = _build_chat_repository()
    mediator.register_command(
        CreateChatCommand,
        [CreateChatCommandHandler(chat_repository=chat_repository)],

    )


def _build_chat_repository() -> BaseChatRepository:
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    database_name = os.getenv("MONGO_DB", "chat")
    collection_name = os.getenv("MONGO_CHAT_COLLECTION", "chats")
    return MongoChatRepository(
        mongo_uri=mongo_uri,
        database_name=database_name,
        collection_name=collection_name,
    )
