from typing import Any

import random

from agent_guy import Grid, IModel, Patch, Turtle
from agent_guy.agent.agent import Colors


class LifeCell(Turtle):
    def __init__(self, color: Colors = Colors.white, living: bool = False) -> None:
        self.neighbors_alive = 0
        self.living = living
        if living:
            color = Colors.black
        super().__init__(color)

    def __str__(self) -> str:
        return self._color.name.upper()

    # these are custom functions for the user
    def observe(self) -> None:
        # retruns me the neighbors agent objects
        # there could be also neighbors patches
        neighbors = self.moore_neighbors.values()
        # count the number of alive neighbors
        self.neighbors_alive = len([n for n in neighbors if n.living])

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
        self.living = False
        self.set_color(Colors.white)
        return

    def live(self) -> None:
        self.living = True
        self.set_color(Colors.black)
        return


class LifeModel(IModel):
    def __init__(self, grid: Grid, parameters: dict[str, Any] = dict()) -> None:
        parameters["chance_alive"] = 0.5

        super().__init__(grid, parameters)

    def setup_grid(self) -> None:
        # nothing to do here
        pass

    def setup_agents(self) -> None:
        # setup a blinker in and expect a grid of size 3x3
        # the blinker is in the middle of the grid

        # create for each patch a turtle
        for patch_id in self.grid.patch_ids:
            if random.random() <= self.parameters["chance_alive"]:
                t1 = LifeCell(living=True)
            else:
                t1 = LifeCell(living=False)

            self.add_turtle_to_grid(
                turtle=t1,
                patch_id=patch_id,
            )

        return

    def step(self) -> None:
        self.ask_turtles(func=["observe"])
        self.ask_turtles(func=["act"])

        # self.ask_turtles(func=["observe", "act"])
