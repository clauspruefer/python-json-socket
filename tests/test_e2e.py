"""Pytest end-to-end tests for basic client/server echo."""

import time
import pytest
import threading

import jsocket


class EchoServer(jsocket.JsonServer, threading.Thread):
    """Minimal echo server for tests."""
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        super().__init__(**kwargs)

    def _process_message(self, obj):
        print('Server rcv() obj:'.format(obj))
        if isinstance(obj, dict):
            return obj
        return {"Status": "NoObect"}

    def run(self):
        self.server_loop()


def test_client_server_send_receive():
    """Server accepts a connection and echoes payload (json object)."""

    server_address = '127.0.0.1'
    server_port = 64000

    server = EchoServer(address=server_address, port=server_port)
    server.start()

    client = jsocket.JsonClient(address=server_address, port=server_port)
    assert client.connect() is True

    # Send simple json dict
    payload = {"message": "new connection"}
    client.send_obj(payload)
    echoed = client.read_obj()
    assert echoed == payload

    time.sleep(1)

    # Echo round-trip
    payload = {"echo": "hello", "i": 1}
    client.send_obj(payload)
    echoed = client.read_obj()
    assert echoed == payload

    client.close()
    server.join()
