import unittest
from nose import tools
from mock import MagicMock

from logflow.base import Logger, CRITICAL
from logflow.routing import Routes, Route, RoutesManager
from logflow.handlers import Handler


class TestFilters(unittest.TestCase):

    def setUp(self):
        self.dispatcher = RoutesManager()
        self.mock_handler = Handler()
        self.mock_handler.emit = MagicMock()

    def get_logger(self, name):
        logger = Logger(name)
        logger._dispatcher = self.dispatcher
        return logger

    def test_same_name_filters(self):
        """Tests filters stop records with exact same name."""
        self.dispatcher.routes.add(
            Route('test', self.mock_handler),
        )
        self.dispatcher.add_filter('test', CRITICAL)

        logger = self.get_logger('test')
        logger.info('message body')
        tools.assert_equal(self.mock_handler.emit.call_count, 0)

    def test_base_name_filters(self):
        """Tests filter stops record with a derived name."""
        self.dispatcher.routes.add(
            Route('test', self.mock_handler),
        )
        self.dispatcher.add_filter('test', CRITICAL)

        logger = self.get_logger('test.out')
        logger.info('message body')
        tools.assert_equal(self.mock_handler.emit.call_count, 0)

    def test_derived_name_passes_filter(self):
        """Tests filter let pass record with a more basic name."""
        self.dispatcher.routes.add(
            Route('test', self.mock_handler),
        )
        self.dispatcher.add_filter('test.out', CRITICAL)

        logger = self.get_logger('test')
        logger.info('message body')
        tools.assert_equal(self.mock_handler.emit.call_count, 1)


class TestBlockers(unittest.TestCase):

    def setUp(self):
        self.dispatcher = RoutesManager()
        self.mock_handler = Handler()
        self.mock_handler.emit = MagicMock()

    def get_logger(self, name):
        logger = Logger(name)
        logger._dispatcher = self.dispatcher
        return logger

    def test_direct_block_record(self):
        """Tests that an aimed block blocks."""
        self.dispatcher.routes.add(
            Route('test', self.mock_handler),
        )
        self.dispatcher.routes.add_block('test', Handler)

        logger = self.get_logger('test')
        logger.info('message body')
        tools.assert_equal(self.mock_handler.emit.call_count, 0)
