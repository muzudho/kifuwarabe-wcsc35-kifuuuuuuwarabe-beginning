import cshogi
import sys

from ..models import constants, Square
from ..sente_perspective import Ban, Comparison, Helper, Ji
from .match_operation import MatchOperation


class DoNotMoveRightLance(MatchOperation):
    """行進［右のイノシシは動くな］
    ［右のイノシシは止まる］意志
    """


    def __init__(self):
        super().__init__()
        self._label = '右のイノシシは動くな'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march_operations']['do_not_move_right_lance']:

            ban = Ban(table)
            cmp = Comparison(table)
            ji = Ji(table)

            # 自ライオンが２八にいる
            if table.piece(ban.masu(28)) == ji.pc(cshogi.KING):
                # （処理を行わず）このオブジェクトを除外
                self._is_removed = True
            
            else:
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

        # １筋の駒が動いたら意志無し
        #print(f'★ ＤoNotMoveRightLance.before_move(): {src_sq_obj.file=} {ban.suji(1)=}')
        if src_sq_obj.file == ban.suji(1):
            return constants.mind.WILL_NOT

        # それ以外は意志有り
        return constants.mind.WILL
