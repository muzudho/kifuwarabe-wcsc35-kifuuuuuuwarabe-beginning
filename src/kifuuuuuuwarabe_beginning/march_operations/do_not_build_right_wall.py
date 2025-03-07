import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper


class DoNotBuildRightWall():
    """行進［右壁を作るな］
    ［右壁を作らない］意志

    NOTE 飛車も玉も、［右壁］の構成物になるので注意。
    """


    @staticmethod
    def will_play_before_move(move, table):
        """指し手は［右壁を作らない］意志を残しているか？

        定義：　移動前の玉の以右の全ての筋について、８段目、９段目の両方に駒がある状態を［右壁］とする。
        """
        ban = Ban(table)
        cmp = Comparison(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))
        #print(f'D: {cshogi.move_to_usi(move)=} {Helper.sq_to_masu(src_sq_obj.sq)=} {Helper.sq_to_masu(dst_sq_obj.sq)=}')

        # ライオンの指し手なら対象外
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            #print(f'★ ライオンの指し手は対象外')
            return Mind.NOT_IN_THIS_CASE

        k_sq_obj = Square(table.king_square(table.turn))     # 移動前の自玉の位置
        #print(f'★ {k_sq_obj.file=} {ban.suji(1)=}')

        # 玉が１筋にいるなら対象外
        if k_sq_obj.file == ban.suji(1):
            #print(f'★ 玉が１筋にいるなら対象外')
            return Mind.NOT_IN_THIS_CASE

        # 玉より左に移動する手なら対象外
        e1 = cmp.swap(k_sq_obj.file, dst_sq_obj.file)
        #print(f'★ {k_sq_obj.file=} {dst_sq_obj.file=} {e1[0]=} {e1[1]}')
        if e1[0] < e1[1]:
            #print(f'★ 玉より左に移動する手なら対象外')
            return Mind.NOT_IN_THIS_CASE

        # ８段目、９段目以外に移動する手なら対象外
        dan8 = ban.dan(8)
        dan9 = ban.dan(9)
        #print(f'D: {dst_sq_obj.rank=} {ban.dan(8)=} {ban.dan(9)}')
        if dst_sq_obj.rank not in [dan8, dan9]:
            #print(f'★ {dst_sq_obj.rank=}段目 は、 {dan8}段目、{dan9}段目以外に移動する手だから対象外')
            return Mind.NOT_IN_THIS_CASE


        # 玉の元位置より右の全ての筋で起こる移動について
        right_side_of_k = []

        # 八段目、九段目
        for rank in [ban.dan(8), ban.dan(9)]:
            sq = Helper.file_rank_to_sq(dst_sq_obj.file, rank)
            #print(f'D: {rank=} {sq=}')
            right_side_of_k.append(sq)

            # 道を塞ぐ動きなら
            if dst_sq_obj.sq in right_side_of_k:
                # 道を消す
                #print(f'D: 道を消す')
                right_side_of_k.remove(dst_sq_obj.sq)

        # 道が空いているか？
        is_empty = False
        for sq in right_side_of_k:
            if (table.piece(sq) == cshogi.NONE
                    # 👇 香車が９段目から８段目に上がるのを右壁と誤認するのを防ぐ
                    or sq == src_sq_obj.sq):
                #print(f'D: 道が空いている')
                is_empty = True

        if not is_empty:
            # 道が開いていなければ、意志なし
            #print(f'★ 道が開いていなければ、意志なし')
            return Mind.WILL_NOT


        # 道は空いていたから、意志あり
        #print(f'★ 道は空いていたから、意志あり')
        return Mind.WILL
