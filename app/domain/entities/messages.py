from dataclasses import dataclass, field
from datetime import datetime

from app.domain.entities.base import BaseEntity
from app.domain.values.messages import Text, Title
from app.domain.events.messages import NewMessageReceivedEvent, NewChatCreated


@dataclass(eq=False)
class Message(BaseEntity):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )
    text: Text

@dataclass(eq=False)
class Chat(BaseEntity):
    created_at: datetime = field(
        default_factory=datetime.now,
        kw_only=True,
    )

    title: Title
    messages: set[Message] = field(
        default_factory=set,
        kw_only=True,
    )


    @classmethod
    def create_chat(cls, title: Title) -> 'Chat':
        new_chat = cls(title=title)
        new_chat.register_event(NewChatCreated(chat_oid=new_chat.oid, title=new_chat.title.as_generic_type()))

    def add_messages(self, message: Message):
        self.messages.add(message)
        self.register_event(NewMessageReceivedEvent(
            message_text=message.text.as_generic_type(),
            chat_oid=self.oid,
            message_oid=message.oid
        ))



