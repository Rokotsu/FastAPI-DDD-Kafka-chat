from dataclasses import dataclass

from app.domain.events.messages import NewChatCreated, NewMessageReceivedEvent
from app.infra.kafka.producer import EventPublisher
from app.logic.events.base import EventHandler


@dataclass
class NewChatCreatedHandler(EventHandler[NewChatCreated, None]):
    producer: EventPublisher

    async def handle(self, event: NewChatCreated) -> None:
        await self.producer.publish(event)


@dataclass
class NewMessageReceivedEventHandler(EventHandler[NewMessageReceivedEvent, None]):
    producer: EventPublisher

    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.producer.publish(event)
