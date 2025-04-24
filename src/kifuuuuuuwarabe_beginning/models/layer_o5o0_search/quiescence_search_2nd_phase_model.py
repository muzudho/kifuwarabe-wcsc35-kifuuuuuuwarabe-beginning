import cshogi
import time

from ...logics.layer_o1o0 import MoveListLogics
from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import constants, Mars, PtolemaicTheoryModel, SquareModel
from ..layer_o1o0o_9o0_table_helper import TableHelper
from ..layer_o2o0 import BackwardsPlotModel, cutoff_reason
from ..layer_o4o0_rules.negative import DoNotDepromotionModel


class QuiescenceSearch2ndPhaseModel():
    """駒の取り合いのための静止探索。
    駒の取り合いが終わるまで、駒の取り合いを探索します。
    """


    def __init__(self, search_model):
        """
        Parameters
        ----------
        search_model : SearchModel
            探索モデル。        
        """
        self._search_model = search_model


    @property
    def search_model(self):
        return self._search_model
    

    def search_alice(
            self,
            #best_plot_model_in_older_sibling,
            depth,
            parent_move):
        """
        Parameters
        ----------
        # best_plot_model_in_older_sibling : BackwardsPlotModel
        #     兄たちの中で最善の読み筋、またはナン。ベータカットに使う。
        depth : int
            あと何手深く読むか。
        parent_move : int
            １手前の手。

        Returns
        -------
        best_prot_model : BackwardsPlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        ########################
        # MARK: 指す前にやること
        ########################

        cur_time = time.time()                                          # 現在の時間
        erapsed_seconds = cur_time - self._search_model.restart_time    # 経過秒
        if 4 <= erapsed_seconds:                                        # 4秒以上経過してたら、情報出力
            print(f"info depth {self._search_model.max_depth - depth} seldepth 0 time 1 nodes {self.search_model.number_of_visited_nodes} score cp 0 string thinking")
            self.search_model.restart_time = cur_time                   # 前回の計測時間を更新

        # 指さなくても分かること（ライブラリー使用）

        if self.search_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = BackwardsPlotModel(
                    is_mars_at_out_of_termination  = self._search_model.gymnasium.is_mars,
                    is_gote_at_out_of_termination  = self._search_model.gymnasium.table.is_gote,
                    out_of_termination             = constants.out_of_termination.RESIGN,
                    cutoff_reason           = cutoff_reason.GAME_OVER,
                    hint                    = '手番の投了局面時２')
            self._search_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')
            return best_plot_model

        # 一手詰めを詰める
        if not self.search_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self.search_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
                cap_pt = self.search_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

                best_plot_model = BackwardsPlotModel(
                        is_mars_at_out_of_termination  = not self._search_model.gymnasium.is_mars,     # ［詰む］のは、もう１手先だから。
                        is_gote_at_out_of_termination  = self._search_model.gymnasium.table.is_gote,
                        out_of_termination             = constants.out_of_termination.RESIGN,
                        cutoff_reason           = cutoff_reason.MATE_MOVE_IN_1_PLY,
                        hint                    = '一手詰め時B')
            
                # 今回の手を付け加える。
                best_plot_model.append_move(
                        move                = mate_move,
                        capture_piece_type  = cap_pt,
                        hint                = f"{Mars.japanese(self._search_model.gymnasium.is_mars)}の一手詰め時")
                self._search_model.gymnasium.health_check_qs_model.append_node(f"＜一手詰め＞{cshogi.move_to_usi(mate_move)}")
                self._search_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')
                return best_plot_model

        if self.search_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言勝ち局面時。
            """
            best_plot_model = BackwardsPlotModel(
                    is_mars_at_out_of_termination  = self._search_model.gymnasium.is_mars,
                    is_gote_at_out_of_termination  = self._search_model.gymnasium.table.is_gote,
                    out_of_termination             = constants.out_of_termination.NYUGYOKU_WIN,
                    cutoff_reason           = cutoff_reason.NYUGYOKU_WIN,
                    hint                    = '手番の入玉宣言勝ち局面時２')
            self._search_model.gymnasium.health_check_qs_model.on_out_of_termination('＜入玉宣言勝ち＞')
            return best_plot_model

        # これ以上深く読まない場合。
        if depth < 1:
            # 末端局面。
            self._search_model.gymnasium.health_check_qs_model.on_out_of_termination('＜水平線＞')
            return BackwardsPlotModel(
                    is_mars_at_out_of_termination  = self._search_model.gymnasium.is_mars,
                    is_gote_at_out_of_termination  = self._search_model.gymnasium.table.is_gote,
                    out_of_termination             = constants.out_of_termination.MAX_DEPTH_BY_THINK,
                    cutoff_reason           = cutoff_reason.MAX_DEPTH,      # ［最大探索深さ］が打切り理由。
                    hint                    = f"{self._search_model.max_depth - depth}階の{Mars.japanese(self._search_model.gymnasium.is_mars)}でこれ以上深く読まない場合_{depth=}/{self._search_model.max_depth=}")

        # まだ深く読む場合。

        ######################
        # MARK: 合法手スキャン
        ######################

        best_old_sibling_plot_model_in_children = None
        best_move           = None
        best_move_cap_pt    = None
        depth_extend        = 0


        # def _get_beta_cutoff_value(best_plot_model_in_older_sibling):
        #     # 最善手が未定なら、天井（底）を最大にします。
        #     if best_plot_model_in_older_sibling is None:
        #         if self._search_model.gymnasium.is_mars:
        #             return constants.value.BETA_CUTOFF_VALUE        # 天井
        #         return - constants.value.BETA_CUTOFF_VALUE  # 底

        #     # 最善手が既存なら、その交換値を返すだけ。
        #     return best_plot_model_in_older_sibling.get_exchange_value_on_earth()


        case_2 = 0
        case_4 = 0
        case_5 = 0
        case_6t = 0
        case_6t_hint_list = []
        case_6f = 0
        case_6f_hint_list = []
        case_8a = 0
        case_8b = 0
        case_8c = 0
        case_8d = 0
        case_8e = 0

        # 合法手を全部調べる。
        do_not_depromotion_model = DoNotDepromotionModel(
                basketball_court_model=self._search_model.gymnasium.basketball_court_model)    # TODO 号令［成らないということをするな］

        do_not_depromotion_model._on_node_entry_negative(
                table=self._search_model.gymnasium.table)

        legal_move_list = list(self.search_model.gymnasium.table.legal_moves)

        remaining_moves = legal_move_list
        # TODO 安い駒から交換したい。
        # remaining_moves = MoveListLogics.when_replacing_pieces_start_with_the_cheaper_ones(
        #         move_list   = legal_move_list,
        #         gymnasium   = self._search_model.gymnasium)

        ############################
        # MARK: データ・クリーニング
        ############################

        def filtering_same_destination_move_list(remaining_moves):
            """［同］（１つ前の手の移動先に移動する手）を優先的に選ぶ。
            """
            dst_sq_of_previous_move_obj = SquareModel(cshogi.move_to(parent_move))      # ［１つ前の手］の［移動先マス］
            same_destination_move_list = []

            for my_move in remaining_moves:
                dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
                if dst_sq_obj.sq == dst_sq_of_previous_move_obj.sq:
                    same_destination_move_list.append(my_move)
            
            if 0 < len(same_destination_move_list):
                return same_destination_move_list
            
            return remaining_moves


        remaining_moves = filtering_same_destination_move_list(remaining_moves=remaining_moves)

        for my_move in reversed(remaining_moves):
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self.search_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            is_capture  = (cap_pt != cshogi.NONE)

            # ２階以降の呼出時は、駒を取る手でなければ無視。
            if not is_capture:
                # ＜📚原則２＞ 王手は（駒を取らない手であっても）探索を続け、深さを１手延長する。
                if self.search_model.gymnasium.table.is_check():
                    #depth_extend += 1  # FIXME 探索が終わらないくなる。
                    pass

                else:
                    remaining_moves.remove(my_move)
                    continue

            # ［成れるのに成らない手］は除外
            mind = do_not_depromotion_model._on_node_exit_negative(
                    move    = my_move,
                    table   = self._search_model.gymnasium.table)
            if mind == constants.mind.WILL_NOT:
                remaining_moves.remove(my_move)
                continue

        # ［駒を取る手］がないことを、［静止］と呼ぶ。
        if len(remaining_moves) == 0:
            self._search_model.gymnasium.health_check_qs_model.on_out_of_termination('＜静止＞')
            return BackwardsPlotModel(
                    is_mars_at_out_of_termination  = self._search_model.gymnasium.is_mars,
                    is_gote_at_out_of_termination  = self._search_model.gymnasium.table.is_gote,
                    out_of_termination             = constants.out_of_termination.QUIESCENCE,
                    cutoff_reason           = cutoff_reason.NO_MOVES,
                    hint                    = f"{self._search_model.max_depth - depth + 1}階の{Mars.japanese(self._search_model.gymnasium.is_mars)}は静止")

        for my_move in remaining_moves:

            ##################
            # MARK: 一手指す前
            ##################

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self.search_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            #is_capture  = (cap_pt != cshogi.NONE)

            # # ２階以降の呼出時は、駒を取る手でなければ無視。
            # if not is_capture:
            #     # ＜📚原則２＞ 王手は（駒を取らない手であっても）探索を続け、深さを１手延長する。
            #     if self.search_model.gymnasium.table.is_check():
            #         #depth_extend += 1  # FIXME 探索が終わらないくなる。
            #         pass

            #     else:
            #         continue

            ################
            # MARK: 一手指す
            ################

            self.search_model.gymnasium.do_move_o1x(move = my_move)
            self._search_model.number_of_visited_nodes += 1

            ####################
            # MARK: 一手指した後
            ####################

            depth       = depth - 1     # 深さを１下げる。
            self._search_model.frontwards_plot_model.append_move(
                    move    = my_move,
                    cap_pt  = cap_pt)
            self._search_model.gymnasium.health_check_qs_model.append_node(cshogi.move_to_usi(my_move))

            ####################
            # MARK: 相手番の処理
            ####################

            # NOTE ネガ・マックスではないので、評価値の正負を反転させなくていい。
            child_plot_model = self.search_alice(      # 再帰呼出
                    #best_plot_model_in_older_sibling    = best_plot_model_in_children,
                    depth       = depth + depth_extend,
                    parent_move = my_move)

            ################
            # MARK: 一手戻す
            ################

            self.search_model.gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            depth       = depth + 1                 # 深さを１上げる。
            ptolemaic_theory_model  = PtolemaicTheoryModel(
                    is_mars=self._search_model.gymnasium.is_mars)
            self._search_model.frontwards_plot_model.pop_move()
            self._search_model.gymnasium.health_check_qs_model.pop_node()

            ##################
            # MARK: 手番の処理
            ##################

            its_update_best = False

            # NOTE `earth` - 自分。 `mars` - 対戦相手。
            piece_exchange_value_on_earth = PieceValuesModel.get_piece_exchange_value_on_earth(      # 交換値に変換。正の数とする。
                    pt          = cap_pt,
                    is_mars     = self._search_model.gymnasium.is_mars)

            # この枝の点（将来の点＋取った駒の点）
            this_branch_value_on_earth = child_plot_model.get_exchange_value_on_earth() + piece_exchange_value_on_earth

            # # TODO 既存の最善手より良い手を見つけてしまったら、ベータカットします。
            # if beta_cutoff_value < this_branch_value:
            #     #will_beta_cutoff = True   # TODO ベータカット
            #     pass

            # この枝が長兄なら。
            if best_old_sibling_plot_model_in_children is None:
                old_sibling_value = 0
            else:
                # 兄枝のベスト評価値
                old_sibling_value = best_old_sibling_plot_model_in_children.get_exchange_value_on_earth()     # とりあえず最善の読み筋の点数。


            (a, b) = ptolemaic_theory_model.swap(old_sibling_value, this_branch_value_on_earth)
            its_update_best = (a < b)

            # # この枝が長兄なら。
            # if best_old_sibling_plot_model_in_children is None:

            #     if its_update_best:
            #         case_8a += 1
            
            # # 兄枝が有るなら。
            # else:

            #     if its_update_best:
            #         case_6t += 1
            #         case_6t_hint_list.append(f"{old_sibling_value=} < {this_branch_value_on_earth=}")

            #         #self.search_model.gymnasium.thinking_logger_module.append(f"[search] 6t {self._search_model.frontwards_plot_model=}")
            #         # if self._search_model.frontwards_plot_model.equals_move_usi_list(['3a4b']):   # FIXME デバッグ絞込み
            #         #     self.search_model.gymnasium.thinking_logger_module.append(_log_1('6t'))

            #     else:
            #         case_6f += 1
            #         case_6f_hint_list.append(f"{old_sibling_value=} < {this_branch_value_on_earth=}")

            #         #self.search_model.gymnasium.thinking_logger_module.append(f"[search] 6f {self._search_model.frontwards_plot_model=}")
            #         # if self._search_model.frontwards_plot_model.equals_move_usi_list(['3a4b']):   # FIXME デバッグ絞込み
            #         #     self.search_model.gymnasium.thinking_logger_module.append(_log_1('6f'))
                        
            # 最善手の更新
            if its_update_best:
                best_old_sibling_plot_model_in_children = child_plot_model
                best_move = my_move
                best_move_cap_pt = cap_pt

            # # FIXME 探索の打切り判定
            # if is_beta_cutoff:
            #     break   # （アンドゥや、depth の勘定をきちんとしたあとで）ループから抜ける

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面を返す。
        if best_old_sibling_plot_model_in_children is None:
            self._search_model.gymnasium.health_check_qs_model.on_out_of_termination('＜指したい手無し＞')
            return BackwardsPlotModel(
                    is_mars_at_out_of_termination  = self._search_model.gymnasium.is_mars,
                    is_gote_at_out_of_termination  = self._search_model.gymnasium.table.is_gote,
                    out_of_termination             = constants.out_of_termination.NO_CANDIDATES,  # 有力な候補手無し。
                    cutoff_reason           = cutoff_reason.NO_MOVES,
                    hint                    = f"{self._search_model.max_depth - depth + 1}階の{Mars.japanese(self._search_model.gymnasium.is_mars)}は指したい手無し,move数={len(legal_move_list)},{case_2=},{case_4=},{case_5=},{case_6t=},({'_'.join(case_6t_hint_list)}),{case_6f=},({'_'.join(case_6f_hint_list)}),{case_8a=},{case_8a=},{case_8b=},{case_8c=},{case_8d=},{case_8e=}")

        # 今回の手を付け加える。
        best_old_sibling_plot_model_in_children.append_move(
                move                = best_move,
                capture_piece_type  = best_move_cap_pt,
                hint                = f"{self._search_model.max_depth - depth + 1}階の{Mars.japanese(self._search_model.gymnasium.is_mars)}の手記憶")

        return best_old_sibling_plot_model_in_children
