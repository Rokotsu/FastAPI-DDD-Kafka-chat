from app.domain.events.messages import NewChatCreated, NewMessageReceivedEvent
from app.infra.kafka.config import KafkaBrokerConfig
from app.infra.kafka.producer import KafkaEventProducer
from app.infra.repositories.messages import MemoryChatRepository, BaseChatRepository
from app.logic.commands.messages import CreateChatCommand, CreateChatCommandHandler
from app.logic.events.messages import NewChatCreatedHandler, NewMessageReceivedEventHandler
from app.infra.repositories.messages import BaseChatRepository
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
    chat_repository: BaseChatRepository,
):
    producer = KafkaEventProducer(config=KafkaBrokerConfig())

    mediator.register_event(
        NewChatCreated,
        [NewChatCreatedHandler(producer=producer)],
    )
    mediator.register_event(
        NewMessageReceivedEvent,
        [NewMessageReceivedEventHandler(producer=producer)],
    )
    mediator.register_command(
        CreateChatCommand,
        [CreateChatCommandHandler(chat_repository=chat_repository, mediator=mediator)],

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
