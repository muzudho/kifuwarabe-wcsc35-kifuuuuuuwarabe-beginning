import cshogi
import sys

from ..helper import Helper
from ..models import constants, Square
from ..large_board_perspective import Ban, Comparison, Ji
from .match_operation import MatchOperation


class DoNotUpTheDog(MatchOperation):
    """行進［イヌを上げるな］
    ［イヌを９段目に留めておく］意志を含む
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'do_not_up_the_dog',
                label       = 'イヌを上げるな',
                config_doc  = config_doc)


    def do_anything(self, will_play_moves, table):
        if self.is_enabled:

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

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))
        #moved_pt = cshogi.move_from_piece_type(move)

        # イヌ以外は対象外。
        if cshogi.move_from_piece_type(move) != cshogi.GOLD:
            return constants.mind.NOT_IN_THIS_CASE

        # 移動方向が上でなければ対象外。
        if dst_sq_obj.sq != ban.top_of_masu(Helper.sq_to_masu(dst_sq_obj.sq)):
            return constants.mind.NOT_IN_THIS_CASE

        # 右上、または左上にネコがいる。
        if ji.pc(cshogi.SILVER) in [
            table.piece(ban.top_right_of_sq(src_sq_obj.sq)),    # 右上
            table.piece(ban.top_left_of_sq(src_sq_obj.sq))      # 左上
        ]:
            # 順法意志無し
            return constants.mind.WILL_NOT

        # 順法意志有り
        return constants.mind.WILL
