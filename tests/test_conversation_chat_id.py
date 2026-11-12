from unittest.mock import MagicMock

from grinning_cat_python_sdk.endpoints.conversation import ConversationEndpoint


class FakeClient:
    def __init__(self):
        self.http_client = MagicMock()


def make_endpoint(payload):
    client = FakeClient()
    endpoint = ConversationEndpoint(client)

    response = MagicMock()
    response.json.return_value = payload
    response.raise_for_status.return_value = None

    session = MagicMock()
    session.get.return_value = response
    session.delete.return_value = response
    session.put.return_value = response

    spy = MagicMock(return_value=session)
    endpoint.get_http_client = spy
    return endpoint, spy


def test_get_conversation_history_propagates_chat_id():
    endpoint, spy = make_endpoint({"history": []})

    endpoint.get_conversation_history("a", "u", "c1")

    spy.assert_called_once_with("a", "u", "c1")


def test_get_conversation_propagates_chat_id():
    endpoint, spy = make_endpoint(
        {
            "chat_id": "c1",
            "name": "n",
            "num_messages": 0,
            "metadata": {},
            "created_at": None,
            "updated_at": None,
        }
    )

    endpoint.get_conversation("a", "u", "c1")

    spy.assert_called_once_with("a", "u", "c1")


def test_delete_conversation_propagates_chat_id():
    endpoint, spy = make_endpoint({"deleted": True})

    endpoint.delete_conversation("a", "u", "c1")

    spy.assert_called_once_with("a", "u", "c1")


def test_put_conversation_attributes_propagates_chat_id():
    endpoint, spy = make_endpoint({"changed": True})

    endpoint.put_conversation_attributes("a", "u", "c1", name="new")

    spy.assert_called_once_with("a", "u", "c1")
