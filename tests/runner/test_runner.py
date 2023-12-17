from typing import Any

import unittest

from agent_guy import Grid, IModel, Patch, Runner, SequentialExecutor, Turtle
from tests.mocks.game_of_life import LifeCell


class TestRunner(unittest.TestCase):
    def setUp(self) -> None:
        class TestModel(IModel):
            def setup_grid(self) -> None:
                pass

            def setup_agents(self) -> None:
                # place three agents on the grid besides each other
                # patch 1
                t1 = LifeCell()
                self.add_turtle_to_grid(
                    turtle=t1,
                    patch_id=Patch.build_id_contract(0, 0),
                )

                # patch 2
                t2 = LifeCell()
                self.add_turtle_to_grid(
                    turtle=t2,
                    patch_id=Patch.build_id_contract(1, 0),
                )

                # patch 3
                t3 = LifeCell()
                self.add_turtle_to_grid(
                    turtle=t3,
                    patch_id=Patch.build_id_contract(2, 0),
                )

                return

            def step(self) -> None:
                pass

        self.grid = Grid(width=10, height=10)
        self.model = TestModel(grid=self.grid)

    def test_init(self) -> None:
        runner = Runner(
            model=self.model,
            observer=None,
            executor=SequentialExecutor(),
            visitor=None,
        )
        self.assertIsInstance(runner, Runner)
