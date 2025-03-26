import cshogi

from ..models_o1x import constants, SquareModel
from ..models_o2x import cutoff_reason, CutoffReason, PlotModel


class QuiescenceSearchForScrambleModel():
    """駒の取り合いのための静止探索。
    駒の取り合いが終わるまで、駒の取り合いを探索します。
    """


    def __init__(self, max_depth, gymnasium):
        """
        Parameters
        ----------
        gymnasium : GymnasiumModel
            体育館。        
        """
        self._max_depth = max_depth
        self._gymnasium = gymnasium
        self._number_of_visited_nodes = 0


    @property
    def number_of_visited_nodes(self):
        return self._number_of_visited_nodes
    

    # TODO 指し手の分析。駒を取る手と、そうでない手を分ける。
    # TODO 駒を取る手も、価値の高い駒から取る手を考える。（相手が手抜く勝手読みをすると、大きな駒を取れてしまうことがあるから）。
    # FIXME 将来的に相手の駒をポロリと取れるなら、手前の手は全部緩手になることがある。どう解消するか？
    """
    TODO 静止探索はせず、［スクランブル・サーチ］というのを考える。静止探索は王手が絡むと複雑だ。
    リーガル・ムーブのうち、
        手番の１手目なら：
            ［取られそうになっている駒を逃げる手］∪［駒を取る手］∪［利きに飛び込む手］に絞り込む。（１度調べた手は２度目は調べない）
            ［放置したとき］も調べる。
        相手番の１手目なら：
            ［動いた駒を取る手］に絞り込む。（１番安い駒から動かす）
        手番の２手目なら：
            ［動いた駒を取る手］に絞り込む。（１番安い駒から動かす）
        最後の評価値が、１手目の評価値。
    """
    def search_at_first(
            self,
            #best_plot_model_in_older_sibling,
            depth,
            is_absolute_opponent,
            remaining_moves):
        """
        Parameters
        ----------
        # best_plot_model_in_older_sibling : PlotModel
        #     兄たちの中で最善の読み筋、またはナン。ベータカットに使う。
        depth : int
            あと何手深く読むか。
        is_absolute_opponent : bool
            対戦相手か？
        remaining_moves : list<int>
            指し手のリスト。

        Returns
        -------
        best_prot_model : PlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        #print(f"[search_alice] {depth=} {is_absolute_opponent=}")

        all_plots_at_first = []

        ########################
        # MARK: 指す前にやること
        ########################

        # 指さなくても分かること（ライブラリー使用）

        if self._gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = PlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration         = constants.declaration.RESIGN,
                    is_mate_in_1_move   = False,
                    cutoff_reason       = cutoff_reason.GAME_OVER)
            all_plots_at_first.append(best_plot_model)
            return all_plots_at_first

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
                cap_pt = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

                best_plot_model = PlotModel(
                        is_absolute_opponent_at_end_position    = is_absolute_opponent,
                        declaration         = constants.declaration.NONE,
                        is_mate_in_1_move   = True,
                        cutoff_reason       = cutoff_reason.MATE_MOVE_IN_1_PLY)
            
                # 今回の手を付け加える。
                best_plot_model.append_move(
                        is_absolute_opponent    = is_absolute_opponent,
                        move                    = mate_move,
                        capture_piece_type      = cap_pt)

                all_plots_at_first.append(best_plot_model)
                return all_plots_at_first

        if self._gymnasium.table.is_nyugyoku():
            """手番の入玉宣言局面時。
            """
            best_plot_model = PlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration         = constants.declaration.NYUGYOKU_WIN,
                    is_mate_in_1_move   = False,
                    cutoff_reason       = cutoff_reason.NYUGYOKU_WIN)            
            all_plots_at_first.append(best_plot_model)
            return all_plots_at_first

        # これ以上深く読まない場合。
        if depth < 1:
            best_plot_model = PlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration         = constants.declaration.NONE,
                    is_mate_in_1_move   = False,
                    cutoff_reason       = cutoff_reason.MAX_DEPTH)
            all_plots_at_first.append(best_plot_model)
            return all_plots_at_first

        # まだ深く読む場合。

        ######################
        # MARK: 合法手スキャン
        ######################

        # 最善手は探さなくていい。全部返すから。

        # 指し手を全部調べる。
        for my_move in remaining_moves:

            ##################
            # MARK: 一手指す前
            ##################

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            is_capture  = (cap_pt != cshogi.NONE)

            # １階呼出時は、どの手も無視しません。
            if depth == self._max_depth:
                pass

            else:
                # ２階以降の呼出時は、駒を取る手でなければ無視。
                if not is_capture:
                    continue

            ################
            # MARK: 一手指す
            ################

            self._gymnasium.do_move_o1x(move = my_move)
            self._number_of_visited_nodes += 1

            ####################
            # MARK: 一手指した後
            ####################

            future_plot_model = self.search_alice(      # 再帰呼出
                    depth                               = depth - 1,                    # 深さを１下げる
                    is_absolute_opponent                = not is_absolute_opponent,     # 手番が逆になる
                    remaining_moves                     = list(self._gymnasium.table.legal_moves))  # 合法手全部。

            # １階呼出時は、必ず今回の手を付け加える。
            future_plot_model.append_move(
                    is_absolute_opponent    = is_absolute_opponent,
                    move                    = my_move,
                    capture_piece_type      = cap_pt)

            # １階呼出時は、全ての手の読み筋を記憶します。最善手は選びません。
            all_plots_at_first.append(future_plot_model)

            ################
            # MARK: 一手戻す
            ################

            self._gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            # ベータカットもしません。全部返すから。

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if len(all_plots_at_first) < 1:
            future_plot_model = PlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration         = constants.declaration.NONE,
                    is_mate_in_1_move   = False,
                    cutoff_reason       = cutoff_reason.NO_MOVES)
            all_plots_at_first.append(future_plot_model)

        return all_plots_at_first


    def search_alice(
            self,
            #best_plot_model_in_older_sibling,
            depth,
            is_absolute_opponent,
            remaining_moves):
        """
        Parameters
        ----------
        # best_plot_model_in_older_sibling : PlotModel
        #     兄たちの中で最善の読み筋、またはナン。ベータカットに使う。
        depth : int
            あと何手深く読むか。
        is_absolute_opponent : bool
            対戦相手か？
        remaining_moves : list<int>
            指し手のリスト。

        Returns
        -------
        best_prot_model : PlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        #print(f"[search_alice] {depth=} {is_absolute_opponent=}")

        ########################
        # MARK: 指す前にやること
        ########################

        # 指さなくても分かること（ライブラリー使用）

        if self._gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = PlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration         = constants.declaration.RESIGN,
                    is_mate_in_1_move   = False,
                    cutoff_reason       = cutoff_reason.GAME_OVER)

            return best_plot_model

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
                cap_pt = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

                best_plot_model = PlotModel(
                        is_absolute_opponent_at_end_position    = is_absolute_opponent,
                        declaration         = constants.declaration.NONE,
                        is_mate_in_1_move   = True,
                        cutoff_reason       = cutoff_reason.MATE_MOVE_IN_1_PLY)
            
                # 今回の手を付け加える。
                best_plot_model.append_move(
                        is_absolute_opponent    = is_absolute_opponent,
                        move                    = mate_move,
                        capture_piece_type      = cap_pt)

                return best_plot_model

        if self._gymnasium.table.is_nyugyoku():
            """手番の入玉宣言局面時。
            """
            best_plot_model = PlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration         = constants.declaration.NYUGYOKU_WIN,
                    is_mate_in_1_move   = False,
                    cutoff_reason       = cutoff_reason.NYUGYOKU_WIN)

            return best_plot_model

        # これ以上深く読まない場合。
        if depth < 1:
            return PlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration         = constants.declaration.NONE,
                    is_mate_in_1_move   = False,
                    cutoff_reason       = cutoff_reason.MAX_DEPTH)

        # まだ深く読む場合。

        ######################
        # MARK: 合法手スキャン
        ######################

        best_plot_model_in_children = None
        best_move = None
        best_move_cap_pt = None


        # def _get_beta_cutoff_value(is_absolute_opponent, best_plot_model_in_older_sibling):
        #     # 最善手が未定なら、天井（底）を最大にします。
        #     if best_plot_model_in_older_sibling is None:
        #         if is_absolute_opponent:
        #             return constants.value.BETA_CUTOFF_VALUE        # 天井
        #         return - constants.value.BETA_CUTOFF_VALUE  # 底

        #     # 最善手が既存なら、その交換値を返すだけ。
        #     return best_plot_model_in_older_sibling.last_piece_exchange_value


        # 指し手を全部調べる。
        for my_move in remaining_moves:

            ##################
            # MARK: 一手指す前
            ##################

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            is_capture  = (cap_pt != cshogi.NONE)

            # １階呼出時は、どの手も無視しません。
            if depth == self._max_depth:
                pass

            else:
                # ２階以降の呼出時は、駒を取る手でなければ無視。
                if not is_capture:
                    continue

            ################
            # MARK: 一手指す
            ################

            self._gymnasium.do_move_o1x(move = my_move)
            self._number_of_visited_nodes += 1

            ####################
            # MARK: 一手指した後
            ####################

            future_plot_model = self.search_alice(      # 再帰呼出
                    #best_plot_model_in_older_sibling    = best_plot_model_in_children,
                    depth                               = depth - 1,                    # 深さを１下げる
                    is_absolute_opponent                = not is_absolute_opponent,     # 手番が逆になる
                    remaining_moves                     = list(self._gymnasium.table.legal_moves))  # 合法手全部。

            # NOTE （スクランブル・サーチでは）ベストがナンということもある。つまり、指さない方がマシな局面がある（のが投了との違い）。
            threshold_value = 0     # 閾値
            if best_plot_model_in_children is not None:
                threshold_value = best_plot_model_in_children.last_piece_exchange_value     # とりあえず最善の点数。

            # 最大深さで戻ってきたなら、最善手ではありません。無視します。
            #print(f"D-368: {future_plot_model.cutoff_reason=} {cutoff_reason.MAX_DEPTH=} {future_plot_model.move_list_length()=} {future_plot_model.is_empty_moves()=}")
            if future_plot_model.cutoff_reason == cutoff_reason.MAX_DEPTH and future_plot_model.is_empty_moves():
                #print(f"D-370: ベストではない")
                its_best = False

            # 自分は、点数が大きくなる手を選ぶ
            elif not is_absolute_opponent:
                # # TODO ただし、既存の最善手より良い手を見つけてしまったら、ベータカットします。
                # if beta_cutoff_value < future_plot_model.last_piece_exchange_value:
                #     #will_beta_cutoff = True   # TODO ベータカット
                #     pass

                # 最善より良い手があれば、そっちを選びます。
                its_best = (threshold_value < future_plot_model.last_piece_exchange_value)

            # 相手は、点数が小さくなる手を選ぶ
            else:
                # # TODO ただし、既存の最悪手より悪い手を見つけてしまったら、ベータカットします。
                # if future_plot_model.last_piece_exchange_value < beta_cutoff_value:
                #     #will_beta_cutoff = True   # TODO ベータカット
                #     pass

                # 最善より悪い手があれば、そっちを選びます。
                its_best = (future_plot_model.last_piece_exchange_value < threshold_value)
                    
            if its_best:
                best_plot_model_in_children = future_plot_model
                best_move = my_move
                best_move_cap_pt = cap_pt

            ################
            # MARK: 一手戻す
            ################

            self._gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            # # FIXME 探索の打切り判定
            # if is_beta_cutoff:
            #     break   # （アンドゥや、depth の勘定をきちんとしたあとで）ループから抜ける

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面を返す。
        if best_plot_model_in_children is None:
            return PlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration         = constants.declaration.NONE,
                    is_mate_in_1_move   = False,
                    cutoff_reason       = cutoff_reason.NO_MOVES)

        # 今回の手を付け加える。
        best_plot_model_in_children.append_move(
                is_absolute_opponent    = is_absolute_opponent,
                move                    = best_move,
                capture_piece_type      = best_move_cap_pt)

        return best_plot_model_in_children
