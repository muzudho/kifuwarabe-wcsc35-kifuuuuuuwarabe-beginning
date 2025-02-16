import cshogi
import sys

from .. import Mind
from ..sente_perspective import Ban, Helper


class WillNotToMove37Pawn():
    """［３七の歩を突かない意志］
    """


    @staticmethod
    def will_on_move(board, move):
        """指し手は［３七の歩を突かない意志］を残しているか？
        """
        ban = Ban(board)

        src_sq = cshogi.move_from(move)
        src_masu = Helper.sq_to_masu(src_sq)


        # ３七以外にある駒は関係ない
        if ban.masu(src_masu) != ban.masu(37):
            return Mind.NOT_IN_THIS_CASE

        # 歩でなければ関係ない
        if board.piece_type(src_sq) != cshogi.PAWN:
            return Mind.NOT_IN_THIS_CASE

        # 歩が動くんだったらダメ
        return Mind.WILL_NOT
