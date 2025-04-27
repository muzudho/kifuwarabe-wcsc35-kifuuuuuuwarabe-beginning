import cshogi

from . import HelperRoutines
from ..layer_o1o1o0_move_list import SplitEatingBeforeMoveRoutines
from ...models.layer_o1o_9o0 import PieceValuesModel, PlanetPieceModel
from ...models.layer_o1o0 import PieceTypeModel, SquareModel
from ...models.layer_o1o1o0_move_list import SplitEatingBeforeMoveModel


class MoveListRoutines():


    @staticmethod
    def move_list_map_usi_list(move_list):
        usi_list = []
        for move in move_list:
            usi_list.append(cshogi.move_to_usi(move))

        return usi_list
