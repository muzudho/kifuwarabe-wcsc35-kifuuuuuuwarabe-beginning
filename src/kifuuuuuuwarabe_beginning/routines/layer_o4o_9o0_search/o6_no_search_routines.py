import cshogi
import time

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import constants, SquareModel
from ...models.layer_o1o0o_9o0_table_helper import TableHelper
from .search_routines import SearchRoutines


INFO_DEPTH = 6


class O6NoSearchRoutines(SearchRoutines):


    ######################################################
    # MARK: 一手も指さずに局面を見て、終局なら終局外を付加
    ######################################################

    @staticmethod
    def set_termination_if_it_o6(parent_pv, search_context_model):
        """一手も指さずに局面を見て、終局なら終局外を付加。
        手番が回ってきてから、終局が成立するものとする。（何も指さない手番）
        """
        SearchRoutines.update_parent_pv_look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)


    ################
    # MARK: 手を指す
    ################

    @staticmethod
    def move_all_pv_o6(pv_list, search_context_model):
        """探索の開始。

        Parameters
        ----------
        pv_list : list<P rincipalVariationModel>
            ［読み筋］のリスト。

        Returns
        -------
        pv_list : list<P rincipalVariationModel>
            有力な読み筋。棋譜のようなもの。
            枝が増えて、合法手の数より多くなることがあることに注意。
        """

        # ノード訪問時
        # ------------
        terminated_pv_list = []
        live_pv_list = []

        # 各PV
        # ----
        for pv in pv_list:
            # 履歴を全部指す
            # --------------
            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # 手番の処理
            # ----------

            # 一手も指さずに局面を見て、終局なら終局外を付加。
            O6NoSearchRoutines.set_termination_if_it_o6(parent_pv=pv, search_context_model=search_context_model)

            if pv.termination_model_pv is not None:     # 探索不要なら。
                terminated_pv_list.append(pv)           # 終了済みPVリストへ当PVを追加。

            else:
                # （無し）［水平指し手一覧］をクリーニング。
                # （無し）remaining_moves から pv へ変換。
                next_pv_list = []

                # # NOTE 再帰は廃止。デバッグ作れないから。ここで＜水平線＞（デフォルト値）。
                # child_plot_model = pv.deprecated_rooter_backwards_plot_model_in_backward_pv

            # MARK: 履歴を全部戻す
            # --------------------
            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # MARK: TODO 全ての親手をさかのぼり、［後ろ向き探索の結果］を確定
            # ----------------------------------------------------------

        # # 合法手スキャン後

        # # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        # if best_pv is None:
        #     return SearchRoutines.setup_to_no_candidates(info_depth=INFO_DEPTH, search_context_model=search_context_model)

        # # 読み筋に今回の手を付け加える。（ TODO 駒得点も付けたい）
        # best_pv.append_move_in_backward_pv(
        #         move                = best_move,
        #         capture_piece_type  = best_move_cap_pt,
        #         best_value          = best_value)

        return terminated_pv_list, live_pv_list
