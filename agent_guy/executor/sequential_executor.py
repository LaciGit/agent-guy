from agent_guy.executor import IExecutor


class SequentialExecutor(IExecutor):
    def execute(self) -> None:
        raise NotImplementedError("SequentialExecutor.execute()")
