from typing import List, Dict

from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint
from grinning_cat_python_sdk.models.api.conversations import (
    ConversationHistoryOutput,
    ConversationDeleteOutput,
    ConversationsResponse,
    ConversationAttributesChangeOutput,
)
from grinning_cat_python_sdk.utils import deserialize


class ConversationEndpoint(AbstractEndpoint):
    def __init__(self, client: "GrinningCatClient"):
        super().__init__(client)
        self.prefix = "/conversations"

    def get_conversation_history(self, agent_id: str, user_id: str, chat_id: str) -> ConversationHistoryOutput:
        """
        This endpoint returns the conversation history.
        :param agent_id: The agent ID.
        :param user_id: The user ID to filter the conversation history.
        :param chat_id: The chat ID to filter the conversation history.
        :return: ConversationHistoryOutput, a list of conversation history entries.
        """
        return self.get(
            self.format_url(f"{chat_id}/history"),
            agent_id,
            user_id=user_id,
            chat_id=chat_id,
            output_class=ConversationHistoryOutput,
        )

    def get_conversations(self, agent_id: str, user_id: str) -> List[ConversationsResponse]:
        """
        This endpoint returns the attributes of the different conversations, given the `agent_id` and the `user_id`.
        :param agent_id: The agent ID.
        :param user_id: The user ID to filter the conversation history.
        :return: List[ConversationsResponse], a list of conversation attributes.
        """
        response = self.get_http_client(agent_id, user_id).get(self.prefix)
        response.raise_for_status()

        return [deserialize(item, ConversationsResponse) for item in response.json()]

    def get_conversation(self, agent_id: str, user_id: str, chat_id: str) -> ConversationsResponse:
        """
        This endpoint returns the attributes of a specific conversation, given the `agent_id`, the `user_id` and the
        `chat_id`.
        :param agent_id: The agent ID.
        :param user_id: The user ID to filter the conversation history.
        :param chat_id: The chat ID to filter the conversation history.
        :return: ConversationsResponse, the conversation attributes.
        """
        return self.get(
            self.format_url(chat_id),
            agent_id,
            user_id=user_id,
            chat_id=chat_id,
            output_class=ConversationsResponse,
        )

    def delete_conversation(self, agent_id: str, user_id: str, chat_id: str) -> ConversationDeleteOutput:
        """
        This endpoint deletes the conversation.
        :param agent_id: The agent ID.
        :param user_id: The user ID to filter the conversation history.
        :param chat_id: The chat ID to filter the conversation history.
        :return: ConversationDeleteOutput, a message indicating whether the conversation was deleted.
        """
        return self.delete(
            self.format_url(chat_id),
            agent_id,
            output_class=ConversationDeleteOutput,
            user_id=user_id,
            chat_id=chat_id,
        )

    def put_conversation_attributes(
        self,
        agent_id: str,
        user_id: str,
        chat_id: str,
        name: str | None,
        metadata: Dict | None = None,
    ) -> ConversationAttributesChangeOutput:
        """
        This endpoint creates a new element in the conversation history.
        :param agent_id: The agent ID.
        :param user_id: The user ID to filter the conversation history.
        :param chat_id: The chat ID to filter the conversation history.
        :param name: The new name to assign to the conversation
        :param metadata: The metadata to assign to the conversation
        :return: ConversationNameChangeOutput, a message indicating whether the conversation name was changed.
        """
        if not name and not metadata:
            raise ValueError("Either name or metadata must be provided")

        payload = {}
        if name:
            payload = {"name": name}
        if metadata:
            payload["metadata"] = metadata

        return self.put(
            self.format_url(chat_id),
            agent_id,
            output_class=ConversationAttributesChangeOutput,
            payload=payload,
            user_id=user_id,
            chat_id=chat_id,
        )
