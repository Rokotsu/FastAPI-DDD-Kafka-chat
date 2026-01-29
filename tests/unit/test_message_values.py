import pytest

from app.domain.exceptions.messages import EmptyTextException, TitleTooLongException
from app.domain.values.messages import Text, Title


def test_text_requires_value():
    with pytest.raises(EmptyTextException):
        Text(value="")


def test_text_as_generic_type_returns_string():
    text = Text(value="Hi")

    assert text.as_generic_type() == "Hi"


def test_title_requires_value():
    with pytest.raises(EmptyTextException):
        Title(value="")


def test_title_rejects_long_titles():
    long_title = "t" * 256

    with pytest.raises(TitleTooLongException):
        Title(value=long_title)


def test_title_as_generic_type_returns_string():
    title = Title(value="Welcome")

    assert title.as_generic_type() == "Welcome"
