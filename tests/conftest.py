# Written by Claude Code on 2026-10-02: test scaffolding, not the lesson.
"""Tests never touch the network: resolving a host or opening an IP socket raises NetworkBlocked."""

import socket

import pytest


class NetworkBlocked(RuntimeError):
    """A test tried to reach the network."""


_real_connect = socket.socket.connect


def _refuse(*args, **kwargs):
    raise NetworkBlocked("tests must not touch the network: script the model instead")


def _connect(sock, address):
    if sock.family in (socket.AF_INET, socket.AF_INET6):
        _refuse()
    return _real_connect(sock, address)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Refuse DNS lookups and IP connections for the duration of each test."""
    monkeypatch.setattr(socket, "getaddrinfo", _refuse)
    monkeypatch.setattr(socket.socket, "connect", _connect)
