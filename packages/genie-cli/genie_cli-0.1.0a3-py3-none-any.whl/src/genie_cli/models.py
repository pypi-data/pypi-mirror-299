from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TYPE_CHECKING


from src.genie_cli.config import LaunchConfig, ServiceChatModel, launch_config

if TYPE_CHECKING:
    from litellm.types.completion import ChatCompletionMessageParam


class UnknownModel(ServiceChatModel):
    pass


def get_model(
    model_id_or_name: str, config: LaunchConfig | None = None
) -> ServiceChatModel:
    """Given the id or name of a model as a string, return the EliaChatModel.

    Models are looked up by ID first.
    """
    if config is None:
        config = launch_config.get()
    try:
        return {model.id: model for model in config.all_models}[model_id_or_name]
    except KeyError:
        try:
            return {model.name: model for model in config.all_models}[model_id_or_name]
        except KeyError:
            pass
    return UnknownModel(id="unknown", name="unknown model")


@dataclass
class ChatMessage:
    message: ChatCompletionMessageParam
    timestamp: datetime | None
    model: ServiceChatModel


@dataclass
class ChatData:
    id: int | None  # Can be None before the chat gets assigned ID from database.
    model: ServiceChatModel
    title: str | None
    create_timestamp: datetime | None
    messages: list[ChatMessage]

    @property
    def short_preview(self) -> str:
        first_message = self.first_user_message.message

        if "content" in first_message:
            first_message = first_message["content"]  # type: ignore
            # We have content, but it's not guaranteed to be a string quite yet.
            # In the case of tool calls or image generation requests, we can
            # have non-string types here. We're not handling/considering this atm.
            if first_message and isinstance(first_message, str):
                if len(first_message) > 77:
                    return first_message[:77] + "..."
                else:
                    return first_message

        return ""

    @property
    def system_prompt(self) -> ChatMessage:
        return self.messages[0]

    @property
    def first_user_message(self) -> ChatMessage:
        return self.messages[1]

    @property
    def non_system_messages(
        self,
    ) -> list[ChatMessage]:
        return self.messages[1:]

    @property
    def update_time(self) -> datetime:
        message_timestamp = self.messages[-1].timestamp
        if message_timestamp is None:
            raise ValueError("The timestamp of the last message is None.")
        return message_timestamp.astimezone().replace(tzinfo=UTC)
