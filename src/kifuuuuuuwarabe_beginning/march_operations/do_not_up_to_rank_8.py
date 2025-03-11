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
    def before_move(move, table):
        """指す前に。
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

        # 動かした駒がライオン、イヌ、ネコ、イノシシのいずれかなら
        if moved_pt in [cshogi.KING, cshogi.GOLD, cshogi.SILVER, cshogi.LANCE]:
            # 意志無し
            return Mind.WILL_NOT

        # # 動かした駒が金なら
        # if moved_pt == cshogi.GOLD:
        #     # ５筋以右にある金なら
        #     e1 = cmp.swap(src_sq_obj.file, ban.suji(5))
        #     if e1[0] <= e1[1]:
        #         # 動かしたら意志なし
        #         return Mind.WILL_NOT

        #     # それ以外の金なら、左の方以外に動かしたら意志なし
        #     e1 = cmp.swap(src_sq_obj.file, dst_sq_obj.file)
        #     if e1[0] < e1[1]:
        #         return Mind.WILL_NOT
            
        #     # 左の方に動かしたのなら、まあ、対象外
        #     return Mind.NOT_IN_THIS_CASE

        # # 動かした駒が銀なら
        # if moved_pt == cshogi.SILVER:
        #     # ５筋以右にある銀を動かしたなら
        #     e1 = cmp.swap(src_sq_obj.file, ban.suji(5))
        #     if e1[0] <= e1[1]:
        #         # 意志なし
        #         return Mind.WILL_NOT

        #     # それ以外の銀を、元位置より右の方に動かしたら意志なし
        #     e1 = cmp.swap(src_sq_obj.file, dst_sq_obj.file)
        #     if e1[0] > e1[1]:
        #         return Mind.WILL_NOT
            
        #     # 位左の方に動かしたのなら、まあ、対象外
        #     return Mind.NOT_IN_THIS_CASE

        # それ以外なら意志を残している
        return Mind.WILL


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march']['do_not_up_to_rank_8']:
            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = DoNotUpToRank8.before_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves
