import abc
import typing

from telegrinder.types.objects import Message as MessageEvent

from .abc import ABCRule, CheckResult, Message
from .adapter import EventAdapter


class MessageRule(ABCRule[Message], abc.ABC):
    adapter: EventAdapter[Message] = EventAdapter(MessageEvent, Message)

    @abc.abstractmethod
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> CheckResult: ...


__all__ = ("MessageRule",)
