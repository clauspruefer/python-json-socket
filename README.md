python-json-socket (jsocket)
============================

[![CI](https://github.com/clauspruefer/python-json-socket/actions/workflows/ci.yml/badge.svg)](https://github.com/clauspruefer/python-json-socket/actions/workflows/ci.yml)
![PyPI](https://img.shields.io/pypi/v/jsocket.svg)
![Python Versions](https://img.shields.io/pypi/pyversions/jsocket.svg)

Simple JSON-over-TCP sockets for Python. This library provides:

- JsonClient / JsonServer: encapsulated JSON message framing over TCP
- Non-Blocking Socket IO
- 1:1 Client / Server Connection (no Mult-Client support)

It aims to be small, predictable, and easy to integrate in tests or small services.


Install
-------

```
pip install jsocket
```

Requires Python 3.8+.


Quickstart
----------

Echo server with `JsonServer`:

```python
class JSONServer(jsocket.JsonServer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _process_message(self, call_obj):
        if isinstance(call_obj, dict):
            print('Server recv():{}'.format(call_obj))
            return call_obj
        return { "Status": "Wrong object type received" }

server = JSONServer(
  address='127.0.0.1'
).server_loop()
```

Client part:

```python
client_ref = jsocket.JsonClient(
  address='127.0.0.1'
)
assert client_ref.connect() is True

client_ref.send_obj({"Echo": "Hello World!"})
res = client_ref.read_obj()

print('Client recv() from server:{}'.format(res))
```


API Highlights
--------------

- JsonClient:
  - `connect()` returns True on success
  - `send_obj(dict)` sends a JSON object
  - `read_obj()` blocks until a full message is received

Examples and Tests
------------------

- Examples: see `examples/example_servers.py`
- Pytest: end-to-end and listener tests under `tests/`
  - Run: `pytest -q`

Notes
-----

- Binding with `port=0` lets the OS choose an ephemeral port; find it with `server.socket.getsockname()`.

Links
-----

- PyPI: https://pypi.org/project/jsocket/
- License: see `LICENSE`
