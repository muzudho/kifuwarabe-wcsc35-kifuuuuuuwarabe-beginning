import cshogi
import sys

from .. import Mind
from ..sente_perspective import Ban, CshogiBoard, Comparison, Helper


class WillNotToBuildRightWall():
    """［右壁を作らない意志］
    """


    @staticmethod
    def will_on_move(board, move):
        """指し手は［右壁を作らない意志］を残しているか？

        定義：　玉の右側の全ての筋について、８段目、９段目の両方に駒がある状態を［右壁］とする。
        """
        ban = Ban(board)
        cboard = CshogiBoard(board)
        cmp = Comparison(board)

        dst_sq_obj = cboard.sq_obj(cshogi.move_to(move))

        # 玉の指し手なら対象外
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            return Mind.NOT_IN_THIS_CASE

        k_sq = board.king_square(board.turn)     # 自玉
        k_suji = Helper.sq_to_suji(k_sq)

        # 玉が１筋にいるなら対象外
        if Helper.suji_to_file(k_suji) == ban.suji(1):
            return Mind.NOT_IN_THIS_CASE

        friend_k_dan = Helper.sq_to_dan(k_sq)


        # 玉より右の全ての筋について
        for suji in range(2, k_suji):
            right_side_of_k = []

            # 八段目、九段目
            for dan in range(8, 10):
                right_side_of_k.append(ban.suji_dan(suji, dan))

                # 道を塞ぐ動きなら
                if dst_sq_obj.sq in right_side_of_k:
                    # 道を消す
                    right_side_of_k.remove(dst_sq_obj.sq)

            # 道が空いているか？
            is_empty = False
            for sq in right_side_of_k:
                if board.piece(sq) == cshogi.NONE:
                    is_empty = True

            if not is_empty:
                # 道が開いていなければ、意志なし
                return Mind.WILL_NOT


        # 道は空いていたから、意志あり
        return Mind.WILL
