import cshogi
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
        ) = search.start_alice()

        return (result_state, best_move)


class _Search():


    def __init__(self, gymnasium):
        self._gymnasium = gymnasium


    def start_alice(self):
        """盤面が与えられるので、次の１手を返します。

        最初の１手だけの処理です。

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
        #print(f"D74: {len(remaining_moves)=}")

        ################
        # MARK: 静止探索
        ################

        remaining_moves = _quiescence_search(
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
        print(f"D98: {len(remaining_moves)=}")

        # １手に絞り込む
        best_move = random.choice(remaining_moves)
        print(f"D102: {best_move=}")
        print(f"D103: {cshogi.move_to_usi(best_move)=}")

        # ［指後］
        MovesReductionFilterLogics.after_best_moving(
                move        = best_move,
                gymnasium   = self._gymnasium)

        return SearchResultStateModel.BEST_MOVE, 0, best_move


def _quiescence_search(depth, remaining_moves, gymnasium):
    """静止探索。
    
    Returns
    -------
    remaining_moves : list
        指し手のリスト。
    """
    max_depth                   = 2
    alice_s_profit_before_move  = 0
    alice_s_remaining_moves_before_move = []

    # 駒の取り合いのための静止探索
    scramble_search = QuiescenceSearchForScramble(
            max_depth   = max_depth,
            gymnasium   = gymnasium)

    old_remaining_moves = remaining_moves.copy()

    if max_depth < 1:
        print(f"D132: _quiescence_search {max_depth=}")
        return remaining_moves

    (
        alice_s_profit_after_move,
        alice_s_remaining_moves_before_move,    # NOTE 入玉宣言勝ちは空リストが返ってくるが、事前に省いているからＯｋ。
        alice_s_move_wp_list
    ) = scramble_search.search_alice(
            depth                           = max_depth,
            alice_s_profit_before_move      = alice_s_profit_before_move,   # アリスの得。
            alice_s_remaining_moves         = remaining_moves)

    #print(f"{alice_s_profit_after_move=} {len(alice_s_remaining_moves_before_move)=}")

    # DEBUG
    for alice_s_omve_wp in alice_s_move_wp_list:
        print(f"D149: _quiescence_search {alice_s_profit_after_move=} {alice_s_omve_wp.stringify()=}")

    # 最善手があるなら、最善手を返します。
    if 0 < len(alice_s_remaining_moves_before_move):
        print(f"D153: _quiescence_search {alice_s_profit_after_move=} {len(alice_s_remaining_moves_before_move)=}")
        return alice_s_remaining_moves_before_move

    # 最善手が無ければ（全ての手がフラットなら）、元に戻します。
    print(f"D157: _quiescence_search {alice_s_profit_after_move=} {len(alice_s_remaining_moves_before_move)=}")
    return old_remaining_moves

    # if len(alice_s_remaining_moves_before_move) < 1:
    #     print(f"D113: {len(alice_s_remaining_moves_before_move)=}")
    #     return old_remaining_moves

    # # 最善手がアリスに得のある手であれば、その手に制限します。
    # if 0 < alice_s_profit_after_move:
    #     print(f"D118: {alice_s_profit_after_move=}")
    #     return alice_s_remaining_moves_before_move
    
    # # アリスに非得の手しかなければ、非損の手に制限します。
    # alice_s_move_list_2 = []
    # for alice_s_move_wp in alice_s_move_wp_list:
    #     print(f"D: {alice_s_move_wp.stringify()=}")
    #     if 0 <= alice_s_move_wp.profit:
    #         alice_s_move_list_2.append(alice_s_move_wp.move)
    
    # # 非損の手もなければ、元に戻します。
    # if len(alice_s_move_list_2) == 0:
    #     print(f"D129: {len(alice_s_move_list_2)=}")
    #     return old_remaining_moves

    # # 非損の手のリスト。
    # print(f"D133: {len(alice_s_move_list_2)=}")
    # return alice_s_move_list_2
