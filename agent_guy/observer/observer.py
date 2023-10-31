from abc import ABC, abstractmethod

from agent_guy.model import IModel


class IObserver(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def aggregate(self, model: IModel) -> None:
        pass
