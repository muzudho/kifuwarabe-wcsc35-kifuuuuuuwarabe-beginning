import cshogi
import sys

from .. import Mind
from ..sente_perspective import Ban, Comparison, CshogiBoard, Helper, Ji


class WillSwingingRook():
    """［振り飛車をする意志］
    """


    @staticmethod
    def will_on_board(board):
        """盤は［振り飛車する意志］を残しているか？

        ４０手目までは振り飛車の意志を残しているとします。
        ４１手目以降は振り飛車の意志はありません
        """
        print(f'★ is_there_will_on_board: {board.move_number=}', file=sys.stderr)
        if board.move_number < 41:
            return Mind.WILL
        
        return Mind.WILL_NOT


    @staticmethod
    def will_on_move(board, move):
        """指し手は［振り飛車する意志］を残しているか？
        """
        ban = Ban(board)
        cboard = CshogiBoard(board)
        cmp = Comparison(board)
        ji = Ji(board)

        src_sq_obj = cboard.sq_obj(cshogi.move_from(move))
        dst_sq_obj = cboard.sq_obj(cshogi.move_to(move))


        # 玉
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            # 飛車が２八にいるか？
            if board.piece(ban.masu(28)) == ji.pc(cshogi.ROOK):
                # この駒は動いてはいけない
                return Mind.WILL_NOT

            #print(f'★ will_on_move: 玉', file=sys.stderr)            
            # 元位置位右に移動するなら、意志あり
            op = cmp.swap(dst_sq_obj.file, src_sq_obj.file)
            if op[0] <= op[1]:
                return Mind.WILL
            
            return Mind.WILL_NOT


        # 飛
        if cshogi.move_from_piece_type(move) == cshogi.ROOK:
            k_sq_obj = cboard.sq_obj(board.king_square(board.turn))
            # 飛車は４筋より左に振る。かつ、玉と同じ筋または玉より左の筋に振る
            e1 = cmp.swap(dst_sq_obj.file, ban.suji(4))
            e2 = cmp.swap(dst_sq_obj.file, k_sq_obj.file)

            if e1[0] > e1[1] and e2[0] >= e2[1]:
                return Mind.WILL
            
            return Mind.WILL_NOT


        return Mind.NOT_IN_THIS_CASE
