import cshogi
import time

from ..models_o1x import AbsoluteOpponent, constants, PieceValuesModel, SquareModel
from ..models_o2x import BackwardsPlotModel, cutoff_reason, FrontwardsPlotModel


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
        self._start_time = None
        self._restart_time = None
        self._end_time = None
        self._move_list_for_debug = FrontwardsPlotModel()  # デバッグ用に手を記憶。


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
        # best_plot_model_in_older_sibling : BackwardsPlotModel
        #     兄たちの中で最善の読み筋、またはナン。ベータカットに使う。
        depth : int
            あと何手深く読むか。
        is_absolute_opponent : bool
            対戦相手か？
        remaining_moves : list<int>
            指し手のリスト。

        Returns
        -------
        best_prot_model : BackwardsPlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        self._start_time = time.time()          # 探索開始時間
        self._restart_time = self._start_time   # 前回の計測開始時間
        all_plots_at_first = []

        ########################
        # MARK: 指す前にやること
        ########################

        # 指さなくても分かること（ライブラリー使用）

        # NOTE このあたりは［０階］。max_depth - depth。
        if self._gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = BackwardsPlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration                             = constants.declaration.RESIGN,
                    is_mate_in_1_move                       = False,
                    cutoff_reason                           = cutoff_reason.GAME_OVER,
                    hint                                    = '手番の投了局面時１')
            all_plots_at_first.append(best_plot_model)
            return all_plots_at_first

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
                cap_pt = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

                best_plot_model = BackwardsPlotModel(
                        is_absolute_opponent_at_end_position    = is_absolute_opponent,
                        declaration                             = constants.declaration.NONE,
                        is_mate_in_1_move                       = True,
                        cutoff_reason                           = cutoff_reason.MATE_MOVE_IN_1_PLY,
                        hint                                    = '一手詰め１')
            
                # 今回の手を付け加える。
                best_plot_model.append_move(
                        is_absolute_opponent    = is_absolute_opponent,
                        move                    = mate_move,
                        capture_piece_type      = cap_pt,
                        hint                    = f"一手詰め１_{is_absolute_opponent=}")

                all_plots_at_first.append(best_plot_model)
                return all_plots_at_first

        if self._gymnasium.table.is_nyugyoku():
            """手番の入玉宣言局面時。
            """
            best_plot_model = BackwardsPlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration                             = constants.declaration.NYUGYOKU_WIN,
                    is_mate_in_1_move                       = False,
                    cutoff_reason                           = cutoff_reason.NYUGYOKU_WIN,
                    hint                                    = '手番の入玉宣言局面時１')
            all_plots_at_first.append(best_plot_model)
            return all_plots_at_first

        # これ以上深く読まない場合。
        if depth < 1:
            best_plot_model = BackwardsPlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration                             = constants.declaration.NONE,
                    is_mate_in_1_move                       = False,
                    cutoff_reason                           = cutoff_reason.MAX_DEPTH,
                    hint                                    = 'これ以上深く読まない場合１')
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

            # １階呼出時は、どの手も無視しません。

            ################
            # MARK: 一手指す
            ################

            self._gymnasium.do_move_o1x(move = my_move)

            ####################
            # MARK: 一手指した後
            ####################

            self._move_list_for_debug.append_move(my_move)      # デバッグ用に手を記憶
            self._number_of_visited_nodes   += 1
            depth                           -= 1                            # 深さを１下げる。
            is_absolute_opponent            = not is_absolute_opponent      # 手番が逆になる。

            ####################
            # MARK: 相手番の処理
            ####################

            # NOTE この辺りは［１階］。max_depth - depth。
            future_plot_model = self.search_alice(      # 再帰呼出
                    depth                               = depth,
                    is_absolute_opponent                = is_absolute_opponent)

            ################
            # MARK: 一手戻す
            ################

            self._gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            self._move_list_for_debug.pop_move()                         # デバッグ用に手を記憶
            depth                   += 1                            # 深さを１上げる。
            is_absolute_opponent    = not is_absolute_opponent      # 手番が逆になる。

            ##################
            # MARK: 手番の処理
            ##################

            # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
            future_plot_model.append_move(
                    is_absolute_opponent    = is_absolute_opponent,
                    move                    = my_move,
                    capture_piece_type      = cap_pt,
                    hint                    = f"１階の手はなんでも記憶_{is_absolute_opponent=}")
            all_plots_at_first.append(future_plot_model)

            # NOTE この辺りは［０階］。

            # ベータカットもしません。全部返すから。

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if len(all_plots_at_first) < 1:
            future_plot_model = BackwardsPlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration                             = constants.declaration.NONE,
                    is_mate_in_1_move                       = False,
                    cutoff_reason                           = cutoff_reason.NO_MOVES,
                    hint                                    = f"指したい１階の手無し_{depth=}/{self._max_depth=}_{is_absolute_opponent}_{len(all_plots_at_first)=}/{len(remaining_moves)=}")
            all_plots_at_first.append(future_plot_model)

        self._end_time = time.time()    # 計測終了時間

        return all_plots_at_first


    def search_alice(
            self,
            #best_plot_model_in_older_sibling,
            depth,
            is_absolute_opponent):
        """
        Parameters
        ----------
        # best_plot_model_in_older_sibling : BackwardsPlotModel
        #     兄たちの中で最善の読み筋、またはナン。ベータカットに使う。
        depth : int
            あと何手深く読むか。
        is_absolute_opponent : bool
            対戦相手か？

        Returns
        -------
        best_prot_model : BackwardsPlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        ########################
        # MARK: 指す前にやること
        ########################

        cur_time = time.time()                              # 現在の時間
        erapsed_seconds = cur_time - self._restart_time     # 経過秒
        if 4 <= erapsed_seconds:                            # 4秒以上経過してたら、情報出力
            print(f"info depth {self._max_depth - depth} seldepth 0 time 1 nodes {self._number_of_visited_nodes} score cp 0 string thinking")
            self._restart_time = cur_time                   # 前回の計測時間を更新


        # 指さなくても分かること（ライブラリー使用）

        if self._gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = BackwardsPlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration                             = constants.declaration.RESIGN,
                    is_mate_in_1_move                       = False,
                    cutoff_reason                           = cutoff_reason.GAME_OVER,
                    hint                                    = '手番の投了局面時２')

            return best_plot_model

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
                cap_pt = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

                best_plot_model = BackwardsPlotModel(
                        is_absolute_opponent_at_end_position    = is_absolute_opponent,
                        declaration                             = constants.declaration.NONE,
                        is_mate_in_1_move                       = True,
                        cutoff_reason                           = cutoff_reason.MATE_MOVE_IN_1_PLY,
                        hint                                    = '一手詰め時２')
            
                # 今回の手を付け加える。
                best_plot_model.append_move(
                        is_absolute_opponent    = is_absolute_opponent,
                        move                    = mate_move,
                        capture_piece_type      = cap_pt,
                        hint                    = f"一手詰め時２_{is_absolute_opponent=}")

                return best_plot_model

        if self._gymnasium.table.is_nyugyoku():
            """手番の入玉宣言局面時。
            """
            best_plot_model = BackwardsPlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration                             = constants.declaration.NYUGYOKU_WIN,
                    is_mate_in_1_move                       = False,
                    cutoff_reason                           = cutoff_reason.NYUGYOKU_WIN,
                    hint                                    = '手番の入玉宣言局面時２')

            return best_plot_model

        # これ以上深く読まない場合。
        if depth < 1:
            # 末端局面。
            return BackwardsPlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration                             = constants.declaration.NONE,   # ［宣言］ではない。
                    is_mate_in_1_move                       = False,                        # ［一手詰め］ではない。
                    cutoff_reason                           = cutoff_reason.MAX_DEPTH,      # ［最大探索深さ］が打切り理由。
                    hint                                    = f"{self._max_depth - depth}階でこれ以上深く読まない場合_{depth=}/{self._max_depth=}_{is_absolute_opponent=}")

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
        #     return best_plot_model_in_older_sibling.last_piece_exchange_value_on_earth

        case_1 = 0
        case_2 = 0
        case_3 = 0
        case_4 = 0
        case_5 = 0
        case_6t = 0
        case_6t_hint_list = []
        case_6f = 0
        case_6f_hint_list = []
        case_7t = 0
        case_7f = 0
        case_8 = 0

        # 合法手を全部調べる。
        legal_move_list = list(self._gymnasium.table.legal_moves)
        for my_move in legal_move_list:

            ##################
            # MARK: 一手指す前
            ##################

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            is_capture  = (cap_pt != cshogi.NONE)

            # ２階以降の呼出時は、駒を取る手でなければ無視。 FIXME 王手が絡んでいるとき、取れないこともあるから、王手が絡むときは場合分けしたい。
            if not is_capture:
                case_1 += 1
                continue

            ################
            # MARK: 一手指す
            ################

            self._gymnasium.do_move_o1x(move = my_move)
            self._number_of_visited_nodes += 1

            ####################
            # MARK: 一手指した後
            ####################

            self._move_list_for_debug.append_move(my_move)           # デバッグ用に手を記憶
            depth                   = depth - 1                 # 深さを１下げる。
            is_absolute_opponent    = not is_absolute_opponent  # 手番が逆になる。

            ####################
            # MARK: 相手番の処理
            ####################

            # NOTE ネガ・マックスではないので、評価値の正負を反転させなくていい。
            future_plot_model = self.search_alice(      # 再帰呼出
                    #best_plot_model_in_older_sibling    = best_plot_model_in_children,
                    depth                               = depth,
                    is_absolute_opponent                = is_absolute_opponent)

            ################
            # MARK: 一手戻す
            ################

            self._gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            self._move_list_for_debug.pop_move()                     # デバッグ用に手を記憶
            depth                   = depth + 1                 # 深さを１上げる。
            is_absolute_opponent    = not is_absolute_opponent  # 手番が逆になる。

            ##################
            # MARK: 手番の処理
            ##################

            its_update_best = False

            # NOTE `earth` - 自分。 `mars` - 対戦相手。
            piece_exchange_value_on_earth = PieceValuesModel.get_piece_exchange_value(      # 交換値に変換。正の数とする。
                    pt                      = cap_pt,
                    is_absolute_opponent    = is_absolute_opponent)

            # 最大深さで戻ってきたなら、最善手ではありません。無視します。
            #print(f"D-368: {future_plot_model.cutoff_reason=} {cutoff_reason.MAX_DEPTH=} {future_plot_model.move_list_length()=} {future_plot_model.is_empty_moves()=}")
            if future_plot_model.is_empty_moves():  # ［宣言］などには［指し手］は含まれません。［指し手のリスト］は空なので、アクセスを避けるようにします。

                # 兄枝のベスト評価値
                old_sibling_value = constants.value.ZERO    # NOTE （スクランブル・サーチでは）ベストがナンということもある。つまり、指さない方がマシな局面がある（のが投了との違い）。
                if best_plot_model_in_children is not None and not best_plot_model_in_children.is_empty_moves():
                    old_sibling_value = best_plot_model_in_children.last_piece_exchange_value_on_earth     # とりあえず最善の読み筋の点数。

                if (
                        future_plot_model.cutoff_reason == cutoff_reason.MAX_DEPTH      # 探索打切り理由は、［最大探索深さ］。
                    or  future_plot_model.cutoff_reason == cutoff_reason.NO_MOVES       # 探索打切り理由は、［指したい手なし］（駒を取り返す手がないなど）。
                ):
                    #print(f"D-370: ベストではない")
                    # 相手が指し返してこなかったということは、自分が指した手が末端局面。
                    # 取った駒の交換値が、そのまま評価値になる。
                    this_branch_value = piece_exchange_value_on_earth

                    # とりあえず、自分と対戦相手で処理を分ける。
                    if not is_absolute_opponent:    # 自分。点数が大きくなる手を選ぶ。
                        # # TODO ただし、既存の最善手より良い手を見つけてしまったら、ベータカットします。
                        # if beta_cutoff_value < this_branch_value:
                        #     #will_beta_cutoff = True   # TODO ベータカット
                        #     pass

                        # （初期値の０または）最善より良い手があれば、そっちを選びます。
                        its_update_best = (old_sibling_value < this_branch_value)
                        case_2 += 1

                    else:   # 対戦相手。点数が小さくなる手を選ぶ。
                        # # TODO ただし、既存の最悪手より悪い手を見つけてしまったら、ベータカットします。
                        # if this_branch_value < beta_cutoff_value:
                        #     #will_beta_cutoff = True   # TODO ベータカット
                        #     pass

                        # （初期値の０または）最善より悪い手があれば、そっちを選びます。
                        its_update_best = (this_branch_value < old_sibling_value)
                        case_3 += 1

                # 相手が投了なら、自分には最善手。
                elif future_plot_model.declaration == constants.declaration.RESIGN:
                    its_update_best = True
                    case_4 += 1

                # 相手が入玉宣言勝ちなら、自分には最悪手。
                elif future_plot_model.declaration == constants.declaration.NYUGYOKU_WIN:
                    case_5 += 1
                    # TODO 最悪手というフラグを立てれないか？

                else:
                    # FIXME 指したい手なし
                    # ValueError: 想定外の読み筋 self._is_absolute_opponent_at_end_position=False self._declaration=0 self._is_mate_in_1_move=False self._move_list=[] self._cap_list=[] self._piece_exchange_value_list=[] self._cutoff_reason=4
                    raise ValueError(f"想定外の読み筋 {future_plot_model.stringify_dump()}")
            
            # 指し手がある。
            else:

                # 最善手がまだ無いなら。
                if best_plot_model_in_children is not None:
                    # 問答無用で良し悪しを最善手として回答。この最善手が最終的に即採用されるというわけではない。
                    case_8 += 1
                    its_update_best = True
                    #case_8_hint_list.append(f"{old_sibling_value=} < {this_branch_value=}")
                    
                else:


                    def _log_1(case_1):
                        return f"[search] {case_1} {depth=}/{self._max_depth=} {AbsoluteOpponent.japanese(is_absolute_opponent)} {self.stringify()},{cshogi.move_to_usi(my_move)}(私{this_branch_value}) {old_sibling_value=} < {future_plot_model.stringify()=}"

                    # とりあえず、自分と対戦相手で処理を分ける。
                    if not is_absolute_opponent:    # 自分。点数が大きくなる手を選ぶ。
                        # 兄枝のベスト評価値
                        old_sibling_value = constants.value.ZERO    # NOTE （スクランブル・サーチでは）ベストがナンということもある。つまり、指さない方がマシな局面がある（のが投了との違い）。
                        if best_plot_model_in_children is not None and not best_plot_model_in_children.is_empty_moves():
                            old_sibling_value = best_plot_model_in_children.last_piece_exchange_value_on_earth     # とりあえず最善の読み筋の点数。

                        this_branch_value = future_plot_model.last_piece_exchange_value_on_earth + piece_exchange_value_on_earth

                        # # TODO ただし、既存の最善手より良い手を見つけてしまったら、ベータカットします。
                        # if beta_cutoff_value < this_branch_value:
                        #     #will_beta_cutoff = True   # TODO ベータカット
                        #     pass

                        its_update_best = (old_sibling_value < this_branch_value)
                        if its_update_best:
                            case_6t += 1
                            case_6t_hint_list.append(f"{old_sibling_value=} < {this_branch_value=}")

                            #self._gymnasium.thinking_logger_module.append(f"[search] 6t {self._move_list_for_debug=}")
                            # if self._move_list_for_debug.equals_move_usi_list(['3a4b']):   # FIXME デバッグ絞込み
                            #     self._gymnasium.thinking_logger_module.append(_log_1('6t'))

                        else:
                            case_6f += 1
                            case_6f_hint_list.append(f"{old_sibling_value=} < {this_branch_value=}")

                            #self._gymnasium.thinking_logger_module.append(f"[search] 6f {self._move_list_for_debug=}")
                            # if self._move_list_for_debug.equals_move_usi_list(['3a4b']):   # FIXME デバッグ絞込み
                            #     self._gymnasium.thinking_logger_module.append(_log_1('6f'))

                    else:   # 対戦相手。点数が小さくなる手を選ぶ。
                        # 兄枝のベスト評価値
                        #       TODO ０点以上の手があり、最善手がまだ無ければ、０点以上の手を選びたい。

                        old_sibling_value = constants.value.ZERO    # NOTE （スクランブル・サーチでは）ベストがナンということもある。つまり、指さない方がマシな局面がある（のが投了との違い）。
                        if best_plot_model_in_children is not None and not best_plot_model_in_children.is_empty_moves():
                            old_sibling_value = best_plot_model_in_children.last_piece_exchange_value_on_earth     # とりあえず最善の読み筋の点数。

                        this_branch_value = future_plot_model.last_piece_exchange_value_on_earth + piece_exchange_value_on_earth

                        # # TODO ただし、既存の最悪手より悪い手を見つけてしまったら、ベータカットします。
                        # if this_branch_value < beta_cutoff_value:
                        #     #will_beta_cutoff = True   # TODO ベータカット
                        #     pass

                        # 最善より悪い手があれば、そっちを選びます。
                        #       NOTE １件に絞り込んでいいのか？ 後ろ向き探索なら１件に絞り込んでいいのか？
                        its_update_best = (this_branch_value < old_sibling_value)
                        if its_update_best:
                            case_7t += 1

                            #self._gymnasium.thinking_logger_module.append(f"[search] 7t {self._move_list_for_debug=}")
                            # if self._move_list_for_debug.equals_move_usi_list(['3a4b']):   # FIXME デバッグ絞込み
                            #     self._gymnasium.thinking_logger_module.append(_log_1('7t'))

                        # 対戦相手は、最善以上の手は選びません。
                        else:
                            case_7f += 1

                            #self._gymnasium.thinking_logger_module.append(f"[search] 7f {self._move_list_for_debug=}")
                            # if self._move_list_for_debug.equals_move_usi_list(['3a4b']):   # FIXME デバッグ絞込み
                            #     self._gymnasium.thinking_logger_module.append(_log_1('7f'))
                        
            # 最善手の更新
            if its_update_best:
                best_plot_model_in_children = future_plot_model
                best_move = my_move
                best_move_cap_pt = cap_pt

            # # FIXME 探索の打切り判定
            # if is_beta_cutoff:
            #     break   # （アンドゥや、depth の勘定をきちんとしたあとで）ループから抜ける

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面を返す。
        if best_plot_model_in_children is None:
            return BackwardsPlotModel(
                    is_absolute_opponent_at_end_position    = is_absolute_opponent,
                    declaration                             = constants.declaration.NONE,
                    is_mate_in_1_move                       = False,
                    cutoff_reason                           = cutoff_reason.NO_MOVES,
                    hint                                    = f"指したい{self._max_depth - depth + 1}階の手無し,敵={is_absolute_opponent},move数={len(legal_move_list)},{case_1=},{case_2=},{case_3=},{case_4=},{case_5=},{case_6t=},({'_'.join(case_6t_hint_list)}),{case_6f=},({'_'.join(case_6f_hint_list)}),{case_7t=},{case_7f=},{case_8=}")

        # 今回の手を付け加える。
        best_plot_model_in_children.append_move(
                is_absolute_opponent    = is_absolute_opponent,
                move                    = best_move,
                capture_piece_type      = best_move_cap_pt,
                hint                    = f"{self._max_depth - depth + 1}階の手記憶_{is_absolute_opponent=}")

        return best_plot_model_in_children
