import cshogi

from ..models_level_1 import constants, Square
from ..models_level_2.nine_rank_side_perspective import Ban, Comparison
from .match_operation import MatchOperation


class DoNotMoveLeftLance(MatchOperation):
    """行進［左のイノシシは動くな］
    ［左のイノシシは止まる］意志
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'do_not_move_left_lance',
                label       = '左のイノシシは動くな',
                config_doc  = config_doc)


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
