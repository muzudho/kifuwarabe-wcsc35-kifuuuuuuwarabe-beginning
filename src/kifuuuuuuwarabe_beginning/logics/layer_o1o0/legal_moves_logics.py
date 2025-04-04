import cshogi

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import SquareModel


class LegalMovesLogics():


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

        return move_not_eat_list, move_eat_list, cap_list


    def select_cheap_eaters(move_eat_list, cap_list, gymnasium):
        """相手の駒Ａを、自分の駒Ｂ１、Ｂ２、…のいずれの駒でも取れる場合、
        Ｂ１、Ｂ２、…の駒について、１番駒得の価値が低い駒を全て選び、それ以外の駒は除外します。
        """

        move_group_by_dst_sq = {}

        # 移動先でグループ化する。
        for i in range(0, len(move_eat_list)):
            move = move_eat_list[i]
            cap_pt = cap_list[i]
            dst_sq_obj  = SquareModel(cshogi.move_to(move))      # ［移動先マス］
            cur_value = PieceValuesModel.by_piece_type(pt=cap_pt)
            best_cheap_value = PieceValuesModel.get_big_value()

            if dst_sq_obj.sq in move_group_by_dst_sq:
                # 駒得の価値を比較。安ければアップデート
                if cur_value < best_cheap_value:
                    best_cheap_value = cur_value
                    move_group_by_dst_sq[dst_sq_obj.sq] = [(move, cap_pt)]
                # 等しければ追加
                elif cur_value == best_cheap_value:
                    move_group_by_dst_sq[dst_sq_obj.sq].append((move, cap_pt))
                # それ以外は無視。

            else:
                best_cheap_value = cur_value
                move_group_by_dst_sq[dst_sq_obj.sq] = [(move, cap_pt)]

        move_eat_list_2 = []
        cap_list_2 = []
        for same_list in move_group_by_dst_sq.values():
            for entry in same_list:
                move_eat_list_2.append(entry[0])
                cap_list_2.append(entry[1])

        return move_eat_list_2, cap_list_2
