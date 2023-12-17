import numpy as np

from agent_guy.agent import Patch, Turtle
from agent_guy.world import IWorld


class Grid(IWorld):
    def __init__(self, width: int, height: int) -> None:
        # these are the dimensions of the grid; whre x is width and y is height
        self.width = width
        self.height = height

        # the patches of the grid
        self.patches: dict[str, Patch] = self._build_patches()

        # only present after build was called
        self.patch_ids: set[str] = set(self.patches.keys())
        self.count_patches: int = len(self.patch_ids)
        self._update_patches_by_neighbors()

        super().__init__()

    # def __str__(self) -> str:
    #     # TODO: implement build_matrix_patches
    #     return (
    #         f"Grid: width={self.width}, height={self.height}\n"
    #         f"{str(self.build_matrix_patches())} \n"
    #         f"{str(self.build_matrix_turtles())} \n"
    #     )

    # def build_matrix_patches(self) -> np.ndarray:
    #     matrix = []

    #     for i_width in range(self.width):
    #         row = []
    #         for i_height in range(self.height):
    #             patch_id = Patch.build_id_contract(i_width, i_height)
    #             patch = self.patches[patch_id]
    #             row.append(patch)
    #         matrix.append(row)

    #     return np.matrix(matrix)

    # def build_matrix_turtles(self) -> np.ndarray:
    #     matrix = []

    #     for i_width in range(self.width):
    #         row = []
    #         for i_height in range(self.height):
    #             patch_id = Patch.build_id_contract(i_width, i_height)
    #             patch = self.patches[patch_id]
    #             if t := list(patch.get_turtles().values()):
    #                 row.append(str(t[0]))
    #             else:
    #                 row.append(None)

    #         matrix.append(row)

    #     return np.matrix(matrix)

    def _build_patches(self) -> dict[str, Patch]:
        """build the patches for the grid

        Returns:
            dict[str, IPatch]: the patches for the grid whre str is the patch id
        """

        patches = {}

        for x in range(self.width):
            for y in range(self.height):
                patch = Patch(x, y)

                patches[patch.agent_id] = patch

        return patches

    def get_neighbors(
        self,
        patch_id: str,
        type: str,
        ignore_oob: bool = False,
    ) -> set[str]:
        """get the neighbors of the patch as ids

        ### moore neighbors
        get the moore neighbors of the patch as ids
        if the patch has id 3_3, the moore neighbors are:
        2_2   3_2    4_2
        2_3   None    4_3
        2_4   3_4    4_4

        3_3 is not included, nor the None

        ### neumann neighbors
        get the von neumann neighbors of the patch as ids
        if the patch has id 3_3, the von neumann neighbors are:
        None   3_2    None
        2_3   None    4_3
        None   3_4    None

        Args:
            patch_id (str): the patch id
            type (str): the type of neighbors to get, either 'moore' or 'von_neumann'
            ignore_oob (bool, optional): ignore out of bounds neighbors. Defaults to False.

        Returns:
            set[str]: the neighbors as ids

        Raises:
            ValueError: if the patch has neighbors outside of the grid

        """

        patch = self.patches[patch_id]

        moore_neighbors = set(
            [
                Patch.build_id_contract(patch.x - 1, patch.y - 1),
                Patch.build_id_contract(patch.x, patch.y - 1),
                Patch.build_id_contract(patch.x + 1, patch.y - 1),
                Patch.build_id_contract(patch.x - 1, patch.y),
                Patch.build_id_contract(patch.x + 1, patch.y),
                Patch.build_id_contract(patch.x - 1, patch.y + 1),
                Patch.build_id_contract(patch.x, patch.y + 1),
                Patch.build_id_contract(patch.x + 1, patch.y + 1),
            ]
        )

        von_neumann_neighbors = set(
            [
                Patch.build_id_contract(patch.x, patch.y - 1),
                Patch.build_id_contract(patch.x - 1, patch.y),
                Patch.build_id_contract(patch.x + 1, patch.y),
                Patch.build_id_contract(patch.x, patch.y + 1),
            ]
        )

        if type == "moore":
            neighbors_build = moore_neighbors
        elif type == "von_neumann":
            neighbors_build = von_neumann_neighbors
        else:
            raise ValueError(f"Unknown type '{type}'")

        # check if neighbors are in grid
        if not neighbors_build.issubset(self.patch_ids):
            # check if we should ignore out of bounds neighbors
            if ignore_oob:
                to_del = neighbors_build.difference(self.patch_ids)
                neighbors_build.difference_update(to_del)
            else:
                raise ValueError(f"Patch {patch_id} has neighbors outside of grid")

        return neighbors_build

    def _update_patches_by_neighbors(self) -> None:
        """update all the patches by their neighbors"""

        for patch in self.patches.values():
            patch.moore_neighbor_ids = self.get_neighbors(
                patch_id=patch.agent_id,
                type="moore",
                ignore_oob=True,
            )
            patch.von_neumann_neighbor_ids = self.get_neighbors(
                patch_id=patch.agent_id,
                type="von_neumann",
                ignore_oob=True,
            )

        return

    def update_turtles_by_neighbors(
        self,
        turtles: dict[str, Turtle],
        neighborhood: list[str] = ["moore", "von_neumann"],
    ) -> None:
        """update the turtles by their neighbors

        Args:
            turtles (dict[str, Turtle]): the turtles to update
            neighborhood (list[str], optional): the neighborhoods to update.
                Defaults to ["moore", "von_neumann"].
        """

        # update the neighbors of the turtles
        for turtle in turtles.values():
            # get turtle's patch
            patch = self.patches[turtle.patch_id]

            for func_name in neighborhood:
                # update_func_name = f"update_{func_name}_neighbors"
                # update_func_name = f"update_{func_name}_neighbors"

                neighbor_ids = f"{func_name}_neighbor_ids"
                neighbor_turtles = f"{func_name}_neighbors"

                # get patch neighbors
                patch_neighbors = getattr(patch, neighbor_ids)

                # current patch_neighbors moore patch_neighbors of patch
                current_neighbors = getattr(turtle, neighbor_turtles)

                # get all new patch_neighbors from the moore patch_neighbors
                new_neighbors = {}
                for n_id in patch_neighbors:
                    n_patch = self.patches[n_id]

                    new_neighbors.update(
                        {
                            a_id: a
                            for a_id, a in n_patch.get_turtles().items()
                            if a_id not in current_neighbors.keys()
                        }
                    )

                # update moore neighbors
                turtle.overwrite_neighbors(
                    neighbors=new_neighbors,
                    func_name=func_name,
                )

        return
