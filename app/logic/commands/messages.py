from dataclasses import dataclass

from app.domain.entities.messages import Chat, Message
from app.domain.values.messages import Title, Text
from app.infra.repositories.messages import BaseChatRepository
from app.logic.commands.base import BaseCommand, CommandHandler, CT, CR
from app.logic.mediator import Mediator

from app.logic.exceptions.messages import (
    CheckWithThatTitleAlreadyExistsException,
    ChatNotFoundException,
)


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str


@dataclass(frozen=True)
class ListChatsCommand(BaseCommand):
    ...


@dataclass(frozen=True)
class GetChatCommand(BaseCommand):
    chat_oid: str


@dataclass(frozen=True)
class CreateMessageCommand(BaseCommand):
    chat_oid: str
    text: str


@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository
    mediator: Mediator
    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise CheckWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)
        new_chat = Chat.create_chat(title=title)
        await self.chat_repository.add_chat(new_chat)
        events = new_chat.pull_events()
        for event in events:
            await self.mediator.handle_event(event)

        return new_chat


@dataclass(frozen=True)
class ListChatsCommandHandler(CommandHandler[ListChatsCommand, list[Chat]]):
    chat_repository: BaseChatRepository

    async def handle(self, command: ListChatsCommand) -> list[Chat]:
        return await self.chat_repository.list_chats()


@dataclass(frozen=True)
class GetChatCommandHandler(CommandHandler[GetChatCommand, Chat]):
    chat_repository: BaseChatRepository

    async def handle(self, command: GetChatCommand) -> Chat:
        chat = await self.chat_repository.get_chat_by_oid(command.chat_oid)
        if chat is None:
            raise ChatNotFoundException(command.chat_oid)
        return chat


@dataclass(frozen=True)
class CreateMessageCommandHandler(CommandHandler[CreateMessageCommand, Message]):
    chat_repository: BaseChatRepository

    async def handle(self, command: CreateMessageCommand) -> Message:
        message = Message(text=Text(value=command.text))
        chat = await self.chat_repository.add_message(command.chat_oid, message)
        if chat is None:
            raise ChatNotFoundException(command.chat_oid)
        chat.pull_events()
        return message
