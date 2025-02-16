import cshogi
import sys

from .. import Mind
from ..sente_perspective import Ban, Comparison, Helper, Turned, Ji


class WillToClearWayOfRook():
    """［飛車道を開ける意志］
    """


    @staticmethod
    def will_on_move(board, move):
        """指し手は［飛車道を開ける意志］を残しているか？
        """
        ban = Ban(board)
        cmp = Comparison(board)
        ji = Ji(board)
        turned = Turned(board)

        src_sq = cshogi.move_from(move)
        dst_sq = cshogi.move_to(move)
        moved_pt = cshogi.move_from_piece_type(move)


        # 飛車が２八にいなければ対象外
        if board.piece(ban.masu(28)) != ji.pc(cshogi.ROOK):
            return Mind.NOT_IN_THIS_CASE


        # 動かした駒が飛なら対象外
        if moved_pt == cshogi.ROOK:
            return Mind.NOT_IN_THIS_CASE


        # 動かした駒が玉なら
        if moved_pt == cshogi.KING:
            # 玉が８段目に上がったら、意志無し
            if turned.suji(Helper.sq_to_suji(dst_sq)) == turned.suji(8):
                return Mind.WILL_NOT


        # 動かした駒が金なら
        if moved_pt == cshogi.GOLD:
            # 移動先が９段目なら、意志を残している
            if Helper.sq_to_dan(dst_sq) == turned.dan(9):
                return Mind.WILL

            # ６筋より右にある金なら
            op = cmp.swap(Helper.sq_to_suji(src_sq), turned.suji(6))
            if op[0] < op[1]:
                # 動かしたら意志なし
                return Mind.WILL_NOT

            # ５筋より左にある金なら、左の方以外に動かしたら意志なし
            op = cmp.swap(Helper.sq_to_suji(dst_sq), turned.suji(6))
            if op[0] <= op[1]:
                return Mind.WILL_NOT
            
            # 左の方に動かしたのなら、まあ、対象外
            return Mind.NOT_IN_THIS_CASE


        # 動かした駒が銀なら
        if cshogi.move_from_piece_type(move) == cshogi.SILVER:
            # ６筋以右にある銀を動かしたなら
            op = cmp.swap(Helper.sq_to_suji(src_sq), turned.suji(6))
            if op[0] <= op[1]:
                # 意志なし
                return Mind.WILL_NOT

            # ７筋以左にある銀を、元位置より右の方に動かしたら意志なし
            op = cmp.swap(Helper.sq_to_suji(src_sq), Helper.sq_to_suji(dst_sq))
            if op[0] > op[1]:
                return Mind.WILL_NOT
            
            # 位左の方に動かしたのなら、まあ、対象外
            return Mind.NOT_IN_THIS_CASE


        # それ以外なら意志を残している
        return Mind.WILL
