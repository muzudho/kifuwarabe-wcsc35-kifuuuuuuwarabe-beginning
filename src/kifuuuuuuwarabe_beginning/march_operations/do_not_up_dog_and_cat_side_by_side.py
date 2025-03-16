import cshogi
import sys

from ..helper import Helper
from ..models import constants, Square
from ..large_board_perspective import Ban, Comparison, Ji
from .match_operation import MatchOperation


class DoNotDogAndCatSideBySide(MatchOperation):
    """行進［イヌとネコを横並びに上げるな］
    ［イヌを９段目に留めておく］意志を含む
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'do_not_up_dog_and_cat_side_by_side',
                label       = 'イヌとネコを横並びに上げるな',
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

        def _do_not_alice_and_bob_side_by_side(alice, bob):
            # アリスなら。
            if cshogi.move_from_piece_type(move) == alice:
                # 移動方向が上でなければ対象外。
                if dst_sq_obj.sq != ban.top_of_masu(Helper.sq_to_masu(dst_sq_obj.sq)):
                    return constants.mind.NOT_IN_THIS_CASE

                # 右上、または左上にボブがいる。
                if ji.pc(bob) in [
                    table.piece(ban.top_right_of_sq(src_sq_obj.sq)),    # 右上
                    table.piece(ban.top_left_of_sq(src_sq_obj.sq))      # 左上
                ]:
                    # 順法意志無し
                    return constants.mind.WILL_NOT

            return None

        # イヌなら。
        result = _do_not_alice_and_bob_side_by_side(
                alice   = cshogi.GOLD,
                bob     = cshogi.SILVER)
        if result is None:
            return result

        # ネコなら。
        result = _do_not_alice_and_bob_side_by_side(
                alice   = cshogi.SILVER,
                bob     = cshogi.GOLD)
        if result is None:
            return result

        # 順法意志有り
        return constants.mind.WILL
