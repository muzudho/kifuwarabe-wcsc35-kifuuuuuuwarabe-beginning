import cshogi

from ..models_o1x import constants, PieceValues, SearchResultStateModel, Square, Turn
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

        # TODO take_move_list のオーダリングがしたければ、ここでする。

        best_alpha = -10000
        best_move_list = []

        # ［駒を取る手］のスクランブル・サーチをする。
        for move in take_move_list:
            print(f'take_move={cshogi.move_to_usi(move)}')

            dst_sq_obj = Square(cshogi.move_to(move))               # 移動先マス
            dst_pc = self._gymnasium.table.piece(dst_sq_obj.sq)     # 移動先マスにある駒
            value = PieceValues.by_piece_type(pt=cshogi.piece_to_piece_type(dst_pc))

            ################
            # MARK: 一手指す
            ################

            self._gymnasium.do_move_o1x(move = move)

            ####################
            # MARK: 一手指した後
            ####################

            scramble_capture_search = _ScrambleCaptureSearch(
                    gymnasium = self._gymnasium)
            
            # alpha は自分の点数。相手の点数を逆にしたのが自分の点数。
            alpha = - scramble_capture_search.search(
                depth   = 0,
                alpha   = -value,   # 相手から見れば、取られているから負。
                move    = move)

            ################
            # MARK: 一手戻す
            ################

            self._gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            if best_alpha < alpha:
                best_alpha = alpha
                best_move_list = [move]
            elif best_alpha == alpha:
                best_move_list.append(move)

        ################
        # MARK: ループ後
        ################
        return best_alpha, best_move_list


class _ScrambleCaptureSearch():
    """［駒を取る手］のスクランブル・サーチ。
    """


    def __init__(self, gymnasium):
        self._gymnasium = gymnasium


    def search(self, depth, alpha, move):

        if self._gymnasium.table.is_game_over():
            """投了局面時。
            """
            return -10000   # 負けだから

        if self._gymnasium.table.is_nyugyoku():
            """入玉宣言局面時。
            """
            return 10000    # 勝ちだから

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return 10000    # 勝ちだから

        if 0 < depth:
            # TODO 一手指す
            remaining_moves = list(self._gymnasium.table.legal_moves)
            pass

            # TODO 一手戻す

        return alpha
