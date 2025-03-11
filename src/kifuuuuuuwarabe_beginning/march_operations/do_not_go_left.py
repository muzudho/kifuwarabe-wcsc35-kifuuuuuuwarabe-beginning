import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper


class DoNotGoLeft():
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
