import cshogi
import sys

from .. import Mind
from ..models import Piece, PieceType
from ..sente_perspective import Ban, Helper, Ji


class WillToTakeThePieceWithoutLosingAnything():
    """［駒取って損しない意志］
    """

    @staticmethod
    def will_after_move(move, board):
        """指し手は［駒取って損しない意志］を残しているか？
        """

        # NOTE 指した後は相手の番になっていることに注意
        ban = Ban(board, after_moving=True)
        ji = Ji(board, after_moving=True)

        # 動かした駒の種類
        pt = cshogi.move_from_piece_type(move)
        print(f'★ will_to_take_the_piece_without_losing_anything.will_after_move: {PieceType.kanji(pt)=}')

        # 動かした駒が角以外なら対象外
        if pt != cshogi.BISHOP:
            return Mind.NOT_IN_THIS_CASE

        # 取った駒
        cap = cshogi.move_cap(move)
        print(f'★ will_to_take_the_piece_without_losing_anything.will_after_move: {Piece.kanji(cap)=}')

        # 取った駒が無ければ、対象外
        if cap == cshogi.NONE:
            return Mind.NOT_IN_THIS_CASE

        cap_type = cshogi.piece_to_piece_type(cap)
        print(f'★ will_to_take_the_piece_without_losing_anything.will_after_move: {PieceType.kanji(cap_type)=}')

        # 取った駒が歩以外なら対象外
        if cap_type != cshogi.PAWN:
            return Mind.NOT_IN_THIS_CASE

        # TODO 角が取り返される危険性のチェック

        # 意志なし
        return Mind.WILL_NOT
