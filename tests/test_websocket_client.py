import asyncio
from unittest.mock import AsyncMock, patch

from grinning_cat_python_sdk.clients.websocket_client import WSClient


def test_get_client_passes_configured_max_size():
    client = WSClient(host="localhost", port=1865, apikey="key", max_size=12345)
    connect = AsyncMock(return_value=object())

    with patch("grinning_cat_python_sdk.clients.websocket_client.connect", new=connect):
        asyncio.run(client.get_client("agent", "user", "chat"))

    assert connect.call_args.kwargs["max_size"] == 12345


def test_default_max_size_is_large_enough_for_images():
    client = WSClient(host="localhost", port=1865, apikey="key")

    assert client.max_size == 256 * 1024 * 1024


def test_configuration_max_size_reaches_ws_client():
    from grinning_cat_python_sdk import Configuration, GrinningCatClient

    client = GrinningCatClient(Configuration(auth_key="k", ws_max_size=777))

    assert client.ws_client.max_size == 777


def test_configuration_max_size_none_disables_limit():
    from grinning_cat_python_sdk import Configuration, GrinningCatClient

    client = GrinningCatClient(Configuration(auth_key="k", ws_max_size=None))

    assert client.ws_client.max_size is None


def _connect_with(client, **kwargs):
    connect = AsyncMock(return_value=object())
    with patch("grinning_cat_python_sdk.clients.websocket_client.connect", new=connect):
        asyncio.run(client.get_client("agent", "user", "chat"))
    return connect


def test_token_takes_precedence_over_apikey_in_ws_headers():
    client = WSClient(host="localhost", port=1865, apikey="key")
    client.set_token("tok")

    connect = _connect_with(client)

    assert connect.call_args.kwargs["additional_headers"] == {"Authorization": "Bearer tok"}


def test_ws_get_client_without_credentials_fails():
    import pytest

    client = WSClient(host="localhost", port=1865)

    with pytest.raises(ValueError, match="apikey or a token"):
        asyncio.run(client.get_client("agent", "user"))


def test_ws_get_client_reuses_open_connection():
    client = WSClient(host="localhost", port=1865, apikey="key")
    connect = AsyncMock(return_value=object())

    async def twice():
        first = await client.get_client("agent", "user")
        return first, await client.get_client("agent", "user")

    with patch("grinning_cat_python_sdk.clients.websocket_client.connect", new=connect):
        first, second = asyncio.run(twice())

    assert first is second
    assert connect.await_count == 1


def test_ws_invalid_uri_is_reported_as_value_error():
    import pytest
    from websockets.exceptions import InvalidURI

    client = WSClient(host="localhost", port=1865, apikey="key")
    connect = AsyncMock(side_effect=InvalidURI("x", "bad"))

    with patch("grinning_cat_python_sdk.clients.websocket_client.connect", new=connect):
        with pytest.raises(ValueError, match="Invalid WebSocket URI"):
            asyncio.run(client.get_client("agent", "user"))
