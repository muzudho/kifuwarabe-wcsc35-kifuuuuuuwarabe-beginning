import cshogi
import time

from ...logics.layer_o1o0 import MoveListLogics
from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import AbsoluteOpponent, constants, PtolemaicTheoryModel, SquareModel
from ..layer_o2o0 import BackwardsPlotModel, cutoff_reason


class QuiescenceSearchForScrambleModel():
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
        erapsed_seconds = cur_time - self._search_model.restart_time     # 経過秒
        if 4 <= erapsed_seconds:                            # 4秒以上経過してたら、情報出力
            print(f"info depth {self._search_model.max_depth - depth} seldepth 0 time 1 nodes {self.search_model.number_of_visited_nodes} score cp 0 string thinking")
            self.search_model.restart_time = cur_time                   # 前回の計測時間を更新

        # 指さなくても分かること（ライブラリー使用）

        if self.search_model.gymnasium.table.is_game_over():
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
        if not self.search_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self.search_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
                cap_pt = self.search_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

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

        if self.search_model.gymnasium.table.is_nyugyoku():
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
                    declaration                             = constants.declaration.MAX_DEPTH_BY_THINK, # 読みの最大深さ。
                    is_mate_in_1_move                       = False,                        # ［一手詰め］ではない。
                    cutoff_reason                           = cutoff_reason.MAX_DEPTH,      # ［最大探索深さ］が打切り理由。
                    hint                                    = f"{self._search_model.max_depth - depth}階でこれ以上深く読まない場合_{depth=}/{self._search_model.max_depth=}_{is_absolute_opponent=}")

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
        case_4 = 0
        case_5 = 0
        case_6t = 0
        case_6t_hint_list = []
        case_6f = 0
        case_6f_hint_list = []
        case_8at = 0
        case_8af = 0
        case_8b = 0
        case_8c = 0
        case_8d = 0
        case_8e = 0

        # 合法手を全部調べる。
        legal_move_list = list(self.search_model.gymnasium.table.legal_moves)

        remaining_moves = legal_move_list
        # TODO 安い駒から交換したい。
        # remaining_moves = MoveListLogics.when_replacing_pieces_start_with_the_cheaper_ones(
        #         move_list   = legal_move_list,
        #         gymnasium   = self._search_model.gymnasium)

        for my_move in remaining_moves:

            ##################
            # MARK: 一手指す前
            ##################

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self.search_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            is_capture  = (cap_pt != cshogi.NONE)

            # ２階以降の呼出時は、駒を取る手でなければ無視。 FIXME 王手が絡んでいるとき、取れないこともあるから、王手が絡むときは場合分けしたい。
            if not is_capture:
                case_1 += 1
                continue

            ################
            # MARK: 一手指す
            ################

            self.search_model.gymnasium.do_move_o1x(move = my_move)
            self._search_model.number_of_visited_nodes += 1

            ####################
            # MARK: 一手指した後
            ####################

            self._search_model.move_list_for_debug.append_move(my_move)           # デバッグ用に手を記憶
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

            self.search_model.gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            self._search_model.move_list_for_debug.pop_move()                     # デバッグ用に手を記憶
            depth                   = depth + 1                 # 深さを１上げる。
            is_absolute_opponent    = not is_absolute_opponent  # 手番が逆になる。
            ptolemaic_theory_model  = PtolemaicTheoryModel(
                    is_absolute_opponent=is_absolute_opponent)

            ##################
            # MARK: 手番の処理
            ##################

            its_update_best = False

            # NOTE `earth` - 自分。 `mars` - 対戦相手。
            piece_exchange_value_on_earth = PieceValuesModel.get_piece_exchange_value_on_earth(      # 交換値に変換。正の数とする。
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

                    e1 = ptolemaic_theory_model.swap(old_sibling_value, this_branch_value)

                    # # TODO ただし、既存の最善手より良い手を見つけてしまったら、ベータカットします。
                    # if beta_cutoff_value < this_branch_value:
                    #     #will_beta_cutoff = True   # TODO ベータカット
                    #     pass

                    # （初期値の０または）最善より良い手なら、これを選びます。
                    its_update_best = (e1[0] < e1[1])
                    case_2 += 1

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
                    # ValueError: 想定外の読み筋 self._is_absolute_opponent_at_end_position=False self._declaration=0 self._is_mate_in_1_move=False self._move_list=[] self._cap_list=[] self._piece_exchange_value_list_on_earth=[] self._cutoff_reason=4
                    raise ValueError(f"想定外の読み筋A {future_plot_model.stringify_dump()}")
            
            # 指し手がある。
            else:
                this_branch_value = future_plot_model.last_piece_exchange_value_on_earth + piece_exchange_value_on_earth

                # 兄手がまだ無いなら。
                if best_plot_model_in_children is None:

                    e1 = ptolemaic_theory_model.swap(0, this_branch_value)
                    # この枝が０点以上なら最善手（［Not Bad］）として回答。この最善手が最終的に即採用されるというわけではない。
                    its_update_best = (e1[0] <= e1[1])

                    if its_update_best:
                        case_8at += 1
                    else:
                        case_8af += 1
                    #case_8_hint_list.append(f"{old_sibling_value=} < {this_branch_value=}")
                
                # 兄枝は有るが、［手］が無い場合。（［宣言］の直前とか、最大深さとか）
                elif best_plot_model_in_children.is_empty_moves():
                    if best_plot_model_in_children.declaration == constants.declaration.RESIGN: # 相手が投了なら、最善手だ。
                        case_8b += 1
                        its_update_best = True

                    elif best_plot_model_in_children.declaration == constants.declaration.NYUGYOKU_WIN: # 相手が入玉宣言勝ちなら、最悪手だ。
                        case_8c += 1

                    elif best_plot_model_in_children.declaration == constants.declaration.MAX_DEPTH_BY_THINK: # 読みの最大深さ。
                        case_8d += 1

                    elif best_plot_model_in_children.declaration == constants.declaration.NO_CANDIDATES: # 有力な候補手無し。
                        case_8e += 1

                    elif best_plot_model_in_children.declaration == constants.declaration.NONE:  # ［宣言］ではない。
                        raise ValueError(f"宣言ではなかったB。 best={best_plot_model_in_children.stringify_dump()} future={future_plot_model.stringify_dump()}")

                    else:
                        raise ValueError(f"想定外の読み筋B best={best_plot_model_in_children.stringify_dump()} future={future_plot_model.stringify_dump()}")

                # 兄枝が有り、［手］も有るなら比較対象。
                else:
                    # 兄枝のベスト評価値
                    old_sibling_value = best_plot_model_in_children.last_piece_exchange_value_on_earth     # とりあえず最善の読み筋の点数。


                    def _log_1(case_1):
                        return f"[search] {case_1} {depth=}/{self._search_model.max_depth=} {AbsoluteOpponent.japanese(is_absolute_opponent)} {self.stringify()},{cshogi.move_to_usi(my_move)}(私{this_branch_value}) {old_sibling_value=} < {future_plot_model.stringify()=}"


                    # この枝の点（将来の点＋取った駒の点）
                    this_branch_value = future_plot_model.last_piece_exchange_value_on_earth + piece_exchange_value_on_earth

                    # # TODO 既存の最善手より良い手を見つけてしまったら、ベータカットします。
                    # if beta_cutoff_value < this_branch_value:
                    #     #will_beta_cutoff = True   # TODO ベータカット
                    #     pass

                    # 最善より良い手があれば、そっちを選びます。
                        #       NOTE １件に絞り込んでいいのか？ 後ろ向き探索なら１件に絞り込んでいいのか？
                    e2 = ptolemaic_theory_model.swap(old_sibling_value, this_branch_value)
                    its_update_best = (e2[0] < e2[1])


                    if its_update_best:
                        case_6t += 1
                        case_6t_hint_list.append(f"{old_sibling_value=} < {this_branch_value=}")

                        #self.search_model.gymnasium.thinking_logger_module.append(f"[search] 6t {self._search_model.move_list_for_debug=}")
                        # if self._search_model.move_list_for_debug.equals_move_usi_list(['3a4b']):   # FIXME デバッグ絞込み
                        #     self.search_model.gymnasium.thinking_logger_module.append(_log_1('6t'))

                    else:
                        case_6f += 1
                        case_6f_hint_list.append(f"{old_sibling_value=} < {this_branch_value=}")

                        #self.search_model.gymnasium.thinking_logger_module.append(f"[search] 6f {self._search_model.move_list_for_debug=}")
                        # if self._search_model.move_list_for_debug.equals_move_usi_list(['3a4b']):   # FIXME デバッグ絞込み
                        #     self.search_model.gymnasium.thinking_logger_module.append(_log_1('6f'))
                        
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
                    declaration                             = constants.declaration.NO_CANDIDATES,  # 有力な候補手無し。
                    is_mate_in_1_move                       = False,
                    cutoff_reason                           = cutoff_reason.NO_MOVES,
                    hint                                    = f"指したい{self._search_model.max_depth - depth + 1}階の手無し,敵={is_absolute_opponent},move数={len(legal_move_list)},{case_1=},{case_2=},{case_4=},{case_5=},{case_6t=},({'_'.join(case_6t_hint_list)}),{case_6f=},({'_'.join(case_6f_hint_list)}),{case_8at=},{case_8af=},{case_8b=},{case_8c=},{case_8d=},{case_8e=}")

        # 今回の手を付け加える。
        best_plot_model_in_children.append_move(
                is_absolute_opponent    = is_absolute_opponent,
                move                    = best_move,
                capture_piece_type      = best_move_cap_pt,
                hint                    = f"{self._search_model.max_depth - depth + 1}階の手記憶_{is_absolute_opponent=}")

        return best_plot_model_in_children
