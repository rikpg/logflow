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

    def __init__(self, level, msg, logger, fields=None):
        self.level = level
        self.msg = msg
        self.logger = logger
        self.fields = fields or {}
        self.datetime = datetime.datetime.now()

    def params(self):
        pms = {
            'level': self.level,
            'msg': self.msg,
            'logger': self.logger,
            'datetime': self.datetime,
        }
        pms.update(self.fields)
        return pms


class Logger:

    def __init__(self, name, level=NOTSET):
        self.name = name
        self._dispatcher = None

    def log(self, lvl, msg, **kwargs):
        record = Record(level=lvl, msg=msg, logger=self.name, fields=kwargs)
        self._dispatcher.send(record)

    def error(self, msg, **kwargs):
        return self.log(ERROR, msg, **kwargs)

    def critical(self, msg, **kwargs):
        return self.log(CRITICAL, msg, **kwargs)

    def warning(self, msg, **kwargs):
        return self.log(WARNING, msg, **kwargs)

    def notice(self, msg, **kwargs):
        return self.log(NOTICE, msg, **kwargs)

    def info(self, msg, **kwargs):
        return self.log(INFO, msg, **kwargs)

    def debug(self, msg, **kwargs):
        return self.log(DEBUG, msg, **kwargs)
