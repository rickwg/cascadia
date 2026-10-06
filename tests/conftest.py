import socket

import pytest

INTERNET_ADDRESS_FAMILIES = (socket.AF_INET, socket.AF_INET6)
unguarded_connect = socket.socket.connect


class NetworkAccessBlocked(RuntimeError):
    pass


def refuse_network_access(*args, **kwargs):
    raise NetworkAccessBlocked(
        "tests must not touch the network: script the model instead"
    )


def connect_unless_internet(sock, address):
    if sock.family in INTERNET_ADDRESS_FAMILIES:
        refuse_network_access()
    return unguarded_connect(sock, address)


@pytest.fixture(autouse=True)
def block_network_access(monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", refuse_network_access)
    monkeypatch.setattr(socket.socket, "connect", connect_unless_internet)
