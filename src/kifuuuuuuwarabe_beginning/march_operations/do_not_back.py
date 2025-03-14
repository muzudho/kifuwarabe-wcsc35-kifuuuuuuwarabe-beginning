import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper
from .match_operation import MatchOperation


class DoNotBack(MatchOperation):
    """行進［戻るな］
    ［常に進む］意志
    """


    @staticmethod
    def before_move(move, table):
        """指す前に。
        """

        ban = Ban(table)
        cmp = Comparison(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))

        # TODO 直近の指し手を調べる。
        # TODO 元居た位置に戻る手は、意志無し。

        # それ以外なら対象外
        return Mind.NOT_IN_THIS_CASE



    def __init__(self):
        super().__init__()
        self._name = '戻るな'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march']['do_not_back']:
            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = DoNotBack.before_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves
