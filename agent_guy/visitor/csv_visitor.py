from agent_guy.observer import IObserver
from agent_guy.visitor import IVisitor


class CsvVisitor(IVisitor):
    def visit(self, observer: IObserver) -> None:
        return super().visit(observer)
