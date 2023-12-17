from uuid import uuid4

from agent_guy.agent.agent import Colors, IAgent


class Turtle(IAgent):
    def __init__(self, color: Colors = Colors.white) -> None:
        # the patch the turtle is on (if any) and only id
        self.patch_id: str = None

        # the neighbors of the patch
        self._moore_neighbors: dict[str, Turtle] = {}
        self._count_moore_neighbors: int = 0

        self._von_neumann_neighbors: dict[str, Turtle] = {}
        self._count_von_neumann_neighbors: int = 0

        super().__init__(color)

    @property
    def moore_neighbors(self) -> dict[str, "Turtle"]:
        """get the moore neighbors of the turtle

        Returns:
            dict[str, Turtle]: the moore neighbors of the turtle
        """
        return self._moore_neighbors

    @property
    def von_neumann_neighbors(self) -> dict[str, "Turtle"]:
        """get the von neumann neighbors of the turtle

        Returns:
            dict[str, Turtle]: the von neumann neighbors of the turtle
        """
        return self._von_neumann_neighbors

    @property
    def count_moore_neighbors(self) -> int:
        """get the number of moore neighbors of the turtle

        Returns:
            int: the number of moore neighbors of the turtle
        """
        return self._count_moore_neighbors

    @property
    def count_von_neumann_neighbors(self) -> int:
        """get the number of von neumann neighbors of the turtle

        Returns:
            int: the number of von neumann neighbors of the turtle
        """
        return self._count_von_neumann_neighbors

    def kill(self) -> None:
        """kill the turtle at the end of the step"""
        self._to_be_deleted = True

    def move(self, patch_id: str) -> None:
        """move the turtle to the given patch

        Args:
            patch_id (str): the patch id to move the turtle to
        """
        self.patch_id = patch_id

    def update_moore_neighbors(
        self,
        del_neighbors: dict[str, "Turtle"],
        add_neighbors: dict[str, "Turtle"],
    ) -> None:
        """update the moore neighbors of the turtle

        - if a neighbor to add is already in the moore neighbors, a ValueError is raised
        - if a neighbor to remove is not in the moore neighbors, nothing happens

        Args:
            del_neighbors (dict[str, Turtle]): neighbors to remove
            add_neighbors (dict[str, Turtle]): neighbors to add

        Raises:
            ValueError: if a neighbor to add is already in the moore neighbors
        """

        self._update_neighbors(
            del_neighbors=del_neighbors,
            add_neighbors=add_neighbors,
            func_name="moore",
        )

    def update_von_neumann_neighbors(
        self,
        del_neighbors: dict[str, "Turtle"],
        add_neighbors: dict[str, "Turtle"],
    ) -> None:
        """update the von neumann neighbors of the turtle

        Args:
            del_neighbors (dict[str, Turtle]): neighbors to remove
            add_neighbors (dict[str, Turtle]): neighbors to add
        """

        self._update_neighbors(
            del_neighbors=del_neighbors,
            add_neighbors=add_neighbors,
            func_name="von_neumann",
        )

    def _update_neighbors(
        self,
        del_neighbors: dict[str, "Turtle"],
        add_neighbors: dict[str, "Turtle"],
        func_name: str,
    ) -> None:
        """update the neighbors of the turtle

        Args:
            del_neighbors (dict[str, Turtle]): neighbors to remove
            add_neighbors (dict[str, Turtle]): neighbors to add
            func_name (str): 'von_neumann' or 'moore'

        Raises:
            ValueError: if a neighbor to add is already in the neighbors
        """

        dict_name = f"_{func_name}_neighbors"
        count_name = f"_count_{func_name}_neighbors"

        dict_to_update = getattr(self, dict_name)
        count_to_update = getattr(self, count_name)

        # remove neighbors
        for n_id in del_neighbors.keys():
            dict_to_update.pop(n_id, None)
            count_to_update -= 1

        # add neighbors
        for neighbor in add_neighbors.values():
            if neighbor.agent_id in dict_to_update:
                raise ValueError(f"Neighbor {neighbor} already in neighbors of {self}")

            dict_to_update[neighbor.agent_id] = neighbor
            count_to_update += 1

        setattr(self, count_name, count_to_update)

        return

    def _build_id(self) -> str:
        return str(uuid4())
