import jsocket
import logging
import threading

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
FORMAT = '[%(asctime)-15s][%(levelname)s][%(module)s][%(funcName)s] %(message)s'
logging.basicConfig(format=FORMAT)


class MyServer(jsocket.JsonServer):
    """This is a basic example of a NonThreadedServer."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _process_message(self, obj):
        print('Server rcv() obj:'.format(obj))
        if isinstance(obj, dict):
            return obj
        return {"Status": "NoObect"}


class MyThreadedServer(jsocket.JsonServer, threading.Thread):
    """This is a basic example of a ThreadedServer."""
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


if __name__ == "__main__":

    # Start a threaded server (in parallel)
    server1 = MyThreadedServer(address='127.0.0.1', port=5491)
    server1.start()

    # Run a second server inside this process (needs ctrl-c twice to abort)
    server2 = MyServer(address='127.0.0.1', port=5492).server_loop()
