import cshogi

from ..layer_o1o0 import constants, SquareModel
from ..layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from .negative_rule_model import NegativeRuleModel


class WillSwingingRookModel(NegativeRuleModel):
    """［振り飛車をする］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'will_swinging_rook',
                label       = '振り飛車をする',
                basketball_court_model  = basketball_court_model)


    def _skip_step_before_branches_nrm(self, remaining_moves, table):
        """枝前スキップ条件。
        真なら、枝前ステップではこのルールをスキップします。
        """
        return constants.mind.WILL != self.will_on_board(table)


    def _before_move_nrm(self, move, table):
        """指し手は［振り飛車をする］意志を残しているか？
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # 玉
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            # 飛車が２八にいるか？
            if table.piece(np.masu(28)) == np.ji_pc(cshogi.ROOK):
                # この駒は動いてはいけない
                return constants.mind.WILL_NOT

            #print(f'★ will_on_move: 玉', file=sys.stderr)            
            # 元位置位右に移動するなら、意志あり
            e1 = np.swap(dst_sq_obj.file, src_sq_obj.file)
            if e1[0] <= e1[1]:
                return constants.mind.WILL
            
            return constants.mind.WILL_NOT

        # 飛
        if cshogi.move_from_piece_type(move) == cshogi.ROOK:
            k_sq_obj = SquareModel(table.king_square(table.turn))
            # 飛車は４筋より左に振る。かつ、玉と同じ筋または玉より左の筋に振る
            e1 = np.swap(dst_sq_obj.file, np.suji(4))
            e2 = np.swap(dst_sq_obj.file, k_sq_obj.file)

            if e1[0] > e1[1] and e2[0] >= e2[1]:
                return constants.mind.WILL
            
            return constants.mind.WILL_NOT

        return constants.mind.NOT_IN_THIS_CASE


    def will_on_board(self, table):
        """盤は［振り飛車をする］意志を残しているか？

        ４０手目までは振り飛車の意志を残しているとします。
        ４１手目以降は振り飛車の意志はありません
        """
        #print(f'★ is_there_will_on_board: {table.move_number=}', file=sys.stderr)
        if table.move_number < 41:
            return constants.mind.WILL
        
        return constants.mind.WILL_NOT
