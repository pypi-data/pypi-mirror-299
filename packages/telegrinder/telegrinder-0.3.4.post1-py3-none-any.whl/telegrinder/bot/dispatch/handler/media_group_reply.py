import typing

from telegrinder.api.api import API
from telegrinder.bot.cute_types.message import InputMediaType, MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.handler.base import BaseReplyHandler
from telegrinder.bot.rules.abc import ABCRule


class MediaGroupReplyHandler(BaseReplyHandler):
    def __init__(
        self,
        media: InputMediaType | list[InputMediaType],
        *rules: ABCRule,
        caption: str | list[str] | None = None,
        parse_mode: str | list[str] | None = None,
        is_blocking: bool = True,
        as_reply: bool = False,
        preset_context: Context | None = None,
        **default_params: typing.Any,
    ) -> None:
        self.media = media
        self.parse_mode = parse_mode
        self.caption = caption
        super().__init__(
            *rules,
            is_blocking=is_blocking,
            as_reply=as_reply,
            preset_context=preset_context,
            **default_params,
        )

    async def run(self, _: API, event: MessageCute, __: Context) -> typing.Any:
        method = event.answer_media_group if not self.as_reply else event.reply_media_group
        await method(
            media=self.media,
            parse_mode=self.parse_mode,
            caption=self.caption,
            **self.default_params,
        )


__all__ = ("MediaGroupReplyHandler",)
