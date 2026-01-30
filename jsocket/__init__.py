""" @package jsocket
    @brief Main package importing one module jsocket_base into the scope of jsocket.

    @example example_servers.py

    @mainpage JSocket - Fast & Scalable JSON Server & Client 
    @section Installation

    The jsocket package should always be installed using the stable PyPi releases.
    Either use "easy_install jsocket" or "pip install jsocket" to get the latest stable version.

    @section Usage

    The jsocket package can be useful during the development of distributed systems, for management channel
    communication or similar. The first and simplest is to create a custom server by overloading the
    jsocket.ThreadedServer class (see example one below).

    @section Examples
    @b 1: The following snippet simply creates a custom server by overloading jsocket.JsonServer
    @code
    class MyServer(jsocket.ThreadedServer):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def _process_message(self, call_obj):
            if isinstance(call_obj, dict):
                print(call_obj)
                return call_obj
            return { "Status": "Object type not dict" }
    @endcode

"""
from jsocket.jsocket_base import *
