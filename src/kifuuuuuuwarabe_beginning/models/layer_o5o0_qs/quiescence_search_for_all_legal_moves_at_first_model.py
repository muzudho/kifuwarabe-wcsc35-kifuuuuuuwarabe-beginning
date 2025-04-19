import cshogi
import time

from ...logics.layer_o1o0 import MoveListLogics
from ..layer_o1o0 import constants, Mars, SquareModel
from ..layer_o2o0 import BackwardsPlotModel, cutoff_reason
from ..layer_o4o0_rules.negative import DoNotDepromotionModel
from .quiescence_search_for_scramble_model import QuiescenceSearchForScrambleModel
from .search_model import SearchModel


class QuiescenceSearchForAllLegalMovesAtFirstModel():
    """１階の全てのリーガル・ムーブについて静止探索。
    """


    def __init__(self, max_depth, gymnasium):
        """
        Parameters
        ----------
        gymnasium : GymnasiumModel
            体育館。        
        """
        self._search_model = SearchModel(
                max_depth   = max_depth,
                gymnasium   = gymnasium)
    

    @property
    def search_model(self):
        return self._search_model


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
            is_mars,
            remaining_moves):
        """
        Parameters
        ----------
        # best_plot_model_in_older_sibling : BackwardsPlotModel
        #     兄たちの中で最善の読み筋、またはナン。ベータカットに使う。
        depth : int
            あと何手深く読むか。
        is_mars : bool
            対戦相手か？
        remaining_moves : list<int>
            指し手のリスト。

        Returns
        -------
        all_backwards_plot_models_at_first : list<BackwardsPlotModel>
            全ての１階の合法手の読み筋。
        """

        self._search_model.start_time = time.time()          # 探索開始時間
        self._search_model.restart_time = self._search_model.start_time   # 前回の計測開始時間
        all_backwards_plot_models_at_first = []

        ########################
        # MARK: 指す前にやること
        ########################

        # 指さなくても分かること（ライブラリー使用）

        # NOTE このあたりは［０階］。max_depth - depth。
        if self._search_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = BackwardsPlotModel(
                    is_mars_at_declaration  = is_mars,
                    declaration             = constants.declaration.RESIGN,
                    cutoff_reason           = cutoff_reason.GAME_OVER,
                    hint                    = '手番の投了局面時１')
            all_backwards_plot_models_at_first.append(best_plot_model)
            return all_backwards_plot_models_at_first

        # 一手詰めを詰める
        if not self._search_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._search_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
                cap_pt = self._search_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

                best_plot_model = BackwardsPlotModel(
                        is_mars_at_declaration  = not is_mars,  # ［詰む］のは、もう１手先だから。
                        declaration             = constants.declaration.RESIGN,
                        cutoff_reason           = cutoff_reason.MATE_MOVE_IN_1_PLY,
                        hint                    = '一手詰めA')
            
                # 今回の手を付け加える。
                best_plot_model.append_move(
                        move                = mate_move,
                        capture_piece_type  = cap_pt,
                        hint                = f"一手詰め１_{Mars.japanese(is_mars)}")

                all_backwards_plot_models_at_first.append(best_plot_model)
                return all_backwards_plot_models_at_first

        if self._search_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言局面時。
            """
            best_plot_model = BackwardsPlotModel(
                    is_mars_at_declaration  = is_mars,
                    declaration             = constants.declaration.NYUGYOKU_WIN,
                    cutoff_reason           = cutoff_reason.NYUGYOKU_WIN,
                    hint                    = '手番の入玉宣言局面時１')
            all_backwards_plot_models_at_first.append(best_plot_model)
            return all_backwards_plot_models_at_first

        # これ以上深く読まない場合。
        if depth < 1:
            best_plot_model = BackwardsPlotModel(
                    is_mars_at_declaration  = is_mars,
                    declaration             = constants.declaration.MAX_DEPTH_BY_THINK, # 読みの最大深さ。
                    cutoff_reason           = cutoff_reason.MAX_DEPTH,
                    hint                    = 'これ以上深く読まない場合１')
            all_backwards_plot_models_at_first.append(best_plot_model)
            return all_backwards_plot_models_at_first

        # まだ深く読む場合。

        ######################
        # MARK: 合法手スキャン
        ######################

        # 最善手は探さなくていい。全部返すから。

        # # TODO 安い駒から交換する
        # remaining_moves = MoveListLogics.when_replacing_pieces_start_with_the_cheaper_ones(
        #         move_list   = remaining_moves,
        #         gymnasium   = self._search_model.gymnasium)

        # 指し手を全部調べる。
        do_not_depromotion_model = DoNotDepromotionModel(
                basketball_court_model=self._search_model.gymnasium.basketball_court_model)    # TODO 号令［成らないということをするな］

        do_not_depromotion_model._before_branches_nrm(
                table=self._search_model.gymnasium.table)
        
        for my_move in remaining_moves:

            ##################
            # MARK: 一手指す前
            ##################

            # ［成れるのに成らない手］は除外
            mind = do_not_depromotion_model._before_move_nrm(
                    move    = my_move,
                    table   = self._search_model.gymnasium.table)
            if mind == constants.mind.WILL_NOT:
                continue

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            # 打の場合、取った駒無し。空マス。
            cap_pt      = self._search_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

            # １階呼出時は、どの手も無視しません。

            # ＜📚原則１＞により、駒を取らない手は、探索を１手延長します。
            is_capture  = (cap_pt != cshogi.NONE)

            # ２階以降の呼出時は、駒を取る手でなければ無視。 FIXME 王手が絡んでいるとき、取れないこともあるから、王手が絡むときは場合分けしたい。
            if not is_capture:
                depth_extend = 1
            else:
                depth_extend = 0

            ################
            # MARK: 一手指す
            ################

            self._search_model.gymnasium.do_move_o1x(move = my_move)

            ####################
            # MARK: 一手指した後
            ####################

            self._search_model.move_list_for_debug.append_move(my_move)      # デバッグ用に手を記憶
            self._search_model.number_of_visited_nodes  += 1
            depth                                       -= 1                            # 深さを１下げる。
            is_mars                                     = not is_mars      # 手番が逆になる。

            ####################
            # MARK: 相手番の処理
            ####################

            # NOTE この辺りは［１階］。max_depth - depth。
            quiescenec_search_for_scramble_model = QuiescenceSearchForScrambleModel(
                    search_model    = self._search_model)
            future_plot_model = quiescenec_search_for_scramble_model.search_alice(      # 再帰呼出
                    depth       = depth + depth_extend,
                    is_mars     = is_mars)

            ################
            # MARK: 一手戻す
            ################

            self._search_model.gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            self._search_model.move_list_for_debug.pop_move()                         # デバッグ用に手を記憶
            depth       += 1                # 深さを１上げる。
            is_mars     = not is_mars       # 手番が逆になる。

            ##################
            # MARK: 手番の処理
            ##################

            # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
            future_plot_model.append_move(
                    move                = my_move,
                    capture_piece_type  = cap_pt,
                    hint                = f"１階の{Mars.japanese(is_mars)}の手はなんでも記憶")
            all_backwards_plot_models_at_first.append(future_plot_model)

            # NOTE この辺りは［０階］。

            # ベータカットもしません。全部返すから。

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if len(all_backwards_plot_models_at_first) < 1:
            future_plot_model = BackwardsPlotModel(
                    is_mars_at_declaration  = is_mars,
                    declaration             = constants.declaration.NO_CANDIDATES, # 有力な候補手無し。
                    cutoff_reason           = cutoff_reason.NO_MOVES,
                    hint                    = f"１階の{Mars.japanese(is_mars)}は指したい手無し_{depth=}/{self._search_model.max_depth=}_{len(all_backwards_plot_models_at_first)=}/{len(remaining_moves)=}")
            all_backwards_plot_models_at_first.append(future_plot_model)

        self._search_model.end_time = time.time()    # 計測終了時間

        return all_backwards_plot_models_at_first
