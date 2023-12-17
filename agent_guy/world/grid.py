from agent_guy.agent import IPatch
from agent_guy.world import IWorld


class Grid(IWorld):
    def __init__(self, width: int, height: int) -> None:
        # these are the dimensions of the grid; whre x is width and y is height
        self.width = width
        self.height = height

        # the patches of the grid
        self._patches: dict[str, IPatch] = self.build_patches()

        # only present after build was called
        self.patch_ids: set[str] = set(self._patches.keys())

        super().__init__()

    def build_patches(self) -> dict[str, IPatch]:
        """build the patches for the grid

        Returns:
            dict[str, IPatch]: the patches for the grid whre str is the patch id
        """

        patches = {}

        for x in range(self.width):
            for y in range(self.height):
                patch = IPatch(x, y)
                patches[patch.agent_id] = patch

        # store the patch ids
        self.patch_ids = set(patches.keys())

        return patches

    def get_patch(self, patch_id: str) -> IPatch:
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

    def get_moore_neighbors(self, patch_id: str) -> dict[str, IPatch]:
        """get the moore neighbors of the patch as ids
        if the patch has id 3_3, the moore neighbors are:
        2_2    2_3    2_4
        3_2    None   3_4
        4_2    4_3    4_4

        3_3 is not included, nor the None


        Args:
            patch_id (str): the patch id

        Returns:
            list[str]: the moore neighbors as ids
        """

        patch = self.get_patch(patch_id)

        neighbors = set(
            [
                IPatch.build_id_contract(patch.x - 1, patch.y + 1),
                IPatch.build_id_contract(patch.x, patch.y + 1),
                IPatch.build_id_contract(patch.x + 1, patch.y + 1),
                IPatch.build_id_contract(patch.x - 1, patch.y),
                IPatch.build_id_contract(patch.x + 1, patch.y),
                IPatch.build_id_contract(patch.x - 1, patch.y - 1),
                IPatch.build_id_contract(patch.x, patch.y - 1),
                IPatch.build_id_contract(patch.x + 1, patch.y - 1),
            ]
        )

        # check if neighbors are in grid
        if not neighbors.issubset(self.patch_ids):
            raise ValueError(f"Patch {patch_id} has neighbors outside of grid")

        return {p: self.get_patch(p) for p in neighbors}

    def get_von_neumann_neighbors(self, patch_id: str) -> dict[str, IPatch]:
        """get the von neumann neighbors of the patch as ids
        if the patch has id 3_3, the von neumann neighbors are:
        None    2_3    None
        3_2    None   3_4
        None    4_3    None

        3_3 is not included, nor the None


        Args:
            patch_id (str): the patch id

        Returns:
            list[str]: the von neumann neighbors as ids
        """

        patch = self.get_patch(patch_id)

        neighbors = set(
            [
                IPatch.build_id_contract(patch.x, patch.y + 1),
                IPatch.build_id_contract(patch.x - 1, patch.y),
                IPatch.build_id_contract(patch.x + 1, patch.y),
                IPatch.build_id_contract(patch.x, patch.y - 1),
            ]
        )

        # check if neighbors are in grid
        if not neighbors.issubset(self.patch_ids):
            raise ValueError(f"Patch {patch_id} has neighbors outside of grid")

        return {p: self.get_patch(p) for p in neighbors}
