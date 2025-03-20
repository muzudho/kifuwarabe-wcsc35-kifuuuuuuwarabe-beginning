import cshogi
import random

from ..logics_o1x import KomadokuFilterLogics, MovesReductionFilterLogics


class GoLogicResultState():


    @staticmethod
    def RESIGN():
        """投了。
        """
        return 1


    @staticmethod
    def NYUGYOKU_WIN():
        """入玉宣言局面時。
        """
        return 2


    def MATE_IN_1_MOVE():
        """１手詰め時。
        """
        return 3


    def BEST_MOVE():
        """通常時の次の１手。
        """
        return 4


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
            return GoLogicResultState.RESIGN, 0, None

        if self._gymnasium.table.is_nyugyoku():
            """入玉宣言局面時。
            """
            return GoLogicResultState.NYUGYOKU_WIN, 0, None

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return GoLogicResultState.MATE_IN_1_MOVE, 0, matemove

        remaining_moves = list(self._gymnasium.table.legal_moves)
        #print(f"A: {len(remaining_moves)=}")

        # 駒得評価値でフィルタリング
        #       制約：
        #           指し手は必ず１つ以上残っています。
        remaining_moves = KomadokuFilterLogics.filtering(
                remaining_moves = remaining_moves,
                gymnasium       = self._gymnasium)
        #print(f"B: {len(remaining_moves)=}")

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

        return GoLogicResultState.BEST_MOVE, 0, best_move
