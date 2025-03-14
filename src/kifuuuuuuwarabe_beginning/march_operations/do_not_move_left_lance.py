import cshogi
import sys

from ..models import constants, Square
from ..sente_perspective import Ban, Comparison, Helper, Ji
from .match_operation import MatchOperation


class DoNotMoveLeftLance(MatchOperation):
    """行進［左のイノシシは動くな］
    ［左のイノシシは止まる］意志
    """


    def __init__(self):
        super().__init__()
        self._label = '左のイノシシは動くな'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march_operations']['do_not_move_left_lance']:
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
        cmp = Comparison(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))

        # いのしし以外なら対象外
        if cshogi.move_from_piece_type(move) not in [cshogi.LANCE]:
            return constants.mind.NOT_IN_THIS_CASE

        # ９筋の駒が動いたら意志無し
        #print(f'★ ＤoNotMoveLeftLance.before_move(): {src_sq_obj.file=} {ban.suji(9)=}')
        if src_sq_obj.file == ban.suji(9):
            return constants.mind.WILL_NOT

        # それ以外は意志有り
        return constants.mind.WILL
