from uuid import uuid4

from agent_guy.agent import Colors, IAgent


class ITurtle(IAgent):
    def __init__(self, color: Colors = Colors.white) -> None:
        # the patch the turtle is on (if any) and only id
        self.patch_id: str = None
        super().__init__(color)

    def kill(self) -> None:
        """kill the turtle at the end of the step"""
        self._to_be_deleted = True

    def _build_id(self) -> str:
        return str(uuid4())
