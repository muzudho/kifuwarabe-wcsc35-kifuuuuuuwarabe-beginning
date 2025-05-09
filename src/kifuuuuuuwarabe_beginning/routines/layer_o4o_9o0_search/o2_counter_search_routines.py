import cshogi
import time

from ...models.layer_o1o0 import constants, SquareModel
from .search_routines import SearchRoutines
from .o3_quiescence_search_routines import O3QuiescenceSearchRoutines


INFO_DEPTH = 2


class O2CounterSearchRoutines(SearchRoutines):
    """２階の探索。
    """

    ######################
    # MARK: 縦の辺を伸ばす
    ######################

    @staticmethod
    def extend_vertical_edges_o2(pv_list, search_context_model):
        """縦の辺を伸ばす。
        """

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
            search_context_model.number_of_visited_nodes  += 1
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, cap_pt=cap_pt, value=piece_exchange_value_on_earth, comment='')

            # 相手番の処理
            # ------------

            # 一手も指さずに局面を見て、終局なら終局外を付加。
            O2CounterSearchRoutines.set_termination_if_it_o2(parent_pv=pv, search_context_model=search_context_model)

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
    def set_termination_if_it_o2(parent_pv, search_context_model):
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
    def cleaning_horizontal_edges_o2(parent_pv, search_context_model):
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
        
        remaining_moves = list(search_context_model.gymnasium.table.legal_moves)      # 全合法手。
        remaining_moves = SearchRoutines.remove_depromoted_moves(remaining_moves=remaining_moves, search_context_model=search_context_model)     # ［成れるのに成らない手］は除外
        aigoma_move_list = O2CounterSearchRoutines._choice_aigoma_move_list(remaining_moves=remaining_moves, search_context_model=search_context_model)   # ［間駒］（相手の利きの上に置く手）を抽出。
        remaining_moves = O2CounterSearchRoutines._remove_drop_except_aigoma(remaining_moves)  # ［間駒］以外の［打］は（多すぎるので）除外。
        (remaining_moves, rolled_back) = SearchRoutines.filtering_capture_or_mate(remaining_moves=remaining_moves, rollback_if_empty=True, search_context_model=search_context_model)    # ［カウンター探索］では、駒を取る手と、王手のみ残す。［駒を取る手、王手］が無ければ、（巻き戻して）それ以外の手を指します。
        remaining_moves.extend(aigoma_move_list)
        return remaining_moves


    ####################
    # MARK: サブルーチン
    ####################

    @staticmethod
    def _choice_aigoma_move_list(remaining_moves, search_context_model):
        # TODO ［間駒］（相手の利きの上に置く手）を抽出。
        aigoma_move_list = []
        for my_move in remaining_moves:
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            is_aigoma = search_context_model.get_root_searched_control_map(sq=dst_sq_obj.sq)
            if is_aigoma:
                aigoma_move_list.append(my_move)
        return aigoma_move_list


    @staticmethod
    def _remove_drop_except_aigoma(remaining_moves):
        # ［間駒］以外の［打］は（多すぎるので）除外。
        for my_move in reversed(remaining_moves):
            is_drop = cshogi.move_is_drop(my_move)
            if is_drop:
                remaining_moves.remove(my_move)
        return remaining_moves
