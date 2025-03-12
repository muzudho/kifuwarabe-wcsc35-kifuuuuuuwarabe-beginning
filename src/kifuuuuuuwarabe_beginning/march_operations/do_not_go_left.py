import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper
from .match_operation import MatchOperation


class DoNotGoLeft(MatchOperation):
    """行進［左へ行くな］
    ［右へ行く］意志
    """


    @staticmethod
    def before_move(move, table):
        """指す前に。
        """

        ban = Ban(table)
        cmp = Comparison(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))

        # ライオン、イヌ、ネコ以外なら対象外
        if cshogi.move_from_piece_type(move) not in [cshogi.KING, cshogi.GOLD, cshogi.SILVER]:
            return Mind.NOT_IN_THIS_CASE

        # ６筋位左にある駒は対象外
        e1 = cmp.swap(src_sq_obj.file, ban.suji(6))
        if e1[0] >= e1[1]:
            return Mind.NOT_IN_THIS_CASE

        # 移動先が同筋位右なら意志あり
        e1 = cmp.swap(dst_sq_obj.file, src_sq_obj.file)
        if e1[0] <= e1[1]:
            return Mind.WILL

        # それ以外は意志なし
        return Mind.WILL_NOT


    def __init__(self):
        super().__init__()
        self._name = '左へ行くな'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march']['do_not_go_left']:
            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = DoNotGoLeft.before_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves
