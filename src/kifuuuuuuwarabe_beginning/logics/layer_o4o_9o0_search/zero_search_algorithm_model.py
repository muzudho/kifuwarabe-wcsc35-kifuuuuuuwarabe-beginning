import time

from ...models.layer_o5o0_search.search_algorithm_model import SearchAlgorithmModel


class ZeroSearchAlgorithumModel(SearchAlgorithmModel):


    @staticmethod
    def search_before_entering_root_node(pv, search_context_model):
        """ルート・ノードに入る前に探索。

        Returns
        -------
        backwards_plot_model : BackwardsPlotModel
            読み筋。
        is_terminate : bool
            読み終わり。
        """

        ########################
        # MARK: 指す前にやること
        ########################

        search_context_model.start_time = time.time()          # 探索開始時間
        search_context_model.restart_time = search_context_model.start_time   # 前回の計測開始時間

        # 指さなくても分かること（ライブラリー使用）

        if search_context_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            return SearchAlgorithmModel.create_backwards_plot_model_at_game_over(search_context_model=search_context_model), True

        # 一手詰めを詰める
        if not search_context_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := search_context_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return SearchAlgorithmModel.create_backwards_plot_model_at_mate_move_in_1_ply(mate_move=mate_move, search_context_model=search_context_model), True

        if search_context_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言勝ち局面時。
            """
            return SearchAlgorithmModel.create_backwards_plot_model_at_nyugyoku_win(search_context_model=search_context_model), True

        return pv.backwards_plot_model, False
