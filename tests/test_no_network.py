import socket

import pytest
from openrouter import OpenRouter


def test_dns_lookup_is_refused():
    with pytest.raises(RuntimeError, match="must not touch the network"):
        socket.getaddrinfo("openrouter.ai", 443)


def test_sdk_chat_call_is_refused():
    client = OpenRouter(api_key="not-a-key")
    with pytest.raises(RuntimeError, match="must not touch the network"):
        client.chat.send(
            model="apodex/apodex-1.1-mini:free",
            messages=[{"role": "user", "content": "hi"}],
        )
