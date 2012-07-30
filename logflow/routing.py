from logflow.base import NOTSET

from collections import defaultdict
from itertools import count


class Route:

    def __init__(self, start, target):
        self.start = start
        self.target = target
        self.blocked = 0

    def __repr__(self):
        return "Route({self.start!r}, {self.target})".format(self=self)


class Routes:

    def __init__(self):
        self.dct = defaultdict(list)
        self._counter = count()
        self._block_register = defaultdict(list)

    def __iter__(self):
        for route_lst in self.dct.values():
            for route in route_lst:
                yield route

    def __contains__(self, item):
        return item in self.dct

    def add(self, *args):
        for r in args:
            self.dct[r.start].append(r)

    def get(self, start, default=None):
        return self.dct.get(start, default)

    def add_block(self, start, target_class):
        block_id = next(self._counter)
        for route in self.dct[start]:
            if issubclass(route.target.__class__, target_class):
                route.blocked += 1
                self._block_register[block_id].append(route)
        return block_id

    def rm_block(self, block_id):
        for route in self._block_register.pop(block_id):
            route.blocked -= 1

    def clear(self):
        self.dct.clear()
        self._counter = count()
        self._block_register.clear()


class RoutesManager:

    def __init__(self):
        self.routes = Routes()
        self.filters = {}

    def send(self, record):
        for filter_start, filter_level in self.filters.items():
            if (record.logger.startswith(filter_start)
                and record.level < filter_level):
                return

        for route in self.routes:
            if record.logger.startswith(route.start) and not route.blocked:
                route.target.handle(record)

    def add_filter(self, start, level):
        self.filters[start] = level

    def rm_filter(self, start):
        self.filters.pop(start)

    def reset(self):
        self.routes.clear()
        self.filters.clear()
