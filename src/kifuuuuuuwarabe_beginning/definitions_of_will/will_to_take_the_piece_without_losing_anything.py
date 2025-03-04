import cshogi
import sys

from .. import Mind
from ..models import Masu, Piece, PieceType, Square
from ..sente_perspective import Ban, Helper, Ji


class WillToTakeThePieceWithoutLosingAnything():
    """［駒取って損しない意志］
    """

    @staticmethod
    def will_move(move, table):
        """指し手は［駒取って損しない意志］を残しているか？
        """

        # 動かした駒の種類
        pt = cshogi.move_from_piece_type(move)
        #print(f'★ will_to_take_the_piece_without_losing_anything.will_move: {PieceType.kanji(pt)=}')

        # 動かした駒が角以外なら対象外
        if pt != cshogi.BISHOP:
            return Mind.NOT_IN_THIS_CASE

        # 歩を取るだろう位置
        dst_sq = cshogi.move_to(move)

        # そこに駒はあるか？
        cap = table.piece(dst_sq)
        #print(f'★ will_to_take_the_piece_without_losing_anything.will_move: {Piece.kanji(cap)=}')

        # 取った駒が無ければ、対象外
        if cap == cshogi.NONE:
            return Mind.NOT_IN_THIS_CASE

        cap_type = cshogi.piece_to_piece_type(cap)
        #print(f'★ will_to_take_the_piece_without_losing_anything.will_move: {PieceType.kanji(cap_type)=}')

        # 取った駒が歩以外なら対象外
        if cap_type != cshogi.PAWN:
            return Mind.NOT_IN_THIS_CASE
        

        table.push(move)   # １手指す

        mind = WillToTakeThePieceWithoutLosingAnything.will_after_move(
                move=move,
                cap_sq=dst_sq,
                cap_type=cap_type,
                table=table)

        table.pop() # １手戻す

        return mind


    @staticmethod
    def will_after_move(move, cap_sq, cap_type, table):
        """
        Parameters
        ----------
        cap_type : int
            取った駒の種類
        """

        # NOTE 指した後は相手の番になっていることに注意
        ban = Ban(table, after_moving=True)
        ji = Ji(table, after_moving=True)


        # TODO 角が取り返される危険性のチェック

        # 歩を取った位置
        cap_masu = Helper.sq_to_masu(cap_sq)

        # 先手が角で１三歩を取ったと想定し、左上を調べていって最初に敵の角が出てきたら、取ったら損。

        # 後手視点だと、左上は右下
        bottom_right_sq = ban.bottom_right(cap_masu)
        if not bottom_right_sq:
            return Mind.WILL_NOT

        # 敵角があるか？
        pc2 = table.piece(bottom_right_sq)
        pt2 = cshogi.piece_to_piece_type(pc2)

        if table.turn == Piece.turn(pc2):
            if pt2 == cshogi.BISHOP:
                # 角で取り返される。意志なし
                return Mind.WILL_NOT

        # TODO 他のパターンも作ること

        # 意志あり
        return Mind.WILL

