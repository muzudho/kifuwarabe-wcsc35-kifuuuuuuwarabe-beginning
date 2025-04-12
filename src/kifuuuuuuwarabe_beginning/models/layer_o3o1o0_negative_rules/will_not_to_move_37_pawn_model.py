import cshogi

from ..layer_o1o0 import constants, SquareModel
from ..layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from .negative_rule_model import NegativeRuleModel


class WillNotToMove37PawnModel(NegativeRuleModel):
    """［３七の歩を突かない］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'will_not_to_move_37_pawn',
                label       = '３七の歩を突かない',
                basketball_court_model  = basketball_court_model)


    def _before_move_nrm(self, move, table):
        """指し手は［３七の歩を突かない］意志を残しているか？
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        # print(f'★ {src_sq_obj.sq=} ', end='')
        # print(f'{Helper.sq_to_masu(src_sq_obj.sq)=} ', end='')
        # print(f'{table.piece_type(src_sq_obj.sq)=}')

        # ３七以外にある駒は関係ない
        #print(f'D: {Helper.turn_name(table.turn)=} {Helper.sq_to_masu(ban.masu(37))=} {Helper.sq_to_masu(src_sq_obj.sq)=}')
        if src_sq_obj.sq != np.masu(37):
            #print('★ ３七以外にある駒は関係ない')
            return constants.mind.NOT_IN_THIS_CASE

        # 歩でなければ関係ない
        #print(f'D: {table.piece_type(src_sq_obj.sq)=} {cshogi.PAWN=}')
        if table.piece_type(src_sq_obj.sq) != cshogi.PAWN:
            #print('★ 歩でなければ関係ない')
            return constants.mind.NOT_IN_THIS_CASE

        # 歩が動くんだったらダメ
        return constants.mind.WILL_NOT
