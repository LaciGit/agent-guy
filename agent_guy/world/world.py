from abc import ABC, abstractmethod

from agent_guy.agent import ITurtle


class IWorld(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def ask_agents(self, func: list[str]) -> None:
        # ask all agent like turtles, patches, etc.
        pass

    @abstractmethod
    def ask_turtles(self, func: list[str]) -> None:
        pass

    @abstractmethod
    def add_turtle(self, turtle: ITurtle) -> None:
        pass
