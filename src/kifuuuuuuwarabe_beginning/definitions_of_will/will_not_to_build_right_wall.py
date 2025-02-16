import cshogi
import sys

from .. import Mind
from ..sente_perspective import Ban, CshogiBoard, Comparison, Helper


class WillNotToBuildRightWall():
    """［右壁を作らない意志］

    NOTE 振り飛車をさせるとき、玉より右側に振って［右壁］が作られるケースがあるので注意。
    """


    @staticmethod
    def will_on_move(board, move):
        """指し手は［右壁を作らない意志］を残しているか？

        定義：　玉の右側の全ての筋について、８段目、９段目の両方に駒がある状態を［右壁］とする。
        """
        ban = Ban(board)
        cboard = CshogiBoard(board)
        cmp = Comparison(board)

        src_sq_obj = cboard.sq_obj(cshogi.move_from(move))
        dst_sq_obj = cboard.sq_obj(cshogi.move_to(move))

        # 玉の指し手なら対象外
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            return Mind.NOT_IN_THIS_CASE

        k_sq_obj = cboard.sq_obj(board.king_square(board.turn))     # 自玉
        k_sq_file = k_sq_obj.file

        # 玉が１筋にいるなら対象外
        if k_sq_file == ban.suji(1):
            return Mind.NOT_IN_THIS_CASE

        # 玉の以左に移動する手なら対象外
        if k_sq_file <= dst_sq_obj.file:
            return Mind.NOT_IN_THIS_CASE

        # ８段目、９段目以外に移動する手なら対象外
        if dst_sq_obj.rank not in [ban.dan(8), ban.dan(9)]:
            return Mind.NOT_IN_THIS_CASE


        # 玉より右の全ての筋で起こる移動について
        right_side_of_k = []

        # 八段目、九段目
        for rank in [ban.dan(8), ban.dan(9)]:
            right_side_of_k.append(Helper.file_rank_to_sq(dst_sq_obj.file, rank))

            # 道を塞ぐ動きなら
            if dst_sq_obj.sq in right_side_of_k:
                # 道を消す
                right_side_of_k.remove(dst_sq_obj.sq)

        # 道が空いているか？
        is_empty = False
        for sq in right_side_of_k:
            if (board.piece(sq) == cshogi.NONE
                    # 👇 香車が９段目から８段目に上がるのを右壁と誤認するのを防ぐ
                    or sq == src_sq_obj.sq):
                is_empty = True

        if not is_empty:
            # 道が開いていなければ、意志なし
            return Mind.WILL_NOT


        # 道は空いていたから、意志あり
        return Mind.WILL
