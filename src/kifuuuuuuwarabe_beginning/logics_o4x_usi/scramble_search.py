import cshogi

from ..models_o1x import PieceValues, Square, Turn
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

        Returns
        -------
        alices_value_after_move : int
            手番の点数。
        alices_best_move_list : list
            最善手のリスト。０～複数件の指し手。
            # FIXME 入玉宣言勝ちは空リストが返ってくる。            
        """
        
        alices_value_before_move = 0    # 手番の点数。

        (
            alices_value_after_move,
            alices_best_move_list   # FIXME 入玉宣言勝ちは空リストが返ってくる。
        ) = _ScrambleCaptureSearch.beta_search(
            depth                   = 2,
            bobs_value_before_move  = alices_value_before_move, # 相手から見た相手（beta）は、自分（alpha）。
            bobs_remaining_moves    = remaining_moves,
            gymnasium               = self._gymnasium)

        ################
        # MARK: ループ後
        ################
        return alices_value_after_move, alices_best_move_list


class _ScrambleCaptureSearch():
    """［駒を取る手］のスクランブル・サーチ。
    """


    @staticmethod
    def beta_search(depth, bobs_value_before_move, bobs_remaining_moves, gymnasium):
        """
        Returns
        -------
        bobs_value_before_move : int
            相手番（ボブ）の、指す前の点数。
        bobs_remaining_moves : list
            相手番（ボブ）の最善手のリスト。０～複数件の指し手。
            FIXME 入玉宣言勝ちは空リストが返ってくる。
        gymnasium : Gymnasium
            体育館。
        """

        bobs_take_move_list = []

        # ［駒を取る手］を全部探す。
        for move in bobs_remaining_moves:

            dst_sq_obj = Square(cshogi.move_to(move))               # 移動先マス
            dst_pc = gymnasium.table.piece(dst_sq_obj.sq)     # 移動先マスにある駒
            if Turn.is_opponent_pc(piece=dst_pc, table=gymnasium.table):
                bobs_take_move_list.append(move)

        # TODO take_move_list のオーダリングがしたければ、ここでする。

        ##########################
        # MARK: 相手番の全取る手前
        ##########################

        bobs_best_value     = -10000
        bobs_best_move_list = []

        # 相手番（ボブ）が［駒を取る手］を全部調べる。
        for bobs_move in bobs_take_move_list:
            #print(f'take_move={cshogi.move_to_usi(opponent_move)}')

            dst_sq_obj  = Square(cshogi.move_to(bobs_move))     # 移動先マス
            dst_pc      = gymnasium.table.piece(dst_sq_obj.sq)      # 移動先マスにある駒
            friend_piece_value = PieceValues.by_piece_type(pt=cshogi.piece_to_piece_type(dst_pc))

            bobs_value_after_move = bobs_value_before_move + friend_piece_value    # 自分の駒が取られたから、相手番の点数が増える

            if 0 < depth:

                ########################
                # MARK: 相手番が一手指す
                ########################

                gymnasium.do_move_o1x(move = bobs_move)

                ############################
                # MARK: 相手番が一手指した後
                ############################

                if gymnasium.table.is_game_over():
                    """手番の投了局面時。
                    """
                    return -10000, [] # 負けだから

                if gymnasium.table.is_nyugyoku():
                    """手番の入玉宣言局面時。
                    """
                    return 10000, []  # 勝ちだから  FIXME 入玉宣言勝ちをどうやって返す？

                # 一手詰めを詰める
                if not gymnasium.table.is_check():
                    """手番玉に王手がかかっていない時で"""

                    if (matemove := gymnasium.table.mate_move_in_1ply()):
                        """一手詰めの指し手があれば、それを取得"""
                        return 10000, matemove  # 勝ちだから

                ########################
                # MARK: 手番の全取る手前
                ########################

                alices_remaining_moves = gymnasium.table.legal_moves

                # TODO take_move_list のオーダリングがしたければ、ここでする。

                alices_value_before_move = - bobs_value_after_move  # 手番の点数。

                # alpha は自分の点数。相手の点数を逆にしたのが自分の点数。
                (
                    alices_value_after_move,
                    alices_best_move_list
                ) = _ScrambleCaptureSearch.beta_search(
                    depth                   = depth - 1,
                    bobs_value_before_move  = alices_value_before_move,
                    bobs_remaining_moves    = alices_remaining_moves,
                    gymnasium               = gymnasium)

                ########################
                # MARK: 相手番が一手戻す
                ########################

                gymnasium.undo_move_o1x()

                # 相手番は、一番得する手を指したい。
                if bobs_best_value < -alices_value_after_move:
                    bobs_best_value = -alices_value_after_move
                    bobs_best_move_list = [bobs_move]
                elif bobs_best_value == -alices_value_after_move:
                    bobs_best_move_list.append(bobs_move)

        ##########################
        # MARK: 相手番の全取る手後
        ##########################

        return bobs_best_value, bobs_best_move_list

