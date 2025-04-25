import cshogi

from ...layer_o1o0 import constants, PieceModel, PieceTypeModel, SquareModel
from ...layer_o1o0o_9o0_table_helper import TableHelper
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotPeckAtChickOnRoundheadedPieceModel(NegativeRuleModel):
    """号令［頭が丸い駒の頭のヒヨコを突くな］
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_peck_at_chick_on_roundheaded_piece',
                label       = '頭が丸い駒の頭のヒヨコを突くな',
                basketball_court_model  = basketball_court_model)


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)
        moving_pt = TableHelper.get_moving_pt_from_move(move)
        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))
        is_drop = cshogi.move_is_drop(move) # ［打］
        moving_pc = table.piece(src_sq_obj.sq)
        moving_color = PieceModel.turn(moving_pc)

        if is_drop:                                 # 打なら。
            print(f"{cshogi.move_to_usi(move)} is 打。")
            return constants.mind.NOT_IN_THIS_CASE  # 対象外。
        
        if moving_pt != cshogi.PAWN:                # 歩でないなら。
            print(f"{cshogi.move_to_usi(move)} is not 歩。")
            return constants.mind.NOT_IN_THIS_CASE  # 対象外。
        
        if moving_color == cshogi.WHITE:
            print(f"{cshogi.move_to_usi(move)} is 後手。")
            south_of_src_sq_obj = src_sq_obj.to_north()
        else:
            print(f"{cshogi.move_to_usi(move)} is 先手。")
            south_of_src_sq_obj = src_sq_obj.to_south()

        south_of_src_pt = table.piece_type(south_of_src_sq_obj.sq)
        print(f"{cshogi.move_to_usi(move)}'s south is {PieceTypeModel.kanji(south_of_src_pt)}。")
        if south_of_src_pt not in [cshogi.BISHOP, cshogi.KNIGHT]:   # 移動元の１段下の駒がゾウ、ウサギでないなら。
            return constants.mind.NOT_IN_THIS_CASE                  # 対象外。

        # それ以外なら、意志無し
        return constants.mind.WILL_NOT
