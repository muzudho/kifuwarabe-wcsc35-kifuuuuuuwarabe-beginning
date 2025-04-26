import cshogi

from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import constants, Mars, SquareModel
from ..layer_o2o0 import BackwardsPlotModel
from ..layer_o4o0_rules.negative import DoNotDepromotionModel


class SearchAlgorithmModel:
    """検索アルゴリズム。
    """


    @staticmethod
    def convert_remaining_moves_to_pv_list(parent_pv, remaining_moves, search_context_model):
        pv_list = []

        # 残った指し手について
        for my_move in remaining_moves:
            ##################
            # MARK: 一手指す前
            ##################

            # 打の場合、取った駒無し。空マス。
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # ［移動先マス］にある［駒種類］。つまりそれは取った駒。打の［移動先マス］は常に空きマス。

            pv = parent_pv.new_and_append(
                    move_pv     = my_move,
                    cap_pt_pv   = cap_pt,
                    value_pv    = PieceValuesModel.get_piece_exchange_value_on_earth(
                                        pt          = cap_pt,
                                        is_mars     = search_context_model.gymnasium.is_mars),
                    replace_backwards_plot_model    = parent_pv.backwards_plot_model,
                    replace_is_terminate            = False)
            pv_list.append(pv)
        
        return pv_list


    def __init__(self, search_context_model):
        """
        Parameters
        ----------
        search_context_model : SearchContextModel
            探索モデル。
        """
        self._search_context_model = search_context_model


    @property
    def search_context_model(self):
        return self._search_context_model


    def create_backwards_plot_model_at_game_over(self):
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.RESIGN,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    def create_backwards_plot_model_at_mate_move_in_1_ply(self, mate_move):
        self._search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=mate_move, hint='＜一手詰め＞')
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')
        dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
        cap_pt = self._search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

        best_plot_model = BackwardsPlotModel(
                is_mars_at_out_of_termination   = not self._search_context_model.gymnasium.is_mars,     # ［詰む］のは、もう１手先だから。
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.RESIGN,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])
    
        # 今回の手を付け加える。
        if self._search_context_model.gymnasium.is_mars:
            best_value = constants.value.BIG_VALUE        # 火星の負け
        else:
            best_value = constants.value.SMALL_VALUE      # 地球の負け

        best_plot_model.append_move_from_back(
                move                = mate_move,
                capture_piece_type  = cap_pt,
                best_value          = best_value,
                hint                = f"{Mars.japanese(self._search_context_model.gymnasium.is_mars)}は一手詰まされ")
        return best_plot_model


    def create_backwards_plot_model_at_nyugyoku_win(self):
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜入玉宣言勝ち＞')
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.NYUGYOKU_WIN,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    def create_backwards_plot_model_at_horizon(self, depth_qs):
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜水平線[深QS={depth_qs}]＞")
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.MAX_DEPTH_BY_THINK,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    def create_backwards_plot_model_at_quiescence(self, depth_qs):
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜静止[深QS={depth_qs}]＞")
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.QUIESCENCE,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    def create_backwards_plot_model_at_no_candidates(self, depth_qs):
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜候補手無し[深QS={depth_qs}]＞")
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.NO_CANDIDATES,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    def remove_drop_moves(self, remaining_moves):
        """［打］は除外。
        """
        for my_move in reversed(remaining_moves):   # 指し手を全部調べる。
            if cshogi.move_is_drop(my_move):
                remaining_moves.remove(my_move)

        return remaining_moves


    def remove_depromoted_moves(self, remaining_moves):
        """［成れるのに成らない手］は除外。
        """

        do_not_depromotion_model = DoNotDepromotionModel(                                               # 号令［成らないということをするな］を利用。
                basketball_court_model=self._search_context_model.gymnasium.basketball_court_model)

        do_not_depromotion_model._on_node_entry_negative(               # ノード来訪時。
                remaining_moves = remaining_moves,
                table           = self._search_context_model.gymnasium.table)

        for my_move in reversed(remaining_moves):   # 指し手を全部調べる。
            # ［成れるのに成らない手］は除外
            mind = do_not_depromotion_model._on_node_exit_negative(
                    move    = my_move,
                    table   = self._search_context_model.gymnasium.table)
            if mind == constants.mind.WILL_NOT:
                remaining_moves.remove(my_move)

        return remaining_moves


    def filtering_capture_or_mate(self, remaining_moves, rollback_if_empty):
        """駒を取る手と、王手のみ残す。

        Returns
        -------
        remaining_moves : list
            残りの指し手。
        rolled_back : bool
            ロールバックされた。
        """

        rolled_back = False

        if rollback_if_empty:
            old_remaining_moves = remaining_moves.copy()    # バックアップ

        for my_move in reversed(remaining_moves):
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self._search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            is_capture  = (cap_pt != cshogi.NONE)

            # ２階以降の呼出時は、駒を取る手でなければ無視。
            if not is_capture:
                # ＜📚原則２＞ 王手は（駒を取らない手であっても）探索を続け、深さを１手延長する。
                if self._search_context_model.gymnasium.table.is_check():
                    #depth_extend += 1  # FIXME 探索が終わらないくなる。
                    pass

                else:
                    remaining_moves.remove(my_move)
                    continue

        if rollback_if_empty and len(remaining_moves) == 0:
            remaining_moves = old_remaining_moves   # 復元
            rolled_back     = True

        return remaining_moves, rolled_back
