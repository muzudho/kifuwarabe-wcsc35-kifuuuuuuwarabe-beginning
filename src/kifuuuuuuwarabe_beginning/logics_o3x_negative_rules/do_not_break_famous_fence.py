import cshogi

from ..models_o1x import constants, Square
from ..models_o2x.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from .negative_rule import NegativeRule


class DoNotBreakFamousFence(NegativeRule):
    """行進［名の有る囲いを崩すな］
    ［名の有る囲いを保つ］意志
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'do_not_break_famous_fence',
                label       = '名の有る囲いを崩すな',
                config_doc  = config_doc)


    def before_move_o1o1x(self, remaining_moves, table):
        if self.is_enabled:

            for i in range(len(remaining_moves))[::-1]:     # `[::-1]` - 逆順
                m = remaining_moves[i]
                mind = self.before_move(m, table)
                if mind == constants.mind.WILL_NOT:
                    del remaining_moves[i]

        return remaining_moves


    def before_move(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = Square(cshogi.move_from(move))

        # ［大住囲い］
        if (
                np.ji_pc(cshogi.KING) == table.piece(np.masu(38))     # 自ライオンが［３八］
            and np.ji_pc(cshogi.GOLD) == table.piece(np.masu(48))     # 自イヌが［４八］
            and np.ji_pc(cshogi.SILVER) == table.piece(np.masu(39))   # 自ネコが［３九］
            ):
            if src_sq_obj.sq in [np.masu(38), np.masu(48), np.masu(39)]:
                # 順法の意志無し
                return constants.mind.WILL_NOT

            # 順法の意志有り
            return constants.mind.WILL
        
        # 対象外
        return constants.mind.NOT_IN_THIS_CASE
