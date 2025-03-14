import cshogi
import sys

from .. import Mind
from ..models import constants, Square
from ..sente_perspective import Ban, Comparison, Helper
from .match_operation import MatchOperation


class DoNotBack(MatchOperation):
    """行進［戻るな］
    ［常に進む］意志
    """


    def __init__(self):
        super().__init__()
        self._name = '戻るな'

        # 元の位置。該当がなければナンです。
        self._back_board = [None] * constants.BOARD_AREA


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march_operations']['do_not_back']:
            for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                m = will_play_moves[i]
                mind = self.before_move(m, table)
                if mind == Mind.WILL_NOT:
                    del will_play_moves[i]

        return will_play_moves


    def before_move(self, move, table):
        """指す前に。
        """

        ban = Ban(table)
        cmp = Comparison(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))

        # 動かす駒は、現在のマスに移動する前はどこに居たか調べます。
        try:
            most_recent_src_sq = self._back_board[src_sq_obj.sq]
        except IndexError:
            print(f'ERROR: {src_sq_obj.sq=}', file=sys.stderr)
            raise

        if most_recent_src_sq in [None, constants.PIECE_STAND_SQ]:
            # 動いていない、または、駒台にあったなら、対象外
            return Mind.NOT_IN_THIS_CASE

        # 元居た位置に戻る手は、意志無し。
        if dst_sq_obj.sq == most_recent_src_sq:
            return Mind.WILL_NOT

        # それ以外なら、意志有り。
        return Mind.WILL


    def on_best_move_played(self, move, table, config_doc):
        """指す手の確定時。
        """

        if config_doc['march_operations']['do_not_back']:
            ban = Ban(table)
            cmp = Comparison(table)

            src_sq_obj = Square(cshogi.move_from(move))
            dst_sq_obj = Square(cshogi.move_to(move))
            is_drop = cshogi.move_is_drop(move)

            # 戻れない駒は対象外。
            if cshogi.move_from_piece_type(move) not in [cshogi.KNIGHT, cshogi.LANCE, cshogi.PAWN]:
                return

            # 移動先のマス番号
            if is_drop: # 打のとき。                
                dst_sq = constants.PIECE_STAND_SQ
            else:
                dst_sq = dst_sq_obj.sq

            # 移動元のマス番号
            src_sq = src_sq_obj.sq

            # 記憶
            self._back_board[dst_sq] = src_sq
            self._back_board[src_sq] = None
