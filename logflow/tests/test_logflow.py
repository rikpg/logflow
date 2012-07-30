import unittest
from nose import tools
from mock import MagicMock, call

import logflow
from logflow.handlers import Handler


class logflowTest(unittest.TestCase):
    """Kind-of integrational tests."""

    def setUp(self):
        self.mock_handler = Handler()
        self.mock_handler.emit = MagicMock()
        logflow._dispatcher.reset()

    def test_default_behaviour(self):
        """Tests a message is emitted with default settings."""
        logflow.routes.add(
            logflow.Route('test', self.mock_handler),
        )

        logger = logflow.get_logger('test')
        logger.info('foo msg')
        self.mock_handler.emit.assert_called_once_with('INFO:test:foo msg')

    def test_block(self):
        """Tests block context manager."""
        logflow.routes.add(
            logflow.Route('test', self.mock_handler),
        )

        logger = logflow.get_logger('test')
        with logflow.block('test', self.mock_handler.__class__):
            logger.info('foo msg')

        tools.assert_equal(self.mock_handler.emit.call_count, 0)

    def test_barriage(self):
        """Tests barriage context manager."""
        logflow.routes.add(
            logflow.Route('test', self.mock_handler),
        )

        logger = logflow.get_logger('test')
        with logflow.barriage('test'):
            logger.info('foo msg')

        tools.assert_equal(self.mock_handler.emit.call_count, 0)

    def test_shut(self):
        """Tests shut context manager."""
        logflow.routes.add(
            logflow.Route('test', self.mock_handler),
        )

        logger = logflow.get_logger('test')
        with logflow.shut(self.mock_handler.__class__):
            logger.info('foo msg')

        tools.assert_equal(self.mock_handler.emit.call_count, 0)
