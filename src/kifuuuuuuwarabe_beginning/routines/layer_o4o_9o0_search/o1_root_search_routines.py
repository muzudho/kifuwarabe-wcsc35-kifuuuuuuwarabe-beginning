import cshogi
import time

from ...models.layer_o1o0 import constants, SquareModel
from ...models.layer_o5o0_search import SearchContextModel
from .search_routines import SearchRoutines
from .o2_counter_search_routines import O2CounterSearchRoutines


INFO_DEPTH = 1


class O1RootSearchRoutines(SearchRoutines):
    """１階の探索。
    """

    ######################
    # MARK: 縦の辺を伸ばす
    ######################

    @staticmethod
    def extend_vertical_edges_o1(pv_list, search_context_model):
        """縦の辺を伸ばす。
        """

        # ノード訪問時
        # ------------
        O1RootSearchRoutines._set_controls(pv_list=pv_list, search_context_model=search_context_model)

        # PVリスト探索
        # ------------
        for pv in pv_list:

            # 履歴を全部指す前
            # ----------------
            my_move                         = pv.leafer_move_in_frontward_pv
            cap_pt                          = pv.leafer_cap_pt_in_frontward_pv
            piece_exchange_value_on_earth   = pv.leafer_value_in_frontward_pv

            # 履歴を全部指す
            # --------------
            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # 履歴を全部指した後
            # ------------------
            search_context_model.number_of_visited_nodes  += 1    # 開示情報
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, cap_pt=cap_pt, value=piece_exchange_value_on_earth, comment='')    # ログ

            # 相手番の処理
            # ------------

            # 一手も指さずに局面を見て、終局なら終局外を付加。
            O1RootSearchRoutines.set_termination_if_it_o1(parent_pv=pv, search_context_model=search_context_model)

            # 履歴を全部戻す
            # --------------
            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # 履歴を全部戻した後
            # ------------------
            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()


    ######################################################
    # MARK: 一手も指さずに局面を見て、終局なら終局外を付加
    ######################################################

    @staticmethod
    def set_termination_if_it_o1(parent_pv, search_context_model):
        """一手も指さずに局面を見て、終局なら終局外を付加。
        手番が回ってきてから、終局が成立するものとする。（何も指さない手番）
        """
        SearchRoutines.update_parent_pv_look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)


    ################################
    # MARK: 水平指し手をクリーニング
    ################################

    @staticmethod
    def cleaning_horizontal_edges_o1(remaining_moves, parent_pv, search_context_model):
        """［水平指し手一覧］をクリーニング。

        Parameters
        ----------
        parent_pv : P rincipalVariationModel
            親手。

        Returns
        -------
        remaining_moves : list<int>
            シーショーギの指し手のリスト。
        """

        remaining_moves = SearchRoutines.remove_depromoted_moves(remaining_moves=remaining_moves, search_context_model=search_context_model)       # ［成れるのに成らない手］は除外
        return remaining_moves


    ################
    # MARK: 手を指す
    ################

    # @staticmethod
    # def move_pv_o2(terminated_pv_list, live_pv_list, pv, remaining_moves, search_context_model):
    #     """探索の開始。
        
    #     Parameters
    #     ----------
    #     pv_list : list<P rincipalVariationModel>
    #         ［読み筋］のリスト。

    #     Returns
    #     -------
    #     pv_list : list<P rincipalVariationModel>
    #         有力な読み筋。棋譜のようなもの。
    #         枝が増えて、合法手の数より多くなることがあることに注意。
    #     """

    #     # TODO 縦の辺を伸ばす。
    #     # O2CounterSearchRoutines.extend_vertical_edges_o2(pv_list=next_pv_list, search_context_model=search_context_model)
    #     # (terminated_pv_list, live_pv_list) = O3QuiescenceSearchRoutines.move_all_pv_o3(
    #     #         pv_list             = live_pv_list,
    #     #         search_context_model= search_context_model)

    #     # TODO 探索不要なら

    #     # TODO ［水平指し手一覧］をクリーニング。

    #     # TODO ［駒を取る手］がないことを、［静止］と呼ぶ。

    #     # TODO ［水平指し手一覧］を［PV］へ変換。

    #     # TODO 縦の辺を伸ばす。

    #     # TODO 残りのPVリストを集める

    #     # TODO （奇数＋１階なら火星、偶数＋１階なら地球）が嫌な手は削除。
    #     # for terminated_pv in reversed(terminated_pv_list):
    #     #     if 0 < terminated_pv.leafer_value_in_frontward_pv:
    #     #         terminated_pv_list.remove(terminated_pv)
    #     #
    #     # for live_pv in reversed(live_pv_list):
    #     #     if 0 < live_pv.leafer_value_in_frontward_pv:
    #     #         live_pv_list.remove(live_pv)


    #     # MARK: TODO 全ての親手をさかのぼり、［後ろ向き探索の結果］を確定
    #     # ----------------------------------------------------------

    #     # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
    #     # pv.append_move_in_backward_pv(
    #     #         move                = pv.leafer_move_in_frontward_pv,
    #     #         capture_piece_type  = pv.leafer_cap_pt_in_frontward_pv,
    #     #         best_value          = pv.get_root_value_in_backward_pv())

    #     # ベータカットもしません。全部返すから。
    #     #pv.value_pv += pv.get_root_value_in_backward_pv()
    #     #terminated_pv_list.append(pv.copy_pv())


    ####################
    # MARK: サブルーチン
    ####################

    @staticmethod
    def _set_controls(pv_list, search_context_model):
        """利きを記録
        """
        search_context_model.clear_root_searched_control_map()

        for pv in pv_list:
            my_move = pv.leafer_move_in_frontward_pv
            if cshogi.move_is_drop(my_move):
                continue
            dst_sq_obj = SquareModel(cshogi.move_to(my_move))       # ［移動先マス］
            search_context_model.set_root_searched_control_map(sq=dst_sq_obj.sq, value=True)
