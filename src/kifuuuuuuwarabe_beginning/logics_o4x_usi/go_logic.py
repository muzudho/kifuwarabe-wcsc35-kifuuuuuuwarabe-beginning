import random

from ..logics_o1x import MovesReductionFilterLogics
from ..models_o1x import SearchResultStateModel
from .quiescence_search_for_scramble import QuiescenceSearchForScramble


class GoLogic():


    @staticmethod
    def Go(gymnasium):
        """盤面が与えられるので、次の１手を返します。

        Returns
        -------
        best_move : int
            ［指す手］
        """
        search = _Search(gymnasium)
        (
            result_state,
            friend_value,
            best_move
        ) = search.search()
        return (result_state, best_move)


class _Search():


    def __init__(self, gymnasium):
        self._gymnasium = gymnasium


    def search(self):
        """盤面が与えられるので、次の１手を返します。

        TODO 再帰的に呼び出されます。

        Returns
        -------
        result_state : int
            結果の種類。
        friend_value : int
            手番から見た駒得評価値。
        best_move : int
            ［指す手］
            該当が無ければナン。
        """

        if self._gymnasium.table.is_game_over():
            """投了局面時。
            """
            return SearchResultStateModel.RESIGN, 0, None

        if self._gymnasium.table.is_nyugyoku():
            """入玉宣言局面時。
            """
            return SearchResultStateModel.NYUGYOKU_WIN, 0, None

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return SearchResultStateModel.MATE_IN_1_MOVE, 0, matemove

        remaining_moves = list(self._gymnasium.table.legal_moves)
        #print(f"A: {len(remaining_moves)=}")

        ################
        # MARK: 静止探索
        ################

        def _quiescence_search_for_scramble_on_board(depth, remaining_moves, gymnasium):
            # 駒の取り合いのための静止探索
            scramble_search = QuiescenceSearchForScramble(
                    gymnasium = gymnasium)

            old_remaining_moves = remaining_moves.copy()

            depth                       = 2
            alice_s_profit_before_move  = 0
            alice_s_remaining_moves_before_move = []

            if 0 < depth:
                (
                    alice_s_profit_after_move,
                    alice_s_remaining_moves_before_move     # NOTE 入玉宣言勝ちは空リストが返ってくるが、事前に省いているからＯｋ。
                ) = scramble_search.search_alice(
                        depth                       = depth,
                        alice_s_profit_before_move  = alice_s_profit_before_move,   # アリスの得。
                        alice_s_remaining_moves     = remaining_moves)

            #print(f"{alice_s_profit_after_move=} {len(alice_s_remaining_moves_before_move)=}")

            # 駒を取る手があり、かつ、アリスに得があればその手に制限します。
            if 0 < len(alice_s_remaining_moves_before_move) and 0 < alice_s_profit_after_move:
                return alice_s_remaining_moves_before_move
            
            # それ以外なら元に戻します。
            return old_remaining_moves

        remaining_moves = _quiescence_search_for_scramble_on_board(
                depth           = 2,                # 何手読みか。
                remaining_moves = remaining_moves,
                gymnasium       = self._gymnasium)





        # 合法手から、１手を選び出します。
        # （必ず、投了ではない手が存在します）
        #
        # ［指前］
        #       制約：
        #           指し手は必ず１つ以上残っています。
        remaining_moves = MovesReductionFilterLogics.before_move_o1x(
                remaining_moves = remaining_moves,
                gymnasium       = self._gymnasium)
        print(f"C: {len(remaining_moves)=}")

        # １手に絞り込む
        best_move = random.choice(remaining_moves)

        # ［指後］
        MovesReductionFilterLogics.after_best_moving(
                move        = best_move,
                gymnasium   = self._gymnasium)

        return SearchResultStateModel.BEST_MOVE, 0, best_move
