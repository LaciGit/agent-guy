from agent_guy.executor import IExecutor
from agent_guy.model import IModel
from agent_guy.observer import IObserver
from agent_guy.visitor import IVisitor


class Runner:
    def __init__(
        self,
        model: IModel,
        observer: IObserver,
        executor: IExecutor,
        visitor: IVisitor,
    ) -> None:
        self.model = model
        self.observer = observer
        self.executor = executor
        self.visitor = visitor
