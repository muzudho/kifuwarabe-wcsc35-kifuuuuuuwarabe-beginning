import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper


class WillForThreeGoldAndSilverCoinsToGatherToTheRight():
    """［金銀３枚が右に集まる意志］
    """

    @staticmethod
    def will_before_move(move, table):
        """［金銀３枚が右に集まる意志］があるか？

        先手から見て５筋と６筋の間にドアがあるとする。
        ５筋位左にある金銀が左へ移動するとき、６筋位左に自駒の金銀が０枚である場合のみ移動できる。
        """

        ban = Ban(table)
        cmp = Comparison(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))

        # ４筋位右にある駒は対象外
        e1 = cmp.swap(src_sq_obj.file, ban.suji(4))
        if e1[0] <= e1[1]:
            return Mind.NOT_IN_THIS_CASE

        # 移動先が同筋位右なら対象外
        e1 = cmp.swap(dst_sq_obj.file, src_sq_obj.file)
        if e1[0] <= e1[1]:
            return Mind.NOT_IN_THIS_CASE

        # 36マスをスキャンする
        left_from_6_suji = [Helper.file_rank_to_sq(file, rank) for file in ban.suji_range(6, 10)
            for rank in ban.dan_range(1, 10)]
        #print(f'{len(left_from_6_suji)=} {left_from_6_suji=}')

        count = 0

        for sq in left_from_6_suji:
            pc = table.piece(sq)

            pt = cshogi.piece_to_piece_type(pc)
            if pt not in [cshogi.GOLD, cshogi.SILVER]:
                continue

            if pc <= 16:
                color = cshogi.BLACK
            else:
                color = cshogi.WHITE

            if table.turn != color:
                continue

            count += 1

        if count == 0:
            return Mind.WILL

        return Mind.WILL_NOT
