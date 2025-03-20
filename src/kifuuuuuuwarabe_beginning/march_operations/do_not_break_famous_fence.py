import cshogi
import sys

from ..helper import Helper
from ..models import constants, Square
from ..large_board_perspective import Ban, Comparison, Ji
from .match_operation import MatchOperation


class DoNotBreakFamousFence(MatchOperation):
    """行進［名の有る囲いを崩すな］
    ［名の有る囲いを保つ］意志
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'do_not_break_famous_fence',
                label       = '名の有る囲いを崩すな',
                config_doc  = config_doc)


    def before_move_o1o1(self, will_play_moves, table):
        if self.is_enabled:

            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = self.before_move(m, table)
                if mind == constants.mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves


    def before_move(self, move, table):
        """指す前に。
        """
        ban = Ban(table)
        #cmp = Comparison(table)
        ji = Ji(table)

        src_sq_obj = Square(cshogi.move_from(move))
        #dst_sq_obj = Square(cshogi.move_to(move))
        #moved_pt = cshogi.move_from_piece_type(move)

        # ［大住囲い］
        if (
                ji.pc(cshogi.KING) == table.piece(ban.masu(38))     # 自ライオンが［３八］
            and ji.pc(cshogi.GOLD) == table.piece(ban.masu(48))     # 自イヌが［４八］
            and ji.pc(cshogi.SILVER) == table.piece(ban.masu(39))   # 自ネコが［３九］
            ):
            if src_sq_obj.sq in [ban.masu(38), ban.masu(48), ban.masu(39)]:
                # 順法の意志無し
                return constants.mind.WILL_NOT

            # 順法の意志有り
            return constants.mind.WILL
        
        # 対象外
        return constants.mind.NOT_IN_THIS_CASE
