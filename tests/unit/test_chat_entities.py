from app.domain.entities.messages import Chat, Message
from app.domain.events.messages import NewChatCreated, NewMessageReceivedEvent
from app.domain.values.messages import Text, Title


def test_create_chat_registers_event_and_sets_title():
    title = Title(value="Support")

    chat = Chat.create_chat(title=title)

    assert chat.title == title
    assert chat.messages == set()

    events = chat.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], NewChatCreated)
    assert events[0].chat_oid == chat.oid
    assert events[0].chat_title == title.as_generic_type()


def test_add_messages_adds_message_and_registers_event():
    chat = Chat.create_chat(title=Title(value="General"))
    chat.pull_events()
    message = Message(text=Text(value="Hello!"))

    chat.add_messages(message)

    assert message in chat.messages

    events = chat.pull_events()
    assert len(events) == 1
    assert isinstance(events[0], NewMessageReceivedEvent)
    assert events[0].chat_oid == chat.oid
    assert events[0].message_oid == message.oid
    assert events[0].message_text == message.text.as_generic_type()
