from abc import ABC, abstractmethod
from enum import Enum
from functools import cached_property


class Colors(Enum):
    black = [0, 0, 0]
    white = [255, 255, 255]
    red = [255, 0, 0]
    green = [0, 255, 0]
    blue = [0, 0, 255]
    yellow = [255, 255, 0]
    cyan = [0, 255, 255]
    magenta = [255, 0, 255]
    gray = [128, 128, 128]
    dark_red = [128, 0, 0]
    dark_green = [0, 128, 0]
    dark_blue = [0, 0, 128]
    dark_yellow = [128, 128, 0]
    dark_cyan = [0, 128, 128]
    dark_magenta = [128, 0, 128]
    dark_gray = [64, 64, 64]


class IAgent(ABC):
    def __init__(self, color: Colors = Colors.white) -> None:
        self._color = color

        # if the turtle should be deleted at the end of the step
        self._to_be_deleted = False

        super().__init__()

    def get_color(self) -> Colors:
        return self._color

    def set_color(self, color: Colors) -> None:
        # check if color is enum
        if not isinstance(color, Colors):
            raise ValueError(f"Color must be of type {Colors}")
        self._color = color

    @abstractmethod
    def _build_id(self) -> str:
        pass

    @cached_property
    def agent_id(self) -> str:
        return self._build_id()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, self.__class__):
            return False

        return self.agent_id == __value.agent_id

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.agent_id}]"
