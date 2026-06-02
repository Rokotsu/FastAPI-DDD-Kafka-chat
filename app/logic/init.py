import os

from app.domain.events.messages import NewChatCreated, NewMessageReceivedEvent
from app.infra.kafka.config import KafkaBrokerConfig
from app.infra.kafka.producer import EventPublisher, KafkaEventProducer, NoopEventPublisher
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
from app.logic.events.messages import NewChatCreatedHandler, NewMessageReceivedEventHandler
from app.logic.mediator import Mediator


def init_mediator(
    mediator: Mediator,
    chat_repository: BaseChatRepository | None = None,
    event_publisher: EventPublisher | None = None,
) -> BaseChatRepository:
    repository = chat_repository or MemoryChatRepository()
    producer = event_publisher or _build_event_publisher()

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
        [CreateChatCommandHandler(chat_repository=repository, mediator=mediator)],
    )
    mediator.register_command(
        ListChatsCommand,
        [ListChatsCommandHandler(chat_repository=repository)],
    )
    mediator.register_command(
        GetChatCommand,
        [GetChatCommandHandler(chat_repository=repository)],
    )
    mediator.register_command(
        CreateMessageCommand,
        [CreateMessageCommandHandler(chat_repository=repository, mediator=mediator)],
    )
    return repository


def _build_event_publisher() -> EventPublisher:
    kafka_enabled = os.getenv("KAFKA_ENABLED", "false").strip().lower()
    if kafka_enabled in {"1", "true", "yes", "on"}:
        return KafkaEventProducer(config=KafkaBrokerConfig())
    return NoopEventPublisher()
