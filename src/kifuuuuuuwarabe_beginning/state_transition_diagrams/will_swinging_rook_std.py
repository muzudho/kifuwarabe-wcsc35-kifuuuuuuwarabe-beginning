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
        src_sq = cshogi.move_from(move)
        dst_sq = cshogi.move_to(move)
        #print(f'★ is_there_will_on_move: {Helper.sq_to_masu(src_sq)=} {Helper.sq_to_masu(dst_sq)=} {cshogi.move_from_piece_type(move)=}', file=sys.stderr)

        # FIXME 先手視点でのみ実装しています。後手視点にも対応したい

        # 玉
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            #print(f'★ is_there_will_on_move: 玉', file=sys.stderr)
            return Helper.sq_to_suji(dst_sq) <= Helper.sq_to_suji(src_sq)

        # 飛
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            black_k_sq = board.king_square(cshogi.BLACK)
            return Helper.sq_to_suji(dst_sq) >= Helper.sq_to_suji(black_k_sq)

        # 金
        if cshogi.move_from_piece_type(move) == cshogi.GOLD:
            #print(f'★ is_there_will_on_move: 金', file=sys.stderr)
            return Helper.sq_to_suji(dst_sq) <= Helper.sq_to_suji(src_sq)

        # 銀
        if cshogi.move_from_piece_type(move) == cshogi.SILVER:
            #print(f'★ is_there_will_on_move: 銀', file=sys.stderr)
            return Helper.sq_to_suji(dst_sq) <= Helper.sq_to_suji(src_sq)

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
