from agent_guy.agent.agent import IAgent


class ITurtle(IAgent):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        super().__init__()
