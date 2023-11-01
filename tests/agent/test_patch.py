from unittest import TestCase

from agent_guy.agent import IPatch

from tests.mocks.mocks import MyPatch, MyTurtle


class TestPatch(TestCase):
    def test_init(self):
        patch = MyPatch(x=1, y=2)
        self.assertEqual(patch.x, 1)
        self.assertEqual(patch.y, 2)

        # get agent id
        self.assertEqual(patch.agent_id, patch._build_id())

    def test_get_turtle_on_patch(self):
        patch = MyPatch(x=1, y=2)
        self.assertEqual(patch.get_turtles(), [])

        # put a turtle on the patch
        turtle = MyTurtle()
        patch.add_turtle(turtle)

        # second turtle
        turtle_2 = MyTurtle()
        patch.add_turtle(turtle_2)

        self.assertEqual(patch.get_turtles(), [turtle, turtle_2])

        # get turtle by id
        self.assertEqual(patch.get_turtles([turtle.agent_id]), [turtle])

        # check for value error
        with self.assertRaises(ValueError):
            patch.get_turtles(["some_id"])
