import cshogi
import sys

from ..models import constants, Square
from ..sente_perspective import Ban, Comparison, Helper, Ji
from .match_operation import MatchOperation


class DoNotUpToRank6(MatchOperation):
    """行進［６段目に上がるな］
    ［玉が２八に行くまで歩を突かない］意志
    """


    def __init__(self):
        super().__init__()
        self._id = 'do_not_up_to_rank_6'
        self._label = '６段目に上がるな'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march_operations'][self._id]:

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
                mind = self.before_move(m, table)
                if mind == constants.mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves


    def before_move(self, move, table):
        """指す前に。
        """
        ban = Ban(table)
        #cmp = Comparison(table)
        ji = Ji(table)

        #src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))
        #moved_pt = cshogi.move_from_piece_type(move)

        # # 自キリンが２八にいる
        # if table.piece(ban.masu(28)) != ji.pc(cshogi.ROOK):
        #     # そうでなければ対象外
        #     return constants.mind.NOT_IN_THIS_CASE

        # 移動先は６段目だ
        if dst_sq_obj.rank != ban.dan(6):
            # そうでなければ意志を残している
            return constants.mind.WILL

        # 意志なし
        return constants.mind.WILL_NOT
