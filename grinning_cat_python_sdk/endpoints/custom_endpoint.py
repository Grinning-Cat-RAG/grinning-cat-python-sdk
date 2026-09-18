from typing import Any, Dict

from grinning_cat_python_sdk.endpoints.base import AbstractEndpoint


class CustomEndpoint(AbstractEndpoint):
    def get_custom(
        self, url: str, agent_id: str, user_id: str | None = None, query: Dict[str, Any] | None = None
    ) -> Any:
        """
        This method is used to trigger a custom endpoint with GET method
        :param url: The url of the custom endpoint to trigger
        :param agent_id: The id of the agent to get settings for (optional)
        :param user_id: The id of the user to get settings for (optional)
        :param query: The query parameters to send to the custom endpoint (optional)
        :return Any, the response from the custom endpoint
        """
        return self.get(url, agent_id, user_id=user_id, query=query)

    def get_global_message(self) -> Any:
        """
        Read the ``mgmt_message`` plugin's global banner via its public,
        unauthenticated endpoint.

        Returns the 4-field settings dict stored by the plugin:
        ``{"management_message": str, "management_active": bool,
        "global_message": str, "show_global_msg": bool}``.

        Uses the base (unauthenticated) HTTP session: the endpoint is public by
        design, so no auth key or token is required (or useful).
        """
        response = self.get_http_session().get("/mgmt_message/global_message")
        response.raise_for_status()
        return response.json()

    def post_custom(
        self, url: str, agent_id: str, payload: Dict[str, Any] | None = None, user_id: str | None = None
    ) -> Any:
        """
        This method is used to trigger a custom endpoint with POST method
        :param url: The url of the custom endpoint to trigger
        :param agent_id: The id of the agent to get settings for (optional)
        :param payload: The payload to send to the custom endpoint (optional)
        :param user_id: The id of the user to get settings for (optional)
        :return Any, the response from the custom endpoint
        """
        return self.post_json(url, agent_id, payload=payload, user_id=user_id)

    def put_custom(
        self, url: str, agent_id: str, payload: Dict[str, Any] | None = None, user_id: str | None = None
    ) -> Any:
        """
        The method is used to trigger a custom endpoint with PUT method
        :param url: The url of the custom endpoint to trigger
        :param agent_id: The id of the agent to get settings for (optional)
        :param payload: The payload to send to the custom endpoint (optional)
        :param user_id: The id of the user to get settings for (optional)
        :return Any, the response from the custom endpoint
        """
        return self.put(url, agent_id, payload=payload, user_id=user_id)

    def delete_custom(
        self, url: str, agent_id: str, payload: Dict[str, Any] | None = None, user_id: str | None = None
    ) -> Any:
        """
        This method is used to trigger a custom endpoint with DELETE method
        :param url: The url of the custom endpoint to trigger
        :param agent_id: The id of the agent to get settings for (optional)
        :param payload: The payload to send to the custom endpoint (optional)
        :param user_id: The id of the user to get settings for (optional)
        :return Any, the response from the custom endpoint
        """
        return self.delete(url, agent_id, payload=payload, user_id=user_id)
