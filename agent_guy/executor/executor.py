from abc import ABC, abstractmethod


class IExecutor(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def execute(self) -> None:
        pass
