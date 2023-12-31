from unittest import TestCase

from agent_guy.agent import Patch, Turtle
from agent_guy.model import IModel
from agent_guy.world import Grid


class TestModel(TestCase):
    def test_init_with_basic_grid(self) -> None:
        class MyModel(IModel):
            def setup_grid(self) -> None:
                pass

            def setup_agents(self) -> None:
                pass

            def step(self) -> None:
                pass

        model = MyModel(grid=Grid(width=10, height=10))

        # check if all patches are built
        self.assertEqual(len(model.grid.patches), 100)

    def test_setup_agents(self) -> None:
        class MyModel(IModel):
            def setup_grid(self) -> None:
                pass

            def setup_agents(self) -> None:
                # create a turtle
                turtle = Turtle()
                turtle2 = Turtle()

                # add turtle to grid
                self.add_turtle_to_grid(turtle, patch_id=Patch.build_id_contract(0, 0))

                # add turtle2 to grid
                self.add_turtle_to_grid(turtle2, patch_id=Patch.build_id_contract(0, 0))

                self.remove_turtle_from_grid(turtle2)

            def step(self) -> None:
                pass

        model = MyModel(grid=Grid(width=3, height=3))
        model.setup_agents()

        # check if turtle is in grid
        self.assertEqual(len(model.turtles), 1)
        # turtle must be on the first patch of the grid (0, 0)
        self.assertEqual(
            list(model.turtles.values())[0].patch_id,
            Patch.build_id_contract(0, 0),
        )

        # check that turtle2 is not on grid
        self.assertEqual(len(model.turtles), 1)

        self.assertIsNone(model.turtles.get("turtle2", None))
