import dataclasses
import typing

import msgspec

from telegrinder.api.api import API
from telegrinder.bot.cute_types import BaseCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.msgspec_utils import DataclassInstance, decoder
from telegrinder.node.base import ComposeError, FactoryNode
from telegrinder.node.update import UpdateNode

if typing.TYPE_CHECKING:
    Dataclass = typing.TypeVar("Dataclass", bound="DataclassType")

    DataclassType: typing.TypeAlias = DataclassInstance | msgspec.Struct | dict[str, typing.Any]

EVENT_NODE_KEY = "_event_node"


class _EventNode(FactoryNode):
    dataclass: type["DataclassType"]

    def __class_getitem__(cls, dataclass: type["DataclassType"], /) -> typing.Self:
        return cls(dataclass=dataclass)

    @classmethod
    def compose(cls, raw_update: UpdateNode, ctx: Context, api: API) -> "DataclassType":
        dataclass_type = typing.get_origin(cls.dataclass) or cls.dataclass

        try:
            if issubclass(dataclass_type, BaseCute):
                if isinstance(raw_update.incoming_update, dataclass_type):
                    dataclass = raw_update.incoming_update
                else:
                    dataclass = dataclass_type.from_update(raw_update.incoming_update, bound_api=api)

            elif issubclass(dataclass_type, msgspec.Struct | dict) or dataclasses.is_dataclass(
                dataclass_type
            ):
                dataclass = decoder.convert(
                    raw_update.incoming_update.to_full_dict(),
                    type=cls.dataclass,
                    str_keys=True,
                )

            else:
                dataclass = cls.dataclass(**raw_update.incoming_update.to_dict())

            ctx[EVENT_NODE_KEY] = cls
            return dataclass
        except Exception as exc:
            raise ComposeError(f"Cannot parse update into {cls.dataclass.__name__!r}, error: {str(exc)!r}")


if typing.TYPE_CHECKING:
    EventNode: typing.TypeAlias = typing.Annotated["Dataclass", ...]

else:

    class EventNode(_EventNode):
        pass


__all__ = ("EventNode",)
