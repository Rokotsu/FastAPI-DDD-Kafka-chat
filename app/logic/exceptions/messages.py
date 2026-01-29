from dataclasses import dataclass

from app.logic.exceptions.base import LogicException


@dataclass(eq=False)
class CheckWithThatTitleAlreadyExistsException(LogicException):
    title: str
    @property
    def message(self):
        return f'Чат с таким названием "{self.title}" уже существует'


@dataclass(eq=False)
class ChatNotFoundException(LogicException):
    chat_oid: str

    @property
    def message(self):
        return f'Чат с идентификатором "{self.chat_oid}" не найден'
