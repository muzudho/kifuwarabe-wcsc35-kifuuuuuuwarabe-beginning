import cshogi
import sys

from ..models import constants, Square
from ..sente_perspective import Ban, Comparison, Helper
from .match_operation import MatchOperation


class DoNotGoLeft(MatchOperation):
    """行進［左へ行くな］
    ［右へ行く］意志
    """


    def __init__(self):
        super().__init__()
        self._name = '左へ行くな'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march_operations']['do_not_go_left']:
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

        # ライオンなら、以左には行くな。
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            # 移動先が右なら意志あり
            e1 = cmp.swap(dst_sq_obj.file, src_sq_obj.file)
            if e1[0] < e1[1]:
                return constants.mind.WILL

            # それ以外は意志なし
            return constants.mind.WILL_NOT

        # イヌ、ネコなら
        if cshogi.move_from_piece_type(move) in [cshogi.GOLD, cshogi.SILVER]:
            # ６筋位左にある駒は対象外
            e1 = cmp.swap(src_sq_obj.file, ban.suji(6))
            if e1[0] >= e1[1]:
                return constants.mind.NOT_IN_THIS_CASE

            # 移動先が同筋位右なら意志あり
            e1 = cmp.swap(dst_sq_obj.file, src_sq_obj.file)
            if e1[0] <= e1[1]:
                return constants.mind.WILL

            # それ以外は意志なし
            return constants.mind.WILL_NOT

        # それ以外なら対象外
        return constants.mind.NOT_IN_THIS_CASE
