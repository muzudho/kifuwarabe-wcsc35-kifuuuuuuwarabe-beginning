import cshogi
import sys

from ..helper import Helper, Turned


class WillNotToMove37Pawn():
    """３七の歩を突かない意志
    """


    @staticmethod
    def is_there_will_on_move(board, move):
        """指し手は［３七の歩を突かない意志］を残しているか？
        """
        turned = Turned(board)

        src_sq = cshogi.move_from(move)
        src_masu = Helper.sq_to_masu(src_sq)


        # ３七にある駒でなければ関係ない
        if src_masu != turned.masu(37):
            return True

        # 歩でなければ関係ない
        if board.piece_type(src_sq) != cshogi.PAWN:
            return True

        # 歩が動くんだったらダメ
        return False
