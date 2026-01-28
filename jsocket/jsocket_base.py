""" @namespace jsocket_base
    Contains JsonSocket, JsonServer and JsonClient implementations (json object message passing server and client).
"""
__author__   = "Christopher Piekarski"
__email__    = "chris@cpiekarski.com"
__copyright__= """
    Copyright (C) 2011 by
    Christopher Piekarski <chris@cpiekarski.com>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__version__  = "1.0.3"

import abc
import json
import socket
import logging

logger = logging.getLogger(__name__)


class JsonSocket:
    """Lightweight JSON-over-TCP socket wrapper."""

    def __init__(self, address='127.0.0.1', port=64000, timeout=0):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self._timeout = timeout
        self._address = address
        self._port = port
        self.socket.settimeout(self._timeout)
        self._shutdown_rcv = False

    def send_obj(self, obj):
        """Send a JSON-serializable object over the connection."""
        msg = json.dumps(obj, ensure_ascii=False)
        if self.socket:
            payload = '<message>{}</message>'.format(msg)
            self._send(payload)

    def _send(self, msg):
        """Send all bytes in `msg` over the connection."""
        msg = msg.encode()
        sent_bytes = 0
        while sent_bytes < len(msg):
            sent_bytes += self.conn.send(msg[sent_bytes:])

    def read_obj(self):
        """Recv until </message> end marker received."""
        buf = b''
        while True:
            tmp_buf = self.conn.recv(1024)
            # close on 0 bytes (close marker)
            if len(tmp_buf) == 0:
                self.close()
                self._shutdown_rcv = True
                break
            buf += tmp_buf
            if buf.find(b'<message>') == 0 and buf.find(b'</message>') == len(buf)-10:
                buf = buf.replace(b'<message>', b'')
                buf = buf.replace(b'</message>', b'')
                break
        return json.loads(buf)

    def close(self):
        """Close active connection and the listening socket if open."""
        try:
            self.socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            self.socket.close()
        except OSError:
            pass

    def _get_timeout(self):
        """Get the current socket timeout in seconds."""
        return self._timeout

    def _set_timeout(self, timeout):
        """Set the socket timeout in seconds and apply to the main socket."""
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        """Return the configured bind address."""
        return self._address

    def _get_port(self):
        """Return the configured bind port."""
        return self._port


class JsonServer(JsonSocket, metaclass=abc.ABCMeta):
    """Server socket that accepts one connection at a time."""

    def __init__(self, address='127.0.0.1', port=64000):
        super().__init__(address, port)
        self._bind()
        self._server_loop()

    def _server_loop(self):
        while self._shutdown_rcv = False:
            try:
                self.accept_connection()
            except TimeoutError:
                logger.debug("ServerLoop timeout exception.")
            try:
                self.send_obj(self._process_message(self.read_obj()))
            except Exception as e:
                logger.debug("Message processing exception:{}".format(e))

    @abc.abstractmethod
    def _process_message(self, obj):
        """Pure Virtual Method

        This method is called every time a JSON object is received from a client

        @param obj JSON "key: value" object received from client
        @retval None or a response object
        """
        # Return None in the base class to satisfy linters; subclasses should override.
        return None

    def _bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self._address, self._port))
        self.socket.listen(1)

    def _accept(self):
        return self.socket.accept()

    def accept_connection(self):
        """Accept a single client connection."""
        self.conn, addr = self._accept()
        logger.debug(
            "Connection accepted, conn socket (%s,%d)", addr[0], addr[1]
        )


class JsonClient(JsonSocket):
    """Client socket for connecting to a JsonServer and exchanging JSON messages."""

    def __init__(self, address='127.0.0.1', port=64000):
        super().__init__(address, port)

    def connect(self):
        """Connect to the server."""
        try:
            logger.debug("Connect to %s:%s", self._address, self._port)
            self.socket.connect((self._address, self._port))
            self.conn = self.socket
            logger.info("Socket connected...")
        except Exception as msg:
            logger.error("Socket connection error: %s", msg)
            return False
        return True
