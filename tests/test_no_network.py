# Written by Claude Code on 2026-10-02: checks the scaffolding in conftest.py, not the lesson.
"""The network guard holds, for a plain lookup and for a real SDK call."""

import socket

import pytest
from openrouter import OpenRouter


def test_dns_lookup_is_refused():
    with pytest.raises(RuntimeError, match="must not touch the network"):
        socket.getaddrinfo("openrouter.ai", 443)


def test_sdk_call_is_refused():
    client = OpenRouter(api_key="not-a-key")
    with pytest.raises(RuntimeError, match="must not touch the network"):
        client.chat.send(model="openai/gpt-6-luna", messages=[{"role": "user", "content": "hi"}])
