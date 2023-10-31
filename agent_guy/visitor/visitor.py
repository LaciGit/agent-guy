from abc import ABC, abstractmethod

from agent_guy.observer import IObserver


class IVisitor(ABC):
    @abstractmethod
    def visit(self, observer: IObserver) -> None:
        pass
