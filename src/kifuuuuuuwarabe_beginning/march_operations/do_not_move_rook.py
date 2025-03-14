import cshogi
import sys

from .. import Mind
from ..models import Square
from ..sente_perspective import Ban, Comparison, Helper, Ji
from .match_operation import MatchOperation


class DoNotMoveRook(MatchOperation):
    """行進［きりんは動くな］
    ［きりんは止まる］意志

    NOTE 初期状態は［アイドリング］で始まり、飛車を振った後に有効化します
    """


    @staticmethod
    def before_move(move, table):
        """指す前に。
        """

        ban = Ban(table)
        cmp = Comparison(table)

        src_sq_obj = Square(cshogi.move_from(move))
        dst_sq_obj = Square(cshogi.move_to(move))

        # キリン以外なら対象外
        if cshogi.move_from_piece_type(move) not in [cshogi.ROOK]:
            return Mind.NOT_IN_THIS_CASE

        # # 移動先が異段なら意志あり
        # e1 = cmp.swap(dst_sq_obj.rank, src_sq_obj.rank)
        # if e1[0] != e1[1]:
        #     return Mind.WILL

        # それ以外は意志なし
        return Mind.WILL_NOT


    def __init__(self):
        super().__init__()
        self._name = 'きりんは動くな'


    def do_anything(self, will_play_moves, table, config_doc):
        if config_doc['march_operations']['do_not_move_rook']:

            ban = Ban(table)
            cmp = Comparison(table)
            ji = Ji(table)

            # 自ライオンが２八にいる
            if table.piece(ban.masu(28)) == ji.pc(cshogi.KING):
                # （処理を行わず）このオブジェクトを除外
                self._is_removed = True
            
            else:
                for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
                    m = will_play_moves[i]
                    mind = DoNotMoveRook.before_move(m, table)
                    if mind == Mind.WILL_NOT:
                        del will_play_moves[i]

        return will_play_moves


    def on_best_move_played_when_idling(self, move, table, config_doc):
        """指す手の確定時。
        """

        if config_doc['march_operations']['do_not_move_rook']: # 無効化のときも（アクティベートのために）実行します
            ban = Ban(table)
            cmp = Comparison(table)

            src_sq_obj = Square(cshogi.move_from(move))
            dst_sq_obj = Square(cshogi.move_to(move))

            # キリン以外なら対象外。
            if cshogi.move_from_piece_type(move) not in [cshogi.ROOK]:
                return

            # キリンの移動先が異筋なら、この行進演算を有効化します。
            e1 = cmp.swap(dst_sq_obj.file, src_sq_obj.file)
            if e1[0] != e1[1]:
                print(f'★ ｏn_best_move_played: {self.name=} 有効化')
                self._is_activate = True

            #     # キリンの移動先が異段なら、この行進演算は削除します。
            #     e1 = cmp.swap(dst_sq_obj.rank, src_sq_obj.rank)
            #     if e1[0] != e1[1]:
            #         self._is_removed = True
