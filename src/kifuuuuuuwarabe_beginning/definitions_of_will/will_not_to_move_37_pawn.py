import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Helper


class WillNotToMove37Pawn():
    """［３七の歩を突かない意志］
    """


    @staticmethod
    def will_on_move(board, move):
        """指し手は［３七の歩を突かない意志］を残しているか？
        """
        ban = Ban(board)

        src_sq_obj = Square(cshogi.move_from(move))
        # print(f'★ {src_sq_obj.sq=} ', end='')
        # print(f'{Helper.sq_to_masu(src_sq_obj.sq)=} ', end='')
        # print(f'{board.piece_type(src_sq_obj.sq)=}')


        # ３七以外にある駒は関係ない
        print(f'D: {Helper.turn_name(board.turn)=} {Helper.sq_to_masu(ban.masu(37))=} {Helper.sq_to_masu(src_sq_obj.sq)=}')
        if src_sq_obj.sq != ban.masu(37):
            #print('★ ３七以外にある駒は関係ない')
            return Mind.NOT_IN_THIS_CASE

        # 歩でなければ関係ない
        print(f'D: {board.piece_type(src_sq_obj.sq)=} {cshogi.PAWN=}')
        if board.piece_type(src_sq_obj.sq) != cshogi.PAWN:
            #print('★ 歩でなければ関係ない')
            return Mind.NOT_IN_THIS_CASE

        # 歩が動くんだったらダメ
        return Mind.WILL_NOT
