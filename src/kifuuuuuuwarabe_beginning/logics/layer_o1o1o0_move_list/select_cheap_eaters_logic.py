import cshogi

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import SquareModel
from ...models.layer_o1o1o0_move_list import SelectCheapEatersModel


class SelectCheapEatersLogic():
    

    @staticmethod
    def select_cheap_eaters(move_eat_list, gymnasium):
        """相手の駒Ａを、自分の駒Ｂ１、Ｂ２、…のいずれの駒でも取れる場合、
        Ｂ１、Ｂ２、…の駒について、１番駒得の価値が低い駒を全て選び、それ以外の駒は除外します。
        """

        move_group_by_dst_sq = {}

        best_cheap_value = PieceValuesModel.get_big_value()

        # 移動先でグループ化する。
        for move in move_eat_list:
            is_drop = cshogi.move_is_drop(move) # ［打］
            if is_drop:
                continue    # 打は除外

            src_sq_obj  = SquareModel(cshogi.move_from(move))       # ［移動元マス］
            dst_sq_obj  = SquareModel(cshogi.move_to(move))         # ［移動先マス］
            src_pc = gymnasium.table.piece(src_sq_obj.sq)           # ［移動元の駒］
            src_pt = cshogi.piece_to_piece_type(src_pc)
            src_value = PieceValuesModel.by_piece_type(pt=src_pt)   # ［動かした駒の価値］

            # 駒得の価値を比較。安ければアップデート
            if src_value < best_cheap_value:
                best_cheap_value = src_value
                move_group_by_dst_sq = {}   # クリアー（他の move も全削除）
                move_group_by_dst_sq[dst_sq_obj.sq] = [move]

            # 等しければ
            elif src_value == best_cheap_value:
                # 辞書に move が既存なら、そこへ追加
                if dst_sq_obj.sq in move_group_by_dst_sq:
                    move_group_by_dst_sq[dst_sq_obj.sq].append(move)

                # 辞書に move を作ってなければ、新規挿入
                else:
                    move_group_by_dst_sq[dst_sq_obj.sq] = [move]

        check_value = None
        cheapest_eat_move_list = []
        for same_list in move_group_by_dst_sq.values():
            for move in same_list:
                # チェック
                src_sq_obj  = SquareModel(cshogi.move_from(move))       # ［移動元マス］
                src_pc = gymnasium.table.piece(src_sq_obj.sq)           # ［移動元の駒］
                src_pt = cshogi.piece_to_piece_type(src_pc)
                src_value = PieceValuesModel.by_piece_type(pt=src_pt)   # ［動かした駒の価値］
                if check_value is not None:
                    if check_value != src_value:
                        raise ValueError(f"D-142: {check_value=} {src_value=}")
                else:
                    check_value = src_value

                cheapest_eat_move_list.append(move)

        select_cheap_eaters_model = SelectCheapEatersModel(
                move_group_by_dst_sq    = move_group_by_dst_sq,
                cheapest_eat_move_list  = cheapest_eat_move_list)

        return select_cheap_eaters_model
