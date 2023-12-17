from agent_guy.agent import Colors, IAgent, Turtle


class Patch(IAgent):
    def __init__(self, x: int, y: int, color: Colors = Colors.white) -> None:
        self.x = x
        self.y = y

        # the turtle's which are on the given patch
        self._turtles_on_patch: dict[str, Turtle] = {}

        # the neighbors of the patch
        self._moore_neighbor_ids: set[str] = set()
        self._von_neumann_neighbor_ids: set[str] = set()

        super().__init__(color)

    @staticmethod
    def build_id_contract(x: int, y: int) -> str:
        return f"{x}_{y}"

    def _build_id(self) -> str:
        return Patch.build_id_contract(self.x, self.y)

    def add_turtle(self, turtle: Turtle) -> None:
        """add a turtle to the patch

        Args:
            turtle (ITurtle): the turtle to add to the patch

        Raises:
            ValueError: if the turtle is already on the patch
        """

        if not issubclass(turtle.__class__, Turtle):
            raise ValueError(f"Can only add turtles to patch, not '{turtle.__class__}'")

        # check if turtle already on patch
        if turtle.agent_id in self._turtles_on_patch:
            raise ValueError(f"Turtle {turtle} already on patch {self}")

        # update turtle's patch id
        turtle.patch_id = self.agent_id

        # add turtle to patch
        self._turtles_on_patch[turtle.agent_id] = turtle

    def rm_turtle(self, turtle: Turtle) -> None:
        """remove a turtle from the patch

        Args:
            turtle (ITurtle): the turtle to remove from the patch

        Raises:
            ValueError: if the turtle is not on the patch
        """

        # check if turtle on patch
        if turtle.agent_id not in self._turtles_on_patch:
            raise ValueError(f"Turtle {turtle} not on patch {self}")

        # update turtle's patch id
        turtle.patch_id = None

        # remove turtle from patch
        del self._turtles_on_patch[turtle.agent_id]

    def get_turtles(self, turtle_ids: list[str] = list()) -> dict[str, Turtle]:
        """get the turtles on the patch

        Args:
            turtle_ids (list[str], optional): if provided you may filter.
                Defaults to list().

        Raises:
            ValueError: if a turtle id is provided which is not on the patch

        Returns:
            dict[str, Turtle]: the turtles on the patch where the key is the turtle id
        """

        # if no turtle ids provided, return all turtles
        if not turtle_ids:
            return self._turtles_on_patch.copy()

        # check if all turtle ids are on the patch
        dict_turtles = {}
        for turle_id in turtle_ids:
            turtle = self._turtles_on_patch.get(turle_id, None)

            if turtle is None:
                raise ValueError(f"Turtle {turle_id} not on patch {self}")

            dict_turtles[turle_id] = turtle

        return dict_turtles
