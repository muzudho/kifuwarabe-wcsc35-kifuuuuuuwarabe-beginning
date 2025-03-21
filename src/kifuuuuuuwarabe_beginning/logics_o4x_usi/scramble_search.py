import cshogi

from ..models_o1x import constants, Square, Turn
from ..models_o2x.nine_rank_side_perspective import NineRankSidePerspective


class ScrambleSearch():
    """きふわらべのお父んが勝手に［スクランブル・サーチ］と読んでいるもの。
    静止探索の代わりの物。
    """


    def __init__(self, gymnasium):
        self._gymnasium = gymnasium


    def start(self, remaining_moves):
        """
        # TODO 静止探索はせず、［スクランブル・サーチ］というのを考える。静止探索は王手が絡むと複雑だ。
        # リーガル・ムーブのうち、
        #   手番の１手目なら：
        #       ［取られそうになっている駒を逃げる手］∪［駒を取る手］∪［利きに飛び込む手］に絞り込む。（１度調べた手は２度目は調べない）
        #       ［放置したとき］も調べる。
        #   相手番の１手目なら：
        #       ［動いた駒を取る手］に絞り込む。（１番安い駒から動かす）
        #   手番の２手目なら：
        #       ［動いた駒を取る手］に絞り込む。（１番安い駒から動かす）
        #   最後の評価値が、１手目の評価値。
        """

        np = NineRankSidePerspective(table = self._gymnasium.table)

        take_move_list = []

        # ［駒を取る手］を全部探す。
        for move in remaining_moves:

            dst_sq_obj = Square(cshogi.move_to(move))               # 移動先マス
            dst_pc = self._gymnasium.table.piece(dst_sq_obj.sq)     # 移動先マスにある駒
            if Turn.is_opponent_pc(piece=dst_pc, table=self._gymnasium.table):
                take_move_list.append(move)

        for move in take_move_list:
            print(f'take_move={cshogi.move_to_usi(move)}')
