import cshogi
import sys

from ..helper import Helper


class WillNotToBuildRightWall():
    """右壁を作らない意志
    """


    @staticmethod
    def is_there_will_on_move(board, move):
        """指し手は［右壁を作らない意志］を残しているか？

        FIXME 先手視点でのみ実装しています。後手視点にも対応したい
        """
        src_sq = cshogi.move_from(move)
        dst_sq = cshogi.move_to(move)

        # 玉
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            return True

        black_k_sq = board.king_square(cshogi.BLACK)
        black_k_suji = Helper.sq_to_suji(black_k_sq)

        if black_k_suji < 2:
            return True

        black_k_dan = Helper.sq_to_dan(black_k_sq)

        right_side_of_k = []

        # 玉の右上
        if black_k_dan > 1:
            right_side_of_k.append(black_k_sq - 10)

        # 玉の真右
        right_side_of_k.append(black_k_sq - 9)

        # 玉の右下
        if black_k_dan < 9:
            right_side_of_k.append(black_k_sq - 8)

        # 道を塞がないならOk
        if dst_sq not in right_side_of_k:
            return True

        # 道を塞ぐ
        right_side_of_k.remove(dst_sq)

        # 道が空いていればOk
        for sq in right_side_of_k:
            if board.piece(sq) == cshogi.NONE:
                return True

        # 右壁ができているから偽
        return False
