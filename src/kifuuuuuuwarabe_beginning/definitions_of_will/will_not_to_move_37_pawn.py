import cshogi
import sys

from ..helper import Turned, Helper


class WillNotToMove37Pawn():
    """３七の歩を突かない意志
    """


    @staticmethod
    def is_there_will_on_move(board, move):
        """指し手は［３七の歩を突かない意志］を残しているか？

        FIXME 先手視点でのみ実装しています。後手視点にも対応したい
        """
        src_sq = cshogi.move_from(move)
        src_masu = Helper.sq_to_masu(src_sq)

        turned = Turned(board)

        # ３七にある駒でなければ関係ない
        if src_masu != turned.masu(37):
            return True

        # 歩でなければ関係ない
        if board.piece_type(src_sq) != cshogi.PAWN:
            return True

        # 歩が動くんだったらダメ
        return False
