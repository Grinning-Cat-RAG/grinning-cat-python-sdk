import pytest

from grinning_cat_python_sdk.clients.http_client import HttpClient


def make_client(apikey: str = "key") -> HttpClient:
    return HttpClient(host="localhost", port=1865, apikey=apikey)


def test_chat_id_does_not_leak_into_next_request():
    client = make_client()

    first = client.get_client(chat_id="c1")
    assert first.headers["X-Chat-ID"] == "c1"

    second = client.get_client(chat_id=None)
    assert "X-Chat-ID" not in second.headers
    assert second.headers["Authorization"] == "Bearer key"


def test_agent_and_user_headers_are_per_request():
    client = make_client()

    session = client.get_client(agent_id="a", user_id="u")
    assert session.headers["X-Agent-ID"] == "a"
    assert session.headers["X-User-ID"] == "u"
    assert "X-Chat-ID" not in session.headers


def test_base_session_keeps_authorization():
    client = make_client()

    session = client.get_base_session()
    assert session.headers["Authorization"] == "Bearer key"


def test_token_takes_precedence_over_apikey():
    client = make_client()
    client.set_token("tok")

    assert client.get_base_session().headers["Authorization"] == "Bearer tok"


def test_get_client_requires_credentials():
    client = HttpClient(host="localhost", port=1865)

    with pytest.raises(ValueError):
        client.get_client()


def test_user_id_is_sent_with_token_only_auth():
    client = HttpClient(host="localhost", port=1865)
    client.set_token("tok")

    session = client.get_client(agent_id="a", user_id="u", chat_id="c")
    assert session.headers["Authorization"] == "Bearer tok"
    assert session.headers["X-User-ID"] == "u"
    assert session.headers["X-Agent-ID"] == "a"
    assert session.headers["X-Chat-ID"] == "c"
