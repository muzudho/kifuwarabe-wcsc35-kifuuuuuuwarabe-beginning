import cshogi
import sys

from .. import Mind
from ..sente_perspective import Ban, CshogiBoard, Comparison, Helper, Ji


class WillToClearWayOfRook():
    """［飛車道を開ける意志］
    """


    @staticmethod
    def will_on_move(board, move):
        """指し手は［飛車道を開ける意志］を残しているか？
        """
        ban = Ban(board)
        cboard = CshogiBoard(board)
        cmp = Comparison(board)
        ji = Ji(board)

        src_sq_obj = cboard.sq_obj(cshogi.move_from(move))
        dst_sq_obj = cboard.sq_obj(cshogi.move_to(move))
        moved_pt = cshogi.move_from_piece_type(move)


        # 飛車が２八にいなければ、対象外
        if board.piece(ban.masu(28)) != ji.pc(cshogi.ROOK):
            return Mind.NOT_IN_THIS_CASE


        # 移動先が８段目以外なら、対象外
        if dst_sq_obj.to_rank() != ban.dan(8):
            return Mind.NOT_IN_THIS_CASE


        # 動かした駒が飛なら対象外
        if moved_pt == cshogi.ROOK:
            return Mind.NOT_IN_THIS_CASE


        # 動かした駒が玉なら
        if moved_pt == cshogi.KING:
            # 意志無し
            return Mind.WILL


        # 動かした駒が金なら
        if moved_pt == cshogi.GOLD:
            # ６筋より右にある金なら
            op = cmp.swap(src_sq_obj.to_file(), ban.suji(6))
            if op[0] < op[1]:
                # 動かしたら意志なし
                return Mind.WILL_NOT

            # ５筋より左にある金なら、左の方以外に動かしたら意志なし
            op = cmp.swap(dst_sq_obj.to_file(), ban.suji(6))
            if op[0] <= op[1]:
                return Mind.WILL_NOT
            
            # 左の方に動かしたのなら、まあ、対象外
            return Mind.NOT_IN_THIS_CASE


        # 動かした駒が銀なら
        if moved_pt == cshogi.SILVER:
            # ６筋以右にある銀を動かしたなら
            op = cmp.swap(src_sq_obj.to_file(), ban.suji(6))
            if op[0] <= op[1]:
                # 意志なし
                return Mind.WILL_NOT

            # ７筋以左にある銀を、元位置より右の方に動かしたら意志なし
            op = cmp.swap(src_sq_obj.to_file(), dst_sq_obj.to_file())
            if op[0] > op[1]:
                return Mind.WILL_NOT
            
            # 位左の方に動かしたのなら、まあ、対象外
            return Mind.NOT_IN_THIS_CASE


        # それ以外なら意志を残している
        return Mind.WILL
