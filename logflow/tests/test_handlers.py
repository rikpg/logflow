import unittest
from nose import tools

from logflow.handlers import Handler


class TestHandlers(unittest.TestCase):

    def test_disabling_parent_handler(self):
        """Tests disabling propagate to child handlers."""
        class A(Handler):
            pass

        class B(A):
            pass

        A.disable()

        result = [A.enabled(), B.enabled()]
        tools.assert_equal([False, False], result)

    def test_disabling_child_handler(self):
        """Tests disabling child handler doesn't affect parent."""
        class A(Handler):
            pass

        class B(A):
            pass

        B.disable()
        result = [A.enabled(), B.enabled()]
        tools.assert_equal([True, False], result)

    def test_disabling_sibiling_handler(self):
        """Tests disabling doesn't affect sibiling handlers."""
        class A(Handler):
            pass

        class Z(Handler):
            pass

        A.disable()
        result = [A.enabled(), Z.enabled()]
        tools.assert_equal([False, True], result)
