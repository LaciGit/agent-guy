from typing import Any

from abc import ABC, abstractmethod
from functools import cached_property
from itertools import chain

from agent_guy.agent import Turtle
from agent_guy.executor import IExecutor
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

        # the executor to execute the model
        self.executor: IExecutor = None

        super().__init__()

    def add_executor(self, executor: IExecutor) -> None:
        """add the executor

        Args:
            executor (IExecutor): the executor to add

        Raises:
            ValueError: if the executor is not of type IExecutor
        """

        # check if executor is executor
        if not issubclass(executor.__class__, IExecutor):
            raise ValueError("'executor' must be of type 'IExecutor'")

        # add executor
        self.executor = executor

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
        raise NotImplementedError("'ask_agents' not implemented")

    @cached_property
    def _pos_turtle_funcs(self) -> set[str]:
        return set(
            chain.from_iterable(list([dir(turtle) for turtle in self.turtles.values()]))
        )

    def ask_turtles(self, func: list[str]) -> None:
        # possible functions in turtles
        if not set(func).issubset(self._pos_turtle_funcs):
            raise ValueError(f"Invalid function in: {func}")

        # get execution order of turtles
        turtle_ids = self.executor.execute_order(list(self.turtles.keys()))

        self.grid.update_turtles_by_neighbors(turtles=self.turtles)

        for turtle_id in turtle_ids:
            for func_name in func:
                try:
                    turtle = self.turtles[turtle_id]
                    # execute function on instance
                    getattr(turtle, func_name)()
                except Exception as e:
                    raise RuntimeError(
                        f"Error executing function '{func_name}' on turtle '{turtle}'"
                        f"{turtle.__class__}: {e}"
                    )

        return
