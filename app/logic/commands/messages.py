from dataclasses import dataclass

from app.domain.entities.messages import Chat
from app.domain.values.messages import Title
from app.infra.repositories.messages import BaseChatRepository
from app.logic.commands.base import BaseCommand, CommandHandler, CT, CR

from app.logic.exceptions.messages import CheckWithThatTitleAlreadyExistsException


@dataclass(frozen=True)
class CreateChatCommand(BaseCommand):
    title: str
@dataclass(frozen=True)
class CreateChatCommandHandler(CommandHandler[CreateChatCommand, Chat]):
    chat_repository: BaseChatRepository
    async def handle(self, command: CreateChatCommand) -> Chat:
        if await self.chat_repository.check_chat_exists_by_title(command.title):
            raise CheckWithThatTitleAlreadyExistsException(command.title)

        title = Title(value=command.title)
        new_chat = Chat.create_chat(title=title)
        #TODO считать ивенты
        await self.chat_repository.add_chat(new_chat)

        return new_chat



