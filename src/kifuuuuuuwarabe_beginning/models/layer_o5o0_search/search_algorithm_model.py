import cshogi

from ..layer_o1o0 import constants, Mars, SquareModel
from ..layer_o2o0 import BackwardsPlotModel, cutoff_reason


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
