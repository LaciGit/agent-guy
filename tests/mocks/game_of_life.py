from typing import Any

from agent_guy import Grid, IModel, Patch, Turtle
from agent_guy.agent.agent import Colors


class LifeCell(Turtle):
    def __init__(self, color: Colors = Colors.white) -> None:
        self.neighbors_alive = 0
        self.status = "dead"
        super().__init__(color)

    # these are custom functions for the user
    def observe(self) -> None:
        # retruns me the neighbors agent objects
        # there could be also neighbors patches
        neighbors = self.von_neumann_neighbors.values()
        # count the number of alive neighbors
        self.neighbors_alive = len([n for n in neighbors if n.status == "alive"])

        return

    def act(self) -> None:
        # if I have less than 2 neighbors I die
        if self.neighbors_alive < 2:
            self.die()
        # if I have more than 3 neighbors I die
        elif self.neighbors_alive > 3:
            self.die()
        # if I have 3 neighbors I live
        elif self.neighbors_alive == 3:
            self.live()
        # otherwise I do nothing
        else:
            pass
        return

    def die(self) -> None:
        self.status = "dead"
        self.set_color(Colors.black)
        return

    def live(self) -> None:
        self.status = "alive"
        self.set_color(Colors.white)
        return


class LifeModel(IModel):
    def __init__(self, grid: Grid, parameters: dict[str, Any] = dict()) -> None:
        super().__init__(grid, parameters)

    def setup_grid(self) -> None:
        # nothing to do here
        pass

    def setup_agents(self) -> None:
        # setup a blinker in and expect a grid of size 3x3
        # the blinker is in the middle of the grid

        # turtles
        t1 = LifeCell()
        t2 = LifeCell()
        t3 = LifeCell()

        # add turtles to grid
        self.add_turtle_to_grid(
            turtle=t1,
            patch_id=Patch.build_id_contract(x=0, y=1),
        )
        self.add_turtle_to_grid(
            turtle=t2,
            patch_id=Patch.build_id_contract(x=1, y=1),
        )
        self.add_turtle_to_grid(
            turtle=t3,
            patch_id=Patch.build_id_contract(x=2, y=1),
        )

        return

    def step(self) -> None:
        self.ask_agents(func=["observe"])

        self.ask_agents(func=["act"])
