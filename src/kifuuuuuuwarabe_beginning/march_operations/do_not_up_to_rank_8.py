import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper, Ji


class DoNotUpToRank8():
    """行進［８段目に上がるな］
    ［飛車道を開ける］意志
    """


    @staticmethod
    def will_before_move(move, table):
        """指し手は［飛車道を開ける］意志を残しているか？
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

        # 移動先は８段目だ
        if dst_sq_obj.rank != ban.dan(8):
            # そうでなければ対象外
            return Mind.NOT_IN_THIS_CASE

        # 動かした駒はキリン以外だ
        if moved_pt == cshogi.ROOK:
            # そうでなければ対象外
            return Mind.NOT_IN_THIS_CASE

        # 動かした駒がライオンかイノシシなら
        if moved_pt in [cshogi.KING, cshogi.LANCE]:
            # 意志無し
            return Mind.WILL_NOT

        # 動かした駒が金なら
        if moved_pt == cshogi.GOLD:
            # ６筋より右にある金なら
            e1 = cmp.swap(src_sq_obj.file, ban.suji(6))
            if e1[0] < e1[1]:
                # 動かしたら意志なし
                return Mind.WILL_NOT

            # ５筋より左にある金なら、左の方以外に動かしたら意志なし
            e1 = cmp.swap(dst_sq_obj.file, ban.suji(6))
            if e1[0] <= e1[1]:
                return Mind.WILL_NOT
            
            # 左の方に動かしたのなら、まあ、対象外
            return Mind.NOT_IN_THIS_CASE

        # 動かした駒が銀なら
        if moved_pt == cshogi.SILVER:
            # ６筋以右にある銀を動かしたなら
            e1 = cmp.swap(src_sq_obj.file, ban.suji(6))
            if e1[0] <= e1[1]:
                # 意志なし
                return Mind.WILL_NOT

            # ７筋以左にある銀を、元位置より右の方に動かしたら意志なし
            e1 = cmp.swap(src_sq_obj.file, dst_sq_obj.file)
            if e1[0] > e1[1]:
                return Mind.WILL_NOT
            
            # 位左の方に動かしたのなら、まあ、対象外
            return Mind.NOT_IN_THIS_CASE

        # それ以外なら意志を残している
        return Mind.WILL
