from abc import ABC, abstractmethod

from agent_guy.world import IWorld


class IModel(ABC):
    def __init__(
        self,
        world: IWorld,
        parameters: dict = dict(),
    ) -> None:
        self.world = world
        self.parameters = parameters
        super().__init__()

    @abstractmethod
    def setup_world(self) -> None:
        pass

    @abstractmethod
    def setup_agents(self) -> None:
        pass

    @abstractmethod
    def step(self) -> None:
        pass
