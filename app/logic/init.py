from app.infra.repositories.messages import MemoryChatRepository, BaseChatRepository
from app.logic.commands.messages import (
    CreateChatCommand,
    CreateChatCommandHandler,
    CreateMessageCommand,
    CreateMessageCommandHandler,
    GetChatCommand,
    GetChatCommandHandler,
    ListChatsCommand,
    ListChatsCommandHandler,
)
from app.logic.mediator import Mediator

def init_mediator(
    mediator: Mediator,
    chat_repository: BaseChatRepository
):
    mediator.register_command(
        CreateChatCommand,
        [CreateChatCommandHandler(chat_repository=chat_repository)],

    )
    mediator.register_command(
        ListChatsCommand,
        [ListChatsCommandHandler(chat_repository=chat_repository)],
    )
    mediator.register_command(
        GetChatCommand,
        [GetChatCommandHandler(chat_repository=chat_repository)],
    )
    mediator.register_command(
        CreateMessageCommand,
        [CreateMessageCommandHandler(chat_repository=chat_repository)],
    )
