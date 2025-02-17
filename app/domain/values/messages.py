from dataclasses import dataclass

from app.domain.exceptions.messages import TextTooLongException, EmptyTextError
from app.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Text(BaseValueObject):

    value: str
    def validate(self):
        if not self.value:
            raise EmptyTextError()

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Title(BaseValueObject):
    def validate(self):
        if not self.value:
            raise EmptyTextError()

        if len(self.value) > 255:
            raise TextTooLongException(self.value)

    def as_generic_type(self):
        return str(self.value)