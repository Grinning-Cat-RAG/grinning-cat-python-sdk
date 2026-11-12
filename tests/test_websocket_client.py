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
