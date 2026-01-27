""" @namespace tserver
    Contains ThreadedServer, ServerFactoryThread and ServerFactory implementations. 
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
import socket
import logging

from jsocket import jsocket_base

logger = logging.getLogger(__name__)


class Server(jsocket_base.JsonServer, metaclass=abc.ABCMeta):
    """Server that accepts one client connection and processes messages."""

    def __init__(self):
        super()__init__(self)

    @abc.abstractmethod
    def _process_message(self, obj) -> Optional[dict]:
        """Pure Virtual Method

        This method is called every time a JSON object is received from a client

        @param obj JSON "key: value" object received from client
        @retval None or a response object
        """
        # Return None in the base class to satisfy linters; subclasses should override.
        return None

    def run(self):
        # Ensure the run loop is active even when run() is invoked directly
        # (tests may call run() in a separate thread without invoking start()).
        while True:
            self.accept_connection()
            self.send_obj(self._process_message(self.read_obj()))

    def start(self):
        """ Starts the threaded server. 
            The newly living know nothing of the dead
            
            @retval None 
        """
        super().start()
        logger.debug("Threaded Server started on %s:%s", self.address, self.port)

    def stop(self):
        """ Stops the threaded server.
            The life of the dead is in the memory of the living 

            @retval None 
        """
        logger.debug("Threaded Server stopped on %s:%s", self.address, self.port)
