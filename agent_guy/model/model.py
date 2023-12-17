from typing import Any

from abc import ABC, abstractmethod

from agent_guy.agent import Patch, Turtle
from agent_guy.world import Grid


class IModel(ABC):
    def __init__(
        self,
        grid: Grid,
        parameters: dict[str, Any] = dict(),
    ) -> None:
        self.grid = grid
        self.parameters = parameters

        # check if grid is grid
        if not isinstance(self.grid, Grid):
            raise ValueError("'grid' must be of type 'Grid'")

        # self._patches: dict[str, IPatch] = self.grid.build_patches()
        self.turtles: dict[str, Turtle] = dict()

        super().__init__()

    @abstractmethod
    def setup_grid(self) -> None:
        pass

    @abstractmethod
    def setup_agents(self) -> None:
        pass

    @abstractmethod
    def step(self) -> None:
        pass

    def add_turtle_to_grid(self, turtle: Turtle, patch_id: str) -> None:
        """add a turtle to the grid

        Args:
            turtle (ITurtle): turtle object
            patch_id (str): the patch id to add the turtle to

        Raises:
            ValueError: if the turtle is already in the grid
        """

        # check if turtle already in grid
        if turtle.agent_id in self.turtles:
            raise ValueError(f"Turtle {turtle} already in grid")

        # get patch
        patch = self.grid.get_patch(patch_id)

        # add turtle to patch
        patch.add_turtle(turtle)

        # update current list of turtles
        self.turtles[turtle.agent_id] = turtle

    def remove_turtle_from_grid(self, turtle: Turtle) -> None:
        """remove a turtle from the grid

        Args:
            turtle (ITurtle): the turtle to remove from the grid

        Raises:
            ValueError: if the turtle is not in the grid
        """

        # check if turtle in grid
        if turtle.agent_id not in self.turtles:
            raise ValueError(f"Turtle {turtle} not in grid")

        # get patch
        patch = self.grid.get_patch(turtle.patch_id)

        # remove turtle from patch
        patch.rm_turtle(turtle)

        # remove turtle from current list of turtles
        del self.turtles[turtle.agent_id]

    def ask_agents(self, func: list[str]) -> None:
        # ask all agent like turtles, patches, etc.
        raise NotImplementedError()

    def ask_turtles(self, func: list[str]) -> None:
        raise NotImplementedError()
