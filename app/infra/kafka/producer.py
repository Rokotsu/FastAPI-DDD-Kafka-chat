import json
from dataclasses import asdict, is_dataclass

from aiokafka import AIOKafkaProducer

from app.domain.events.base import BaseEvent

from app.infra.kafka.config import KafkaBrokerConfig


class KafkaEventProducer:
    def __init__(self, config: KafkaBrokerConfig) -> None:
        self._config = config
        self._producer: AIOKafkaProducer | None = None

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

    async def _get_producer(self) -> AIOKafkaProducer:
        if self._producer is None:
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
