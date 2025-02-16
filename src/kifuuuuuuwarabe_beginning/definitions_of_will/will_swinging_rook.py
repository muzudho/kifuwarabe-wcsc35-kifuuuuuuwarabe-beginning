import cshogi
import sys

from ..sente_perspective import Ban, Comparison, Helper, Turned, Ji


class WillSwingingRook():
    """［振り飛車をする意志］
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
        ban = Ban(board)
        cmp = Comparison(board)
        ji = Ji(board)
        turned = Turned(board)

        src_sq = cshogi.move_from(move)
        dst_sq = cshogi.move_to(move)
        #print(f'★ is_there_will_on_move: {Helper.sq_to_masu(src_sq)=} {Helper.sq_to_masu(dst_sq)=} {cshogi.move_from_piece_type(move)=}', file=sys.stderr)


        # 玉
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            # 飛車が２八にいるか？
            if board.piece(ban.masu(28)) == ji.pc(cshogi.ROOK):
                # この駒は動いてはいけない
                return False

            #print(f'★ is_there_will_on_move: 玉', file=sys.stderr)            
            op = cmp.swap(Helper.sq_to_suji(dst_sq), Helper.sq_to_suji(src_sq))
            return op[0] <= op[1]

        # 飛
        if cshogi.move_from_piece_type(move) == cshogi.ROOK:
            friend_k_sq = board.king_square(board.turn)
            # 飛車は４筋より左に振る。かつ、玉と同じ筋または玉より左の筋に振る
            #print(f'★ 飛車が振る： {Helper.sq_to_masu(friend_k_sq)=} {Helper.sq_to_masu(src_sq)=} {Helper.sq_to_masu(dst_sq)=}', file=sys.stderr)
            a = cmp.swap(Helper.sq_to_suji(dst_sq), turned.suji(4))
            b = cmp.swap(Helper.sq_to_suji(dst_sq), Helper.sq_to_suji(friend_k_sq))
            return a[0] > a[1] and b[0] >= b[1]

        # 金
        if cshogi.move_from_piece_type(move) == cshogi.GOLD:
            # 飛車が２八にいるか？
            if board.piece(ban.masu(28)) == ji.pc(cshogi.ROOK):
                # この駒は、６筋より右にあるか？
                op = cmp.swap(Helper.sq_to_suji(src_sq), turned.suji(6))
                if op[0] < op[1]:
                    # この駒は動いてはいけない
                    return False

                # この駒は、５筋より左にあるか？
                
                op = cmp.swap(Helper.sq_to_suji(src_sq), turned.suji(6))
                if op[0] >= op[1]:
                    # この駒は左の方以外に動かしてはいけない
                    
                    op = cmp.swap(Helper.sq_to_suji(dst_sq), turned.suji(6))
                    if op[0] <= op[1]:
                        return False

            #print(f'★ is_there_will_on_move: 金', file=sys.stderr)
            op = cmp.swap(Helper.sq_to_suji(dst_sq), Helper.sq_to_suji(src_sq))
            return op[0] <= op[1]

        # 銀
        if cshogi.move_from_piece_type(move) == cshogi.SILVER:
            # 飛車が２八にいるか？
            if board.piece(ban.masu(28)) == ji.pc(cshogi.ROOK):
                # この駒は、６筋より右にあるか？
                op = cmp.swap(Helper.sq_to_suji(src_sq), turned.suji(6))
                if op[0] < op[1]:
                    # この駒は動いてはいけない
                    return False

                # この駒は、５筋より左にあるか？
                op = cmp.swap(Helper.sq_to_suji(src_sq), turned.suji(6))
                if op[0] >= op[1]:
                    # この駒は左の方以外に動かしてはいけない
                    op = cmp.swap(Helper.sq_to_suji(dst_sq), turned.suji(6))
                    if op[0] <= op[1]:
                        return False

            #print(f'★ is_there_will_on_move: 銀', file=sys.stderr)
            op = cmp.swap(Helper.sq_to_suji(dst_sq), Helper.sq_to_suji(src_sq))
            return op[0] <= op[1]

        return True    # FIXME


    def __init__(self):
        self._state = WillSwingingRook.ENTRY


    @property
    def state(self):
        return self._state


    def to_transition(self, board):
        """遷移する
        """

        if self.state == WillSwingingRook.ENTRY:
            return

        if self.state == WillSwingingRook.BEFORE_SWINGING_ROOK:
            return

        if self.state == WillSwingingRook.AFTER_NOT_SWINGING_ROOK:
            return

        if self.state == WillSwingingRook.AFTER_SWINGING_ROOK:
            return
