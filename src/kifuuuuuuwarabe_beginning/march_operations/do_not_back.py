import cshogi
import sys

from ..helper import Helper
from ..models import constants, Square
from ..large_board_perspective import Ban, Comparison
from .match_operation import MatchOperation


class DoNotBack(MatchOperation):
    """行進［戻るな］
    ［常に進む］意志
    """


    def __init__(self, config_doc):
        super().__init__(
                id          = 'do_not_back',
                label       = '戻るな',
                config_doc  = config_doc)

        #print(f'★ ＤoNotBack: back_board 生成')
        # 元の位置。該当がなければナンです。
        # NOTE 自分が指し手を送信した手しか記憶していません。
        self._back_board = [None] * constants.BOARD_AREA


    def before_move(self, move, table):
        """指す前に。
        """

        ban = Ban(table)
        cmp = Comparison(table)

        is_drop = cshogi.move_is_drop(move)
        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))

        if is_drop: # 打のとき
            back_sq = constants.PIECE_STAND_SQ
        
        else:
            # 動かす駒は、現在のマスに移動する前はどこに居たか調べます。
            try:
                back_sq = self._back_board[src_sq_obj.sq]
            except:
                # NOTE 角打だと 89 が返ってくる？
                print(f'ERROR1: {src_sq_obj.sq=}')
                #print(f'ERROR2: {src_sq_obj.sq=}', file=sys.stderr)
                raise

        if back_sq in [None, constants.PIECE_STAND_SQ]:
            # 動いていない、または、駒台にあったなら、対象外
            return constants.mind.NOT_IN_THIS_CASE

        #print(f'★ ＤoNotBack: {Helper.sq_to_masu(src_sq_obj.sq)=} の前位置は {Helper.sq_to_masu(back_sq)=}。')

        # 元居た位置に戻る手は、意志無し。
        if dst_sq_obj.sq == back_sq:
            return constants.mind.WILL_NOT

        # それ以外なら、意志有り。
        return constants.mind.WILL


    def after_best_moving(self, move, table):
        """指す手の確定時。
        """

        if self.is_enabled:
            src_sq_obj = Square(cshogi.move_from(move))
            dst_sq_obj = Square(cshogi.move_to(move))
            is_drop = cshogi.move_is_drop(move)

            # 戻れない駒は対象外。
            if cshogi.move_from_piece_type(move) in [cshogi.KNIGHT, cshogi.LANCE, cshogi.PAWN]:
                return

            # 移動元のマス番号
            if is_drop: # 打のとき。                
                src_sq = constants.PIECE_STAND_SQ
            else:
                src_sq = src_sq_obj.sq

            # 記憶
            self._back_board[dst_sq_obj.sq] = src_sq

            if not is_drop:
                self._back_board[src_sq] = None

            #print(f'★ ＤoNotBack: {Helper.sq_to_masu(dst_sq_obj.sq)=} に前位置 {Helper.sq_to_masu(src_sq)=} を記憶。')
