import cshogi
import sys

from ..helper import Helper, Turned


class WillNotToBuildRightWall():
    """右壁を作らない意志
    """


    @staticmethod
    def is_there_will_on_move(board, move):
        """指し手は［右壁を作らない意志］を残しているか？
        """
        src_sq = cshogi.move_from(move)
        dst_sq = cshogi.move_to(move)

        # 玉
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            return True

        turned = Turned(board)

        friend_k_sq = board.king_square(board.turn)     # 自玉
        friend_k_suji = Helper.sq_to_suji(friend_k_sq)

        if friend_k_suji < turned.suji(2):
            return True

        friend_k_dan = Helper.sq_to_dan(friend_k_sq)

        right_side_of_k = []

        # 玉の右上
        if friend_k_dan > turned.dan(1):
            right_side_of_k.append(friend_k_sq + turned.sign(-10))

        # 玉の真右
        right_side_of_k.append(friend_k_sq + turned.sign(-9))

        # 玉の右下
        if friend_k_dan < turned.dan(9):
            right_side_of_k.append(friend_k_sq + turned.sign(-8))

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
