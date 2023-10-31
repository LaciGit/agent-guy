from agent_guy.executor import IExecutor


class RandomExecutor(IExecutor):
    def execute(self) -> None:
        raise NotImplementedError("RandomExecutor.execute()")
