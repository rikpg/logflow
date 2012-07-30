import datetime


class Level:

    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Level({self.value}, '{self.name}')".format(self=self)

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value


CRITICAL = Level(6, 'CRITICAL')
ERROR = Level(5, 'ERROR')
WARNING = Level(4, 'WARNING')
NOTICE = Level(3, 'NOTICE')
INFO = Level(2, 'INFO')
DEBUG = Level(1, 'DEBUG')
NOTSET = Level(0, 'NOTSET')


class Record:

    def __init__(self, level, msg, logger):
        self.level = level
        self.msg = msg
        self.logger = logger
        self.datetime = datetime.datetime.now()


class Logger:

    def __init__(self, name, level=NOTSET):
        self.name = name
        self._dispatcher = None

    def log(self, lvl, msg):
        record = Record(level=lvl, msg=msg, logger=self.name)
        self._dispatcher.send(record)

    def error(self, msg):
        return self.log(ERROR, msg)

    def critical(self, msg):
        return self.log(CRITICAL, msg)

    def warning(self, msg):
        return self.log(WARNING, msg)

    def notice(self, msg):
        return self.log(NOTICE, msg)

    def info(self, msg):
        return self.log(INFO, msg)

    def debug(self, msg):
        return self.log(DEBUG, msg)
