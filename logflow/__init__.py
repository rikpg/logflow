from logflow.base import CRITICAL, ERROR, WARNING, NOTICE, INFO, DEBUG, NOTSET
from logflow.routing import RoutesManager, Route

__version__ = '0.1'


_dispatcher = RoutesManager()
routes = _dispatcher.routes


def get_logger(name):
    from logflow.base import Logger
    logger = Logger(name)
    logger._dispatcher = _dispatcher
    return logger


class block:

    def __init__(self, start, target_class):
        self.start = start
        self.target_class = target_class

    def __enter__(self):
        self.block_id = routes.add_block(self.start, self.target_class)

    def __exit__(self, exc_type, exc_val, exc_tb):
        routes.rm_block(self.block_id)


class barriage:

    def __init__(self, start, level=CRITICAL):
        self.start = start
        self.level = level

    def __enter__(self):
        _dispatcher.add_filter(self.start, self.level)

    def __exit__(self, exc_type, exc_val, exc_tb):
        _dispatcher.rm_filter(self.start)


class shut:

    def __init__(self, handler_class):
        self.handler_class = handler_class

    def __enter__(self):
        if self.handler_class.enabled():
            self.handler_class.disable()
            self._was_enabled = True
        else:
            self._was_enabled = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._was_enabled:
            self.handler_class.enable()
