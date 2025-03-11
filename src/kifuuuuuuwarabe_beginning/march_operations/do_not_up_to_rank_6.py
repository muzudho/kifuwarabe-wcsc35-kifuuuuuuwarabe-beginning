import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper, Ji


class DoNotUpToRank6():
    """行進［６段目に上がるな］
    ［飛車を振るまで歩を突かない］意志
    """


    @staticmethod
    def before_move(move, table):
        """指す前に。
        """
        ban = Ban(table)
        cmp = Comparison(table)
        ji = Ji(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))
        moved_pt = cshogi.move_from_piece_type(move)

        # キリンが２八にいる
        if table.piece(ban.masu(28)) != ji.pc(cshogi.ROOK):
            # そうでなければ対象外
            return Mind.NOT_IN_THIS_CASE

        # 移動先は６段目だ
        if dst_sq_obj.rank != ban.dan(6):
            # そうでなければ意志を残している
            return Mind.WILL

        # 意志なし
        return Mind.WILL_NOT
