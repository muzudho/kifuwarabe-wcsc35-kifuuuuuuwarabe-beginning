import cshogi

from ..layer_o1o0 import constants, Mars, SquareModel
from ..layer_o2o0 import BackwardsPlotModel, cutoff_reason
from ..layer_o4o0_rules.negative import DoNotDepromotionModel


class SearchAlgorithmModel:
    """検索アルゴリズム。
    """


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
                cutoff_reason                   = cutoff_reason.GAME_OVER,
                hint                            = '手番の投了局面時')


    def create_backwards_plot_model_at_mate_move_in_1_ply(self, mate_move):
        self._search_context_model.gymnasium.health_check_qs_model.append_node(f"＜一手詰め＞{cshogi.move_to_usi(mate_move)}")
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')
        dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
        cap_pt = self._search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

        best_plot_model = BackwardsPlotModel(
                is_mars_at_out_of_termination   = not self._search_context_model.gymnasium.is_mars,     # ［詰む］のは、もう１手先だから。
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.RESIGN,
                cutoff_reason                   = cutoff_reason.MATE_MOVE_IN_1_PLY,
                hint                            = '一手詰め時')
    
        # 今回の手を付け加える。
        best_plot_model.append_move(
                move                = mate_move,
                capture_piece_type  = cap_pt,
                hint                = f"{Mars.japanese(self._search_context_model.gymnasium.is_mars)}の一手詰め時")
        return best_plot_model


    def create_backwards_plot_model_at_nyugyoku_win(self):
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜入玉宣言勝ち＞')
        best_plot_model = BackwardsPlotModel(
                is_mars_at_out_of_termination  = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination  = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination             = constants.out_of_termination.NYUGYOKU_WIN,
                cutoff_reason           = cutoff_reason.NYUGYOKU_WIN,
                hint                    = '手番の入玉宣言勝ち局面時')
        return best_plot_model


    def create_backwards_plot_model_at_horizon(self, depth_qs):
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜水平線＞')
        best_plot_model = BackwardsPlotModel(
                is_mars_at_out_of_termination   = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.MAX_DEPTH_BY_THINK,
                cutoff_reason                   = cutoff_reason.MAX_DEPTH,
                hint                            = f"{self._search_context_model.max_depth - depth_qs}階の{Mars.japanese(self._search_context_model.gymnasium.is_mars)}でこれ以上深く読まない場合_{depth_qs=}/{self._search_context_model.max_depth=}")
        return best_plot_model


    def create_backwards_plot_model_at_quiescence(self, depth_qs):
        self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜静止＞')
        future_plot_model = BackwardsPlotModel(
                is_mars_at_out_of_termination  = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination  = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination             = constants.out_of_termination.QUIESCENCE,
                cutoff_reason           = cutoff_reason.NO_MOVES,
                hint                    = f"{self._search_context_model.max_depth - depth_qs + 1}階の{Mars.japanese(self._search_context_model.gymnasium.is_mars)}は静止")
        return future_plot_model


    def create_backwards_plot_model_at_no_candidates(self, depth_qs):
        future_plot_model = BackwardsPlotModel(
                is_mars_at_out_of_termination   = self._search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = self._search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.NO_CANDIDATES,
                cutoff_reason                   = cutoff_reason.NO_MOVES,
                hint                            = f"{self._search_context_model.max_depth - depth_qs + 1}階の{Mars.japanese(self._search_context_model.gymnasium.is_mars)}は指したい手無し")
        return future_plot_model


    def remove_depromoted_moves(self, remaining_moves):
        """［成れるのに成らない手］は除外。
        """
        # 指し手を全部調べる。
        do_not_depromotion_model = DoNotDepromotionModel(
                basketball_court_model=self._search_context_model.gymnasium.basketball_court_model)    # TODO 号令［成らないということをするな］

        do_not_depromotion_model._on_node_entry_negative(
                table=self._search_context_model.gymnasium.table)

        for my_move in reversed(remaining_moves):
            # ［成れるのに成らない手］は除外
            mind = do_not_depromotion_model._on_node_exit_negative(
                    move    = my_move,
                    table   = self._search_context_model.gymnasium.table)
            if mind == constants.mind.WILL_NOT:
                remaining_moves.remove(my_move)

        return remaining_moves
