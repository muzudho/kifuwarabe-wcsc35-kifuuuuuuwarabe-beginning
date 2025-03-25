import cshogi

from ..logics_o1x import Helper
from ..models_o1x import constants, MoveOnScrambleModel, PieceValuesModel, PieceTypeModel, SearchResultStateModel, SquareModel, TurnModel
from ..models_o2x import PlotModel


class QuiescenceSearchForScramble():
    """駒の取り合いのための静止探索。
    駒の取り合いが終わるまで、駒の取り合いを探索します。
    TODO Model
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
        self._all_plots_at_first = []


    @property
    def all_plots_at_first(self):
        return self._all_plots_at_first


    def search_alice(self, depth, alice_s_remaining_moves):
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

        Parameters
        ----------
        depth : int
            残りの探索深さ。
        alice_s_remaining_moves : list<int>
            アリスの指し手のリスト。

        Returns
        -------
        best_prot_model : PlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        if depth < 1:
            raise ValueError(f'depth が 1 未満のときにこのメソッドを呼び出してはいけません。 {depth=}')

        ########################
        # MARK: 指す前にやること
        ########################

        if self._gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = PlotModel()
            best_plot_model.append_capture(
                    search_result_state_model   = SearchResultStateModel.RESIGN,
                    move        = None,
                    piece_type  = None)
            
            if depth == self._max_depth:
                self._all_plots_at_first.append(best_plot_model)

            return best_plot_model

        if self._gymnasium.table.is_nyugyoku():
            """手番の入玉宣言局面時。
            """
            best_plot_model = PlotModel()
            best_plot_model.append_capture(
                    search_result_state_model   = SearchResultStateModel.NYUGYOKU_WIN,
                    move        = None,
                    piece_type  = None)
            
            if depth == self._max_depth:
                self._all_plots_at_first.append(best_plot_model)

            return best_plot_model

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj = SquareModel(cshogi.move_to(matemove))           # ［移動先マス］
                cap_pt = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

                best_plot_model = PlotModel()
                best_plot_model.append_capture(
                        search_result_state_model   = SearchResultStateModel.MATE_IN_1_MOVE,
                        move        = matemove,
                        piece_type  = cap_pt)
            
                if depth == self._max_depth:
                    self._all_plots_at_first.append(best_plot_model)

                return best_plot_model

        best_value = constants.value.NOTHING_CAPTURE_MOVE  # （指し手のリストが空でなければ）どんな手でも更新される。
        best_plot_model = None

        ##############################
        # MARK: アリスの合法手スキャン
        ##############################

        # 手番（アリス）が［駒を取る手］を全部調べる。
        for index, alice_s_move in enumerate(alice_s_remaining_moves):

            ##########################
            # MARK: アリスが一手指す前
            ##########################

            dst_sq_obj = SquareModel(cshogi.move_to(alice_s_move))           # ［移動先マス］
            cap_pt = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            is_capture = (cap_pt != cshogi.NONE)

            # １回呼出時。
            if self._max_depth == depth:
                pass    # 何も無視しない。
            else:
                # 駒を取る手でなければ無視。
                if not is_capture:
                    continue

            ########################
            # MARK: アリスが一手指す
            ########################

            self._gymnasium.do_move_o1x(move = alice_s_move)
            depth -= 1

            ############################
            # MARK: アリスが一手指した後
            ############################

            #print(f"(next {self._gymnasium.table.move_number} teme) ({index}) alice's move={cshogi.move_to_usi(alice_s_move)}({Helper.sq_to_masu(dst_sq_obj.sq)}) pt({PieceTypeModel.alphabet(piece_type=cap_pt)}) {alice_s_best_piece_value=} {piece_exchange_value=}")

            # これ以上深く読まない場合。
            if depth - 1 < 1:
                cur_plot_model = PlotModel()

            # まだ深く読む場合。
            else:
                cur_plot_model = self.search_alice(      # 再帰呼出
                        depth                           = depth,
                        alice_s_remaining_moves         = list(self._gymnasium.table.legal_moves))

            cur_plot_model.append_capture(
                    search_result_state_model   = SearchResultStateModel.NONE,  # ふつうの手
                    move        = alice_s_move,
                    piece_type  = cap_pt)
            
            if depth == self._max_depth:
                self._all_plots_at_first.append(cur_plot_model)

            # TODO アリスとしては、損が一番小さな分岐へ進みたい。
            # 手番は、一番得する手を指したい。
            if best_plot_model is None:
                best_plot_model = cur_plot_model
            if best_plot_model.last_piece_exchange_value < cur_plot_model.last_piece_exchange_value:
                best_plot_model = cur_plot_model

            ########################
            # MARK: アリスが一手戻す
            ########################

            self._gymnasium.undo_move_o1x()

            ############################
            # MARK: アリスが一手戻した後
            ############################

            depth += 1

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指せる手がなかったなら、静止探索の終了後だ。
        if best_value == constants.value.NOTHING_CAPTURE_MOVE:
            return PlotModel()

        return best_plot_model
