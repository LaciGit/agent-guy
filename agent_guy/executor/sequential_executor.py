from agent_guy.executor import IExecutor


class SequentialExecutor(IExecutor):
    def execute_order(self, agent_ids: list[str]) -> list[str]:
        """return the order of agents which should be executed

        Args:
            agent_ids (list[str]): the agent ids to execute

        Returns:
            list[str]: the order of agents which should be executed
        """
        return agent_ids
