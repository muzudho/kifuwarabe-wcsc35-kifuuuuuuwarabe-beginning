import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper, Ji
from .match_operation import MatchOperation


class DoNotUpToRank6(MatchOperation):
    """行進［６段目に上がるな］
    ［玉が２八に行くまで歩を突かない］意志
    """


    @staticmethod
    def before_move(move, table):
        """指す前に。
        """
        ban = Ban(table)
        #cmp = Comparison(table)
        ji = Ji(table)

        #src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))
        #moved_pt = cshogi.move_from_piece_type(move)

        # 自キリンが２八にいる
        if table.piece(ban.masu(28)) != ji.pc(cshogi.ROOK):
            # そうでなければ対象外
            return Mind.NOT_IN_THIS_CASE

        # 移動先は６段目だ
        if dst_sq_obj.rank != ban.dan(6):
            # そうでなければ意志を残している
            return Mind.WILL

        # 意志なし
        return Mind.WILL_NOT


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march']['do_not_up_to_rank_6']:

            ban = Ban(table)
            #cmp = Comparison(table)
            ji = Ji(table)

            # 自ライオンが２八にいる
            if table.piece(ban.masu(28)) == ji.pc(cshogi.KING):
                # このオブジェクトを除外
                self._is_removed = True

                # 対象外
                return will_play_moves

            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = DoNotUpToRank6.before_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves
