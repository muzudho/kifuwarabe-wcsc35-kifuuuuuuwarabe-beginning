import cshogi
import sys

from ..helper import Helper


class WillSwingingRookSTD():
    """［振り飛車します］状態遷移図
    """


    @staticmethod
    @property
    def ENTRY():
        return 0


    @staticmethod
    @property
    def BEFORE_SWINGING_ROOK():
        return 1


    @staticmethod
    @property
    def AFTER_NOT_SWINGING_ROOK():
        return 2


    @staticmethod
    @property
    def AFTER_SWINGING_ROOK():
        return 3


    @staticmethod
    def is_there_will_on_board(board):
        """盤は［振り飛車する意志］を残しているか？

        ４０手目までは振り飛車の意志を残しているとします。
        ４１手目以降は振り飛車の意志はありません
        """
        print(f'★ is_there_will_on_board: {board.move_number=}', file=sys.stderr)
        return board.move_number < 41


    @staticmethod
    def is_there_will_on_move(board, move):
        """指し手は［振り飛車する意志］を残しているか？
        """
        print(f'★ is_there_will_on_move: {Helper.sq_to_masu(cshogi.move_from(move))=} {Helper.sq_to_masu(cshogi.move_to(move))=} {cshogi.move_from_piece_type(move)=}', file=sys.stderr)
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            print(f'★ is_there_will_on_move: 玉', file=sys.stderr)

        return True    # FIXME


    def __init__(self):
        self._state = WillSwingingRookSTD.ENTRY


    @property
    def state(self):
        return self._state


    def to_transition(self, board):
        """遷移する
        """

        if self.state == WillSwingingRookSTD.ENTRY:
            return

        if self.state == WillSwingingRookSTD.BEFORE_SWINGING_ROOK:
            return

        if self.state == WillSwingingRookSTD.AFTER_NOT_SWINGING_ROOK:
            return

        if self.state == WillSwingingRookSTD.AFTER_SWINGING_ROOK:
            return
