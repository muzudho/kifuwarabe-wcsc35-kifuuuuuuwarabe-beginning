import cshogi

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import PieceTypeModel, SquareModel
from ...models.layer_o1o1o0_move_list import SplitEatingBeforeMoveModel


class SplitEatingBeforeMoveLogic():
    

    @staticmethod
    def split_eating_before_move(move_list, gymnasium):
        """駒を取る手と、そうでない手に分ける。
        """

        move_not_eat_list = []  # 駒を取らない手リスト
        move_eat_list = []      # 駒を取る手リスト
        cap_list = []           # 取った駒リスト

        # 指し手を全部調べる。
        for my_move in move_list:

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            # 打の場合、取った駒無し。空マス。
            cap_pt      = gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

            if cap_pt == cshogi.NONE:
                move_not_eat_list.append(my_move)
            else:
                move_eat_list.append(my_move)
                cap_list.append(cap_pt)

        split_eating_before_move_model = SplitEatingBeforeMoveModel(
                move_not_eat_list   = move_not_eat_list,
                move_eat_list       = move_eat_list,
                cap_list            = cap_list)
        return split_eating_before_move_model
