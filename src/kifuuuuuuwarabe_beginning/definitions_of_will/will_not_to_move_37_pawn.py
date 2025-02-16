import cshogi
import sys

from .. import Mind
from ..sente_perspective import Ban, CshogiBoard, Helper


class WillNotToMove37Pawn():
    """［３七の歩を突かない意志］
    """


    @staticmethod
    def will_on_move(board, move):
        """指し手は［３七の歩を突かない意志］を残しているか？
        """
        ban = Ban(board)
        cboard = CshogiBoard(board)

        src_sq_obj = cboard.sq_obj(cshogi.move_from(move))
        print(f'★ {src_sq_obj.sq=} ', end='')
        print(f'{Helper.sq_to_masu(src_sq_obj.sq)=} ', end='')
        print(f'{board.piece_type(src_sq_obj.sq)=}')


        # ３七以外にある駒は関係ない
        if src_sq_obj.sq != ban.masu(37):
            return Mind.NOT_IN_THIS_CASE

        # 歩でなければ関係ない
        if board.piece_type(src_sq_obj.sq) != cshogi.PAWN:
            return Mind.NOT_IN_THIS_CASE

        # 歩が動くんだったらダメ
        return Mind.WILL_NOT
