from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field


from app.domain.events.base import BaseEvent
from app.logic.commands.base import CommandHandler, CT, CR, BaseCommand
from app.logic.events.base import EventHandler, ET, ER
from app.logic.exceptions.mediator import EventHandlersNotRegisteredException, CommandHandlersNotRegisteredException


@dataclass(eq=False)
class Mediator:
    events_map: dict[ET, EventHandler] = field(
        default_factory=lambda: defaultdict(list),
        km_only=True,
    )
    commands_map: dict[CT, CommandHandler] = field(
        default_factory=lambda: defaultdict(list),
        km_only=True,
    )

    def register_event(self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]]):
        self.events_map[event.__class__].append(event_handlers)

    def register_command(self, command: CT, command_handlers: Iterable[EventHandler[CT, CR]]):
        self.events_map[command.__class__].extend(command_handlers)

    async def handle_event(self, event: BaseEvent) -> Iterable[ER]:
        event_type = event.__class__
        handlers = self.events_map.get(event_type)

        if not handlers:
            raise EventHandlersNotRegisteredException(event_type)
        return [await handler.handle(event) for handler in handlers]
    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.events_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredException(command_type)
        return [await handler.handle(command) for handler in handlers]


