from abc import ABC, abstractmethod


class IWorld(ABC):
    def __init__(self) -> None:
        super().__init__()
