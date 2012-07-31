import unittest
from nose import tools
from mock import MagicMock, call

import logflow
from logflow.handlers import Handler


class LogflowTest(unittest.TestCase):
    """Kind-of integrational tests."""

    def setUp(self):
        self.mock_handler = Handler()
        self.mock_handler.emit = MagicMock()
        logflow._dispatcher.reset()
        logflow.routes.add(
            logflow.Route('test', self.mock_handler),
        )
        self.logger = logflow.get_logger('test')

    def test_default_behaviour(self):
        """Tests a message is emitted with default settings."""
        self.logger.info('foo msg')
        self.mock_handler.emit.assert_called_once_with('INFO:test:foo msg')

    def test_get_logger_with_no_route_raise_exception(self):
        """Tests get_logger with no matching route raise an exception."""
        tools.assert_raises(AttributeError, logflow.get_logger, 'test.foo')

    def test_fields_log_formatting(self):
        """Tests extra fields are properly formatted."""
        self.mock_handler.formatter = '{msg}::{foobaz}'
        self.logger.info('foo msg', foobaz='extra param')
        self.mock_handler.emit.assert_called_once_with('foo msg::extra param')

    def test_block_cm(self):
        """Tests block context manager."""
        with logflow.block('test', self.mock_handler.__class__):
            self.logger.info('foo msg')
        tools.assert_equal(self.mock_handler.emit.call_count, 0)

    def test_barriage_cm(self):
        """Tests barriage context manager."""
        with logflow.barriage('test'):
            self.logger.info('foo msg')
        tools.assert_equal(self.mock_handler.emit.call_count, 0)

    def test_shut_cm(self):
        """Tests shut context manager."""
        with logflow.shut(self.mock_handler.__class__):
            self.logger.info('foo msg')
        tools.assert_equal(self.mock_handler.emit.call_count, 0)
