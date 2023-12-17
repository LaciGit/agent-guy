from agent_guy.agent import Patch
from agent_guy.world import IWorld


class Grid(IWorld):
    def __init__(self, width: int, height: int) -> None:
        # these are the dimensions of the grid; whre x is width and y is height
        self.width = width
        self.height = height

        # the patches of the grid
        self._patches: dict[str, Patch] = self._build_patches()

        # only present after build was called
        self.patch_ids: set[str] = set(self._patches.keys())
        self.count_patches: int = len(self.patch_ids)
        self._update_patches_by_neighbors()

        super().__init__()

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

    def get_patch(self, patch_id: str) -> Patch:
        """get a patch by its id

        Args:
            patch_id (str): the patch id

        Raises:
            ValueError: if the patch id does not exist

        Returns:
            IPatch: the patch
        """
        patch = self._patches.get(patch_id, None)

        if not patch:
            raise ValueError(f"Patch {patch_id} does not exist in grid")

        return patch

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
        2_2    2_3    2_4
        3_2    None   3_4
        4_2    4_3    4_4

        3_3 is not included, nor the None

        ### neumann neighbors
        get the von neumann neighbors of the patch as ids
        if the patch has id 3_3, the von neumann neighbors are:
        None    2_3    None
        3_2    None   3_4
        None    4_3    None

        Args:
            patch_id (str): the patch id
            type (str): the type of neighbors to get, either 'moore' or 'von_neumann'
            ignore_oob (bool, optional): ignore out of bounds neighbors. Defaults to False.

        Returns:
            set[str]: the neighbors as ids

        Raises:
            ValueError: if the patch has neighbors outside of the grid

        """

        patch = self.get_patch(patch_id)

        moore_neighbors = set(
            [
                Patch.build_id_contract(patch.x - 1, patch.y + 1),
                Patch.build_id_contract(patch.x, patch.y + 1),
                Patch.build_id_contract(patch.x + 1, patch.y + 1),
                Patch.build_id_contract(patch.x - 1, patch.y),
                Patch.build_id_contract(patch.x + 1, patch.y),
                Patch.build_id_contract(patch.x - 1, patch.y - 1),
                Patch.build_id_contract(patch.x, patch.y - 1),
                Patch.build_id_contract(patch.x + 1, patch.y - 1),
            ]
        )

        von_neumann_neighbors = set(
            [
                Patch.build_id_contract(patch.x, patch.y + 1),
                Patch.build_id_contract(patch.x - 1, patch.y),
                Patch.build_id_contract(patch.x + 1, patch.y),
                Patch.build_id_contract(patch.x, patch.y - 1),
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

        for patch in self._patches.values():
            patch._moore_neighbor_ids = self.get_neighbors(
                patch_id=patch.agent_id,
                type="moore",
                ignore_oob=True,
            )
            patch._von_neumann_neighbor_ids = self.get_neighbors(
                patch_id=patch.agent_id,
                type="von_neumann",
                ignore_oob=True,
            )

        return
