import cshogi

from ...logics.layer_o1o0 import Helper
from ...logics.layer_o1o1o0_move_list import SelectCheapEatersLogic, SplitEatingBeforeMoveLogic
from ...models.layer_o1o_9o0 import PieceValuesModel, PlanetPieceModel
from ...models.layer_o1o0 import PieceTypeModel, SquareModel
from ...models.layer_o1o1o0_move_list import SplitEatingBeforeMoveModel


class MoveListLogics():


    @staticmethod
    def move_list_map_usi_list(move_list):
        usi_list = []
        for move in move_list:
            usi_list.append(cshogi.move_to_usi(move))

        return usi_list


    def when_replacing_pieces_start_with_the_cheaper_ones(move_list, gymnasium):
        """駒を交換するときは、安い駒から。
        """

        # 全ての指し手を調べ、駒を取る手と、そうでない手に分ける。
        split_eating_before_move_model = SplitEatingBeforeMoveLogic.split_eating_before_move(
                move_list   = move_list,
                gymnasium   = gymnasium)

        # # ロガー Ok
        # for move_not_eat in split_eating_before_move_model.move_not_eat_list:
        #     gymnasium.thinking_logger_module.append(f"D-1: {cshogi.move_to_usi(move_not_eat)=}")

        # # ロガー Ok
        # for move_eat in split_eating_before_move_model.move_eat_list:
        #     gymnasium.thinking_logger_module.append(f"D-2: {cshogi.move_to_usi(move_eat)=}")

        # ヘルスチェック
        for i in range(0, len(split_eating_before_move_model.move_eat_list)):
            move_eat = split_eating_before_move_model.move_eat_list[i]
            cap_pt = split_eating_before_move_model.cap_list[i]
            src_sq_obj  = SquareModel(cshogi.move_from(move_eat))   # ［移動元マス］
            src_pc = gymnasium.table.piece(src_sq_obj.sq)           # ［移動元の駒］
            src_pt = cshogi.piece_to_piece_type(src_pc)
            src_value = PieceValuesModel.by_piece_type(pt=src_pt)   # ［取った駒の価値］

            gymnasium.health_check_go_model.append(
                    move    = move_eat,
                    name    = 'SQ_eater',
                    value   = f"SQ_eater{PlanetPieceModel.kanji(piece=src_pc, is_gote=gymnasium.table.is_gote)}{src_value}")

        # TODO 相手の駒Ａを、自分の駒Ｂ１、Ｂ２、…のいずれの駒でも取れる場合、
        # Ｂ１、Ｂ２、…の駒について、１番駒得の価値が低い駒を全て選び、それ以外の駒は除外します。
        select_cheap_eaters_model = SelectCheapEatersLogic.select_cheap_eaters(
                move_eat_list   = split_eating_before_move_model.move_eat_list,
                gymnasium       = gymnasium)
        #select_cheap_eaters_model = select_cheap_eaters_model(move_eat_list = split_eating_before_move_model.move_eat_list)

        # # ロガー
        # for dst_sq, move_list in select_cheap_eaters_model.move_group_by_dst_sq.items():
        #     gymnasium.thinking_logger_module.append(f"D-3a: {Helper.sq_to_masu(dst_sq)=} {MoveListLogics.move_list_map_usi_list(move_list)=}")

        # # ロガー
        # for cheapest_eat_move in select_cheap_eaters_model.cheapest_eat_move_list:
        #     gymnasium.thinking_logger_module.append(f"D-3b: {cshogi.move_to_usi(cheapest_eat_move)=}")

        # ヘルスチェック
        for i in range(0, len(select_cheap_eaters_model.cheapest_eat_move_list)):
            move_eat = select_cheap_eaters_model.cheapest_eat_move_list[i]
            src_sq_obj  = SquareModel(cshogi.move_from(move_eat))   # ［移動元マス］
            src_pc = gymnasium.table.piece(src_sq_obj.sq)           # ［移動元の駒］
            src_pt = cshogi.piece_to_piece_type(src_pc)
            src_value = PieceValuesModel.by_piece_type(pt=src_pt)   # ［取った駒の価値］

            gymnasium.health_check_go_model.append(
                    move    = move_eat,
                    name    = 'cheapest',
                    value   = f"cheapest{PlanetPieceModel.kanji(piece=src_pc, is_gote=gymnasium.table.is_gote)}{src_value}")

        move_list = split_eating_before_move_model.move_not_eat_list
        move_list.extend(select_cheap_eaters_model.cheapest_eat_move_list)

        return move_list
