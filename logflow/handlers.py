from logflow.base import NOTSET


class Handler:

    @classmethod
    def enabled(cls):
        try:
            return not cls._disabled
        except AttributeError:
            return True

    @classmethod
    def disable(cls):
        cls._disabled = True

    @classmethod
    def enable(cls):
        del cls._disabled

    def __init__(self, frmt='{level}:{logger}:{msg}', level=NOTSET):
        self.formatter = frmt
        self.level = level

    def __repr__(self):
        return "{self.__class__.__name__}(frmt='{self.formatter}', level={self.level})".format(self=self)

    def handle(self, record):
        if self.enabled() and self.level < record.level:
            self.emit(self.formatter.format_map(record.params()))

    def emit(self, message):
        raise NotImplementedError


class ConsoleHandler(Handler):

    terminator = '\n'

    def emit(self, message):
        print(message, end=self.terminator)


class FileHandler(Handler):

    terminator = '\n'

    def __init__(self, filename, mode='a', **kwargs):
        super().__init__(**kwargs)
        self.filename = filename
        self.mode = mode

    def emit(self, message):
        with open(self.filename, self.mode) as f:
            f.write(message + self.terminator)
