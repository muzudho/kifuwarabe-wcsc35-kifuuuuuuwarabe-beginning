import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotDepromotionModel(NegativeRuleModel):
    """号令［成らないということをするな］
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_depromotion_model',
                label       = '成らないということをするな',
                basketball_court_model  = basketball_court_model)

        self._promotion_doc = None


    def _before_branches_nrm(self, table):
        """枝前に。
        """

        # 枝前処理で、［成る手］の一覧を作る。
        # {
        #   移動元：［移動先］
        # }
        self._promotion_doc = {}

        for move in list(table.legal_moves):
            is_promotion = cshogi.move_is_promotion(move)
            if not is_promotion:
                continue

            src_sq_obj = SquareModel(cshogi.move_from(move))
            dst_sq_obj = SquareModel(cshogi.move_to(move))
            
            if src_sq_obj.sq not in self._promotion_doc:
                self._promotion_doc[src_sq_obj.sq] = []
            
            if dst_sq_obj.sq not in self._promotion_doc[src_sq_obj.sq]:
                self._promotion_doc[src_sq_obj.sq].append(dst_sq_obj.sq)


    def _before_move_nrm(self, move, table):
        """指す前に。
        """

        # ［成る手］は意志有り。
        is_promotion = cshogi.move_is_promotion(move)
        if is_promotion:
            return constants.mind.WILL

        # ネコは対象外（成らない手も良い手）
        if cshogi.move_from_piece_type(move) == cshogi.SILVER:
            return constants.mind.NOT_IN_THIS_CASE

        np = NineRankSidePerspectiveModel(table)
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # ウサギは３段目なら対象外（成らない手も良い手）
        if cshogi.move_from_piece_type(move) == cshogi.KNIGHT and dst_sq_obj.rank == np.dan(3):
            return constants.mind.NOT_IN_THIS_CASE

        # イノシシは３段目なら対象外（成らない手も良い手）
        if cshogi.move_from_piece_type(move) == cshogi.LANCE and dst_sq_obj.rank == np.dan(3):
            return constants.mind.NOT_IN_THIS_CASE

        # （成る手があるのに）［成らない手］なら意志無し。
        src_sq_obj = SquareModel(cshogi.move_from(move))
        if src_sq_obj.sq in self._promotion_doc:
            if dst_sq_obj.sq in self._promotion_doc[src_sq_obj.sq]:
                return constants.mind.WILL_NOT

        # 対象外
        return constants.mind.NOT_IN_THIS_CASE
