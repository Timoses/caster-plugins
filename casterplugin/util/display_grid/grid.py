from functools import wraps
from multiprocessing import Process

from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer

from time import sleep


def grid_proxy(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        attempts = 0
        success = False
        while not success and attempts < 50:
            try:
                function(*args, **kwargs)
                success = True
            except ConnectionRefusedError:
                attempts += 1
                sleep(0.1)

        if not success:
            raise ConnectionRefusedError()

    return wrapper


class Grid():

    """Display grid to determine position on screen

    The visual representation of the grid runs in a
    separate child process.

    """

    def __init__(self, id=None):
        """TODO: to be defined. """
        # ID of the grid
        self._id = id

        self._grid_process = None
        self._grid_proxy = None

    def initialize(self):
        """Initialize grid"""

        self._grid_process = Process(target=grid_initialize,
                                     args=(self._draw, self._show, self._hide),
                                     daemon=True)
        self._grid_process.start()

        self._grid_proxy = ServerProxy('http://127.0.0.1:8080')

    @grid_proxy
    def draw(self):
        """Draw grid on screen

        Runs in separate process
        """
        self._grid_proxy._draw()

    @grid_proxy
    def show(self):
        """Show Grid as visible
        """
        self._grid_proxy._show()

    @grid_proxy
    def hide(self):
        """Hide Grid as invisble
        """
        self._grid_proxy._hide()

    @staticmethod
    def _draw():
        print("Please implement me in child class")
        NotImplementedError("Please implement me in child class")

    @staticmethod
    def _show():
        print("Please implement me in child class")
        NotImplementedError("Please implement me in child class")

    @staticmethod
    def _hide():
        print("Please implement me in child class")
        NotImplementedError("Please implement me in child class")

    def get_position(self, **kwargs):
        """Get position on screen based on parameters

        :**kwargs: Parameters for the grid schema to determine position on
                   screen
        :returns: Screen position

        """
        pass


def grid_initialize(*callbacks):
    # TODO: initialize
    server = SimpleXMLRPCServer(('127.0.0.1', 8080), allow_none=True,
                                logRequests=False)
    for cb in callbacks:
        server.register_function(cb)
    server.serve_forever()


class RainbowGrid(Grid):

    @staticmethod
    def _draw():
        """ Should draw the grid on screen """
        print('rb_draw')

    def get_position(color_sequence, color, number):
        pass


if __name__ == "__main__":
    g = RainbowGrid()
    g.initialize()
    g.draw()
    g.show()
    g.hide()
