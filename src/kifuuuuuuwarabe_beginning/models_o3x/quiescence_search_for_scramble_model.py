import cshogi

from ..models_o1x import constants, SquareModel
from ..models_o2x import PlotModel


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
        self._all_plots_at_first = []


    @property
    def all_plots_at_first(self):
        return self._all_plots_at_first


    def search_alice(
            self,
            depth,
            is_opponent,
            beta_cutoff_value,
            alice_s_remaining_moves):
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
        is_opponent : bool

        beta_cutoff_value : int

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
            best_plot_model = PlotModel(
                    declaration         = constants.declaration.RESIGN,
                    is_mate_in_1_move   = False)
            best_plot_model.append_move(
                    is_opponent         = is_opponent,
                    move                = None,
                    capture_piece_type  = cshogi.NONE)
            
            if depth == self._max_depth:
                self._all_plots_at_first.append(best_plot_model)

            return best_plot_model

        if self._gymnasium.table.is_nyugyoku():
            """手番の入玉宣言局面時。
            """
            best_plot_model = PlotModel(
                    declaration         = constants.declaration.NYUGYOKU_WIN,
                    is_mate_in_1_move   = False)
            best_plot_model.append_move(
                    is_opponent         = is_opponent,
                    move                = None,
                    capture_piece_type  = cshogi.NONE)
            
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

                best_plot_model = PlotModel(
                        declaration         = constants.declaration.NONE,
                        is_mate_in_1_move   = True)
                best_plot_model.append_move(
                        is_opponent         = is_opponent,
                        move                = matemove,
                        capture_piece_type  = cap_pt)
            
                if depth == self._max_depth:
                    self._all_plots_at_first.append(best_plot_model)

                return best_plot_model

        best_plot_model = None

        # TODO 指し手の分析。駒を取る手と、そうでない手を分ける。
        # TODO 駒を取る手も、価値の高い駒から取る手を考える。（相手が手抜く勝手読みをすると、大きな駒を取れてしまうことがあるから）。

        ##############################
        # MARK: アリスの合法手スキャン
        ##############################

        is_beta_cutoff = False  # この関数の緊急脱出フラグ。

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

            ############################
            # MARK: アリスが一手指した後
            ############################

            (
                best_plot_model,
                is_beta_cutoff
            ) = self.search_bob(
                    best_plot_model     = best_plot_model,
                    is_beta_cutoff      = is_beta_cutoff,
                    depth               = depth - 1,                # 深さを１下げる
                    is_opponent         = not is_opponent,          # 手番が逆になる
                    alice_s_move        = alice_s_move,
                    cap_pt              = cap_pt,
                    beta_cutoff_value   = beta_cutoff_value)

            ########################
            # MARK: アリスが一手戻す
            ########################

            self._gymnasium.undo_move_o1x()

            ############################
            # MARK: アリスが一手戻した後
            ############################

            # 探索の打切り判定
            if is_beta_cutoff:
                break   # （アンドゥや、depth の勘定をきちんとしたあとで）ループから抜ける

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指せる手がなかったなら、静止探索の末端局面の後ろだ。
        if best_plot_model is None:
            return PlotModel(
                    declaration         = constants.declaration.NONE,
                    is_mate_in_1_move   = False)

        return best_plot_model


    def search_bob(
            self,
            best_plot_model,
            is_beta_cutoff,
            depth,
            is_opponent,
            alice_s_move,
            cap_pt,
            beta_cutoff_value):
        #print(f"(next {self._gymnasium.table.move_number} teme) ({index}) alice's move={cshogi.move_to_usi(alice_s_move)}({Helper.sq_to_masu(dst_sq_obj.sq)}) pt({PieceTypeModel.alphabet(piece_type=cap_pt)}) {alice_s_best_piece_value=} {piece_exchange_value=}")

        # これ以上深く読まない場合。
        if depth - 1 < 1:
            cur_plot_model = PlotModel(
                    declaration         = constants.declaration.NONE,
                    is_mate_in_1_move   = False)

        # まだ深く読む場合。
        else:


            def _get_beta_cutoff_value(is_opponent, best_plot_model):
                # 最善手が未定なら、天井（底）を最大にします。
                if best_plot_model is None:
                    if is_opponent:
                        return constants.value.BETA_CUTOFF_VALUE        # 天井
                    return - constants.value.BETA_CUTOFF_VALUE  # 底

                # 最善手が既存なら、その交換値を返すだけ。
                return best_plot_model.last_piece_exchange_value


            cur_plot_model = self.search_alice(      # 再帰呼出
                    depth                   = depth,
                    is_opponent             = is_opponent,
                    beta_cutoff_value       = _get_beta_cutoff_value(is_opponent, best_plot_model),
                    alice_s_remaining_moves = list(self._gymnasium.table.legal_moves))

        if cur_plot_model is None:  # 枝は無かったことにされた。（ベータカット）
            pass

        else:
            cur_plot_model.append_move(
                    is_opponent         = not is_opponent,
                    move                = alice_s_move,
                    capture_piece_type  = cap_pt)
            
            if depth + 1 == self._max_depth:
                self._all_plots_at_first.append(cur_plot_model)

            # FIXME 将来的に相手の駒をポロリと取れるなら、手前の手は全部緩手になることがある。どう解消するか？

            # NOTE （スクランブル・サーチでは）ベストがナンということもある。つまり、指さない方がマシな局面がある。
            threshold_value = 0     # 閾値
            if best_plot_model is not None:
                threshold_value = best_plot_model.last_piece_exchange_value     # とりあえず最善の点数。

            # 相手は、点数が小さくなる手を選ぶ
            if not is_opponent:
                if cur_plot_model.last_piece_exchange_value < threshold_value:
                    # 最善より悪い手があれば、そっちを選びます。
                    best_plot_model = cur_plot_model
                    
                    # TODO 既存の最悪手より悪い手を見つけてしまったら、ベータカットします。
                    if cur_plot_model.last_piece_exchange_value < beta_cutoff_value:
                        is_beta_cutoff = True   # beta_cutoff

            # 自分は、点数が大きくなる手を選ぶ
            else:
                if threshold_value < cur_plot_model.last_piece_exchange_value:
                    # 最善より良い手があれば、そっちを選びます。
                    best_plot_model = cur_plot_model

                    # TODO 既存の最善手より良い手を見つけてしまったら、ベータカットします。
                    if beta_cutoff_value < cur_plot_model.last_piece_exchange_value:
                        is_beta_cutoff = True   # beta_cutoff

        return best_plot_model, is_beta_cutoff
