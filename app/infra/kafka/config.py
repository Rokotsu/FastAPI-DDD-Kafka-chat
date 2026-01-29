from dataclasses import dataclass, field
import os


@dataclass(frozen=True)
class KafkaBrokerConfig:
    bootstrap_servers: list[str] = field(
        default_factory=lambda: [
            host.strip()
            for host in os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092").split(",")
            if host.strip()
        ],
    )
    topic_prefix: str = os.getenv("KAFKA_TOPIC_PREFIX", "chat")
