import cshogi

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import PieceTypeModel, SquareModel


class MoveListLogics():


    def when_replacing_pieces_start_with_the_cheaper_ones(move_list, gymnasium):
        """駒を交換するときは、安い駒から。
        """

        # 全ての指し手を調べ、駒を取る手と、そうでない手に分ける。
        (
            move_not_eat_list,
            move_eat_list_1,
            cap_list_1
        ) = MoveListLogics.split_eating_before_move(
                move_list   = move_list,
                gymnasium   = gymnasium)

        # ヘルスチェック
        for i in range(0, len(move_eat_list_1)):
            move_eat = move_eat_list_1[i]
            cap_pt = cap_list_1[i]
            #cur_value = PieceValuesModel.by_piece_type(pt=cap_pt)
            src_sq_obj  = SquareModel(cshogi.move_from(move_eat))   # ［移動元マス］
            src_pc = gymnasium.table.piece(src_sq_obj.sq)           # ［移動元の駒］
            src_pt = cshogi.piece_to_piece_type(src_pc)
            src_value = PieceValuesModel.by_piece_type(pt=src_pt)   # ［取った駒の価値］

            gymnasium.health_check.append(
                    move    = move_eat,
                    name    = 'SQ_eater',
                    value   = f"SQ_eater{PieceTypeModel.kanji(src_pt)}{src_value}")

        # 相手の駒Ａを、自分の駒Ｂ１、Ｂ２、…のいずれの駒でも取れる場合、
        # Ｂ１、Ｂ２、…の駒について、１番駒得の価値が低い駒を全て選び、それ以外の駒は除外します。
        (
            move_eat_list_2,
            cap_list_2
        ) = MoveListLogics.select_cheap_eaters(
                move_eat_list   = move_eat_list_1,
                cap_list        = cap_list_1,
                gymnasium       = gymnasium)

        # ヘルスチェック
        for i in range(0, len(move_eat_list_2)):
            move_eat = move_eat_list_2[i]
            cap_pt = cap_list_2[i]
            #cur_value = PieceValuesModel.by_piece_type(pt=cap_pt)
            src_sq_obj  = SquareModel(cshogi.move_from(move_eat))   # ［移動元マス］
            src_pc = gymnasium.table.piece(src_sq_obj.sq)           # ［移動元の駒］
            src_pt = cshogi.piece_to_piece_type(src_pc)
            src_value = PieceValuesModel.by_piece_type(pt=src_pt)   # ［取った駒の価値］

            gymnasium.health_check.append(
                    move    = move_eat,
                    name    = 'cheapest',
                    value   = f"cheapest{PieceTypeModel.kanji(src_pt)}{src_value}")

        move_list = move_not_eat_list
        move_list.extend(move_eat_list_2)

        return move_list


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
            src_sq_obj  = SquareModel(cshogi.move_from(move))       # ［移動元マス］
            dst_sq_obj  = SquareModel(cshogi.move_to(move))         # ［移動先マス］
            #cap_value = PieceValuesModel.by_piece_type(pt=cap_pt)   # ［取った駒の価値］

            is_drop = cshogi.move_is_drop(move) # ［打］
            if is_drop:
                continue    # 打は除外

            src_pc = gymnasium.table.piece(src_sq_obj.sq)           # ［移動元の駒］
            src_pt = cshogi.piece_to_piece_type(src_pc)
            src_value = PieceValuesModel.by_piece_type(pt=src_pt)   # ［動かした駒の価値］

            best_cheap_value = PieceValuesModel.get_big_value()

            # 駒得の価値を比較。安ければアップデート
            if src_value < best_cheap_value:
                best_cheap_value = src_value
                move_group_by_dst_sq = {}   # クリアー（他の move も全削除）
                move_group_by_dst_sq[dst_sq_obj.sq] = [(move, cap_pt)]

            # 等しければ
            elif src_value == best_cheap_value:
                # 辞書に move が既存なら、そこへ追加
                if dst_sq_obj.sq in move_group_by_dst_sq:
                    move_group_by_dst_sq[dst_sq_obj.sq].append((move, cap_pt))

                # 辞書に move を作ってなければ、新規挿入
                else:
                    move_group_by_dst_sq[dst_sq_obj.sq] = [(move, cap_pt)]

        check_value = None
        move_eat_list_2 = []
        cap_list_2 = []
        for same_list in move_group_by_dst_sq.values():
            for entry in same_list:
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

                move_eat_list_2.append(entry[0])
                cap_list_2.append(entry[1])

        return move_eat_list_2, cap_list_2
