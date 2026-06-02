import json
from dataclasses import asdict, is_dataclass
from typing import Any, Protocol

from app.domain.events.base import BaseEvent

from app.infra.kafka.config import KafkaBrokerConfig


class EventPublisher(Protocol):
    async def publish(self, event: BaseEvent) -> None:
        ...

    async def stop(self) -> None:
        ...


class NoopEventPublisher:
    async def publish(self, event: BaseEvent) -> None:
        return None

    async def stop(self) -> None:
        return None


class KafkaEventProducer:
    def __init__(self, config: KafkaBrokerConfig) -> None:
        self._config = config
        self._producer: Any | None = None

    async def publish(self, event: BaseEvent) -> None:
        producer = await self._get_producer()
        topic = self._topic_for(event)
        payload = self._serialize_event(event)
        await producer.send_and_wait(topic, payload)

    async def stop(self) -> None:
        if self._producer is None:
            return
        await self._producer.stop()
        self._producer = None

    async def _get_producer(self) -> Any:
        if self._producer is None:
            try:
                from aiokafka import AIOKafkaProducer
            except ImportError as exc:
                raise RuntimeError(
                    "Kafka support requires the aiokafka package. "
                    "Install project dependencies or disable KAFKA_ENABLED."
                ) from exc

            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._config.bootstrap_servers,
            )
            await self._producer.start()
        return self._producer

    def _topic_for(self, event: BaseEvent) -> str:
        return f"{self._config.topic_prefix}.{event.__class__.__name__}"

    def _serialize_event(self, event: BaseEvent) -> bytes:
        payload = {
            "type": event.__class__.__name__,
            "payload": asdict(event) if is_dataclass(event) else event.__dict__,
        }
        return json.dumps(payload, ensure_ascii=False).encode("utf-8")
