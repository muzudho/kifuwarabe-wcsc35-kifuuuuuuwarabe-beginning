import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper, Ji
from .match_operation import MatchOperation


class DoNotMoveLeftLance(MatchOperation):
    """行進［左のイノシシは動くな］
    ［左のイノシシは止まる］意志
    """


    @staticmethod
    def before_move(move, table):
        """指す前に。
        """

        ban = Ban(table)
        cmp = Comparison(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))

        # いのしし以外なら対象外
        if cshogi.move_from_piece_type(move) not in [cshogi.LANCE]:
            return Mind.NOT_IN_THIS_CASE

        # ９筋の駒が動いたら意志無し
        print(f'★ ＤoNotMoveLeftLance.before_move(): {src_sq_obj.file=} {ban.suji(9)=}')
        if src_sq_obj.file == ban.suji(9):
            return Mind.WILL_NOT

        # それ以外は意志有り
        return Mind.WILL


    def __init__(self):
        super().__init__()
        self._name = '左のイノシシは動くな'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march']['do_not_move_left_lance'] and not self.is_disabled:
            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = DoNotMoveLeftLance.before_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves
