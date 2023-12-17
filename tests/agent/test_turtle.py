import unittest

from agent_guy import Colors
from tests.mocks.game_of_life import LifeCell


class TestTurtle(unittest.TestCase):
    def setUp(self) -> None:
        self.cell = LifeCell()

    def test_init(self) -> None:
        self.assertEqual(self.cell.status, "dead")

    def test_cell_of_life(self) -> None:
        self.cell.live()
        self.assertEqual(self.cell.status, "alive")
        self.assertEqual(self.cell.get_color(), Colors.white)

        self.cell.die()
        self.assertEqual(self.cell.status, "dead")
        self.assertEqual(self.cell.get_color(), Colors.black)

        # set cell count to 3 and check if cell is alive
        self.cell.neighbors_alive = 3
        self.cell.act()
        self.assertEqual(self.cell.status, "alive")
        self.assertEqual(self.cell.get_color(), Colors.white)

        # set cell count to 2 and check if cell is alive
        self.cell.neighbors_alive = 2
        self.cell.act()
        self.assertEqual(self.cell.status, "alive")

        # set cell count to 1 and check if cell is dead
        self.cell.neighbors_alive = 1
        self.cell.act()
        self.assertEqual(self.cell.status, "dead")

    def test_neighbors(self) -> None:
        # three cells and we fake that one of them has two neighbors
        cell_1 = LifeCell()
        cell_2 = LifeCell()
        cell_3 = LifeCell()

        # add cell_2 and cell_3 to cell_1
        cell_1.update_moore_neighbors(
            add_neighbors={
                cell_2.agent_id: cell_2,
                cell_3.agent_id: cell_3,
            },
            del_neighbors={},
        )
        cell_1.update_von_neumann_neighbors(
            add_neighbors={
                cell_2.agent_id: cell_2,
                cell_3.agent_id: cell_3,
            },
            del_neighbors={},
        )

        # check if cell_1 has two neighbors
        self.assertEqual(cell_1._count_moore_neighbors, 2)
        self.assertEqual(cell_1._count_von_neumann_neighbors, 2)

        # delete cell_2 from cell_1
        cell_1.update_moore_neighbors(
            add_neighbors={},
            del_neighbors={cell_2.agent_id: cell_2},
        )
        cell_1.update_von_neumann_neighbors(
            add_neighbors={},
            del_neighbors={cell_2.agent_id: cell_2},
        )

        self.assertEqual(cell_1._count_moore_neighbors, 1)
        self.assertEqual(cell_1._count_von_neumann_neighbors, 1)
