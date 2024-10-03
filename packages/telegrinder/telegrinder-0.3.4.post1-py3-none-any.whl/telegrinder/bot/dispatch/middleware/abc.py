import typing
from abc import ABC

from telegrinder.bot.dispatch.context import Context
from telegrinder.model import Model
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.rules.adapter.abc import ABCAdapter

Event = typing.TypeVar("Event", bound=Model)


class ABCMiddleware(ABC, typing.Generic[Event]):
    adapter: "ABCAdapter[Update, Event] | None" = None

    async def pre(self, event: Event, ctx: Context) -> bool: ...

    async def post(self, event: Event, responses: list[typing.Any], ctx: Context) -> None: ...


__all__ = ("ABCMiddleware",)
