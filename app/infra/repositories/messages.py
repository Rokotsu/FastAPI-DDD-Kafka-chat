from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable

from motor.motor_asyncio import AsyncIOMotorClient

from app.domain.entities.messages import Chat, Message
from app.domain.values.messages import Text, Title


@dataclass
class BaseChatRepository(ABC):
    @abstractmethod
    async def check_chat_exists_by_title(self, title: str) -> bool:
        ...

    @abstractmethod
    async def add_chat(self, chat: Chat) -> None:
        ...

    @abstractmethod
    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        ...

    @abstractmethod
    async def get_chat_by_title(self, title: str) -> Chat | None:
        ...
@dataclass
class MemoryChatRepository(BaseChatRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(next(
                chat for chat in self._saved_chats if chat.title.as_generic_type() == title
            ))
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        try:
            return next(chat for chat in self._saved_chats if chat.oid == oid)
        except StopIteration:
            return None

    async def get_chat_by_title(self, title: str) -> Chat | None:
        try:
            return next(
                chat for chat in self._saved_chats if chat.title.as_generic_type() == title
            )
        except StopIteration:
            return None


@dataclass
class MongoChatRepository(BaseChatRepository):
    mongo_uri: str
    database_name: str
    collection_name: str = "chats"

    def __post_init__(self) -> None:
        client = AsyncIOMotorClient(self.mongo_uri)
        self._collection = client[self.database_name][self.collection_name]

    async def check_chat_exists_by_title(self, title: str) -> bool:
        return await self._collection.count_documents({"title": title}, limit=1) > 0

    async def add_chat(self, chat: Chat) -> None:
        await self._collection.insert_one(self._chat_to_document(chat))

    async def get_chat_by_oid(self, oid: str) -> Chat | None:
        document = await self._collection.find_one({"oid": oid})
        if not document:
            return None
        return self._document_to_chat(document)

    async def get_chat_by_title(self, title: str) -> Chat | None:
        document = await self._collection.find_one({"title": title})
        if not document:
            return None
        return self._document_to_chat(document)

    def _chat_to_document(self, chat: Chat) -> dict:
        return {
            "oid": chat.oid,
            "title": chat.title.as_generic_type(),
            "created_at": chat.created_at,
            "messages": [
                {
                    "oid": message.oid,
                    "text": message.text.as_generic_type(),
                    "created_at": message.created_at,
                }
                for message in self._messages_to_list(chat.messages)
            ],
        }

    def _document_to_chat(self, document: dict) -> Chat:
        messages = {
            Message(
                oid=message["oid"],
                text=Text(value=message["text"]),
                created_at=message["created_at"],
            )
            for message in document.get("messages", [])
        }
        return Chat(
            oid=document["oid"],
            title=Title(value=document["title"]),
            created_at=document["created_at"],
            messages=messages,
        )

    @staticmethod
    def _messages_to_list(messages: Iterable[Message]) -> list[Message]:
        return list(messages)
