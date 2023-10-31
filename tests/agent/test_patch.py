from unittest import TestCase

from agent_guy.agent import IPatch


class TestPatch(TestCase):
    def test_init(self):
        class MyPatch(IPatch):
            pass

        patch = MyPatch(x=1, y=2)
        self.assertEqual(patch.x, 1)
        self.assertEqual(patch.y, 2)
