from abc import ABC, abstractmethod


class IExecutor(ABC):
    def __init__(self, max_step: int = 1) -> None:
        self.max_step = max_step
        if max_step < 1:
            raise ValueError("'max_step' must be greater than 0")

        super().__init__()

    @abstractmethod
    def execute_order(self, agent_ids: list[str]) -> list[str]:
        """return the order of agents which should be executed

        Args:
            agent_ids (list[str]): the agent ids to execute

        Returns:
            list[str]: the order of agents which should be executed
        """
        pass
