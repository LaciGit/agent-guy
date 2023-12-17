import logging
import unittest

from agent_guy import Grid, IModel, Patch, Runner, SequentialExecutor, Turtle
from tests.mocks.game_of_life import LifeCell, LifeModel

logging.basicConfig(level=logging.DEBUG)


class TestRunner(unittest.TestCase):
    def setUp(self) -> None:
        self.grid = Grid(width=5, height=5)
        self.model = LifeModel(grid=self.grid)

    def test_init(self) -> None:
        runner = Runner(
            model=self.model,
            observer=None,
            executor=SequentialExecutor(),
            visitor=None,
        )
        self.assertIsInstance(runner, Runner)

    def test_step(self):
        runner = Runner(
            model=self.model,
            observer=None,
            executor=SequentialExecutor(max_step=6),
            visitor=None,
            debug=True,
        )

        runner.run()

        print()
