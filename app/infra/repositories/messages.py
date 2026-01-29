from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterable

from app.domain.entities.messages import Chat, Message


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
    async def list_chats(self) -> list[Chat]:
        ...

    @abstractmethod
    async def get_chat_by_oid(self, chat_oid: str) -> Chat | None:
        ...

    @abstractmethod
    async def add_message(self, chat_oid: str, message: Message) -> Chat | None:
        ...


@dataclass
class MemoryChatRepository(BaseChatRepository):
    _saved_chats: list[Chat] = field(default_factory=list, kw_only=True)

    async def check_chat_exists_by_title(self, title: str) -> bool:
        try:
            return bool(
                next(
                    chat
                    for chat in self._saved_chats
                    if chat.title.as_generic_type() == title
                )
            )
        except StopIteration:
            return False

    async def add_chat(self, chat: Chat) -> None:
        self._saved_chats.append(chat)

    async def list_chats(self) -> list[Chat]:
        return list(self._saved_chats)

    async def get_chat_by_oid(self, chat_oid: str) -> Chat | None:
        try:
            return next(chat for chat in self._saved_chats if chat.oid == chat_oid)
        except StopIteration:
            return None

    async def add_message(self, chat_oid: str, message: Message) -> Chat | None:
        chat = await self.get_chat_by_oid(chat_oid)
        if chat is None:
            return None
        chat.add_messages(message)
        return chat
