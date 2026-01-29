from dataclasses import dataclass

from app.domain.events.messages import NewChatCreated, NewMessageReceivedEvent
from app.infra.kafka.producer import KafkaEventProducer
from app.logic.events.base import EventHandler


@dataclass(frozen=True)
class NewChatCreatedHandler(EventHandler[NewChatCreated, None]):
    producer: KafkaEventProducer

    async def handle(self, event: NewChatCreated) -> None:
        await self.producer.publish(event)


@dataclass(frozen=True)
class NewMessageReceivedEventHandler(EventHandler[NewMessageReceivedEvent, None]):
    producer: KafkaEventProducer

    async def handle(self, event: NewMessageReceivedEvent) -> None:
        await self.producer.publish(event)
