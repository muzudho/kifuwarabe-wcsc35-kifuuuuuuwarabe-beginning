import cshogi

from ..logics_o1x.helper import Helper
from ..models_o1x import constants, SquareModel
from ..models_o2x.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from .negative_rule_model import NegativeRuleModel


class WillForThreeGoldAndSilverCoinsToGatherToTheRightModel(NegativeRuleModel):
    """［金銀３枚が右に集まる］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'will_for_three_gold_and_silver_coins_to_gather_to_the_right',
                label       = '金銀３枚が右に集まる',
                basketball_court_model  = basketball_court_model)


    def before_move(self, move, table):
        """指す前に。

        先手から見て５筋と６筋の間にドアがあるとする。
        ５筋位左にある金銀が左へ移動するとき、６筋位左に自駒の金銀が０枚である場合のみ移動できる。
        """

        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # ４筋位右にある駒は対象外
        e1 = np.swap(src_sq_obj.file, np.suji(4))
        if e1[0] <= e1[1]:
            return constants.mind.NOT_IN_THIS_CASE

        # 移動先が同筋位右なら対象外
        e1 = np.swap(dst_sq_obj.file, src_sq_obj.file)
        if e1[0] <= e1[1]:
            return constants.mind.NOT_IN_THIS_CASE

        # 36マスをスキャンする
        left_from_6_suji = [Helper.file_rank_to_sq(file, rank) for file in np.suji_range(6, 10)
            for rank in np.dan_range(1, 10)]
        #print(f'{len(left_from_6_suji)=} {left_from_6_suji=}')

        count = 0

        for sq in left_from_6_suji:
            pc = table.piece(sq)

            pt = cshogi.piece_to_piece_type(pc)
            if pt not in [cshogi.GOLD, cshogi.SILVER]:
                continue

            if pc <= 16:
                color = cshogi.BLACK
            else:
                color = cshogi.WHITE

            if table.turn != color:
                continue

            count += 1

        if count == 0:
            return constants.mind.WILL

        return constants.mind.WILL_NOT
