import cshogi
import random

from ..logics_o1x import MovesReductionFilterLogics
from ..models_o1x import ResultOfGo, SearchResultStateModel
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

        return search.start_alice()


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

        remaining_moves         = list(self._gymnasium.table.legal_moves)
        length_by_cshogi        = len(remaining_moves)  # cshogi が示した合法手の数
        length_of_quiescence_search_by_kifuwarabe   = length_by_cshogi  # きふわらべ が静止探索で絞り込んだ指し手の数
        length_by_kifuwarabe    = length_by_cshogi      # きふわらべ が最終的に絞り込んだ指し手の数
        #print(f"D-74: {len(remaining_moves)=}")

        if self._gymnasium.table.is_game_over():
            """投了局面時。
            """
            return ResultOfGo(
                    search_result_state_model   = SearchResultStateModel.RESIGN,
                    alice_s_profit              = 0,
                    best_move                   = None,
                    length_by_cshogi            = length_by_cshogi,
                    length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                    length_by_kifuwarabe        = length_by_kifuwarabe)

        if self._gymnasium.table.is_nyugyoku():
            """入玉宣言局面時。
            """
            return ResultOfGo(
                    search_result_state_model   = SearchResultStateModel.NYUGYOKU_WIN,
                    alice_s_profit              = 0,
                    best_move                   = None,
                    length_by_cshogi            = length_by_cshogi,
                    length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                    length_by_kifuwarabe        = length_by_kifuwarabe)

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return ResultOfGo(
                        search_result_state_model   = SearchResultStateModel.MATE_IN_1_MOVE,
                        alice_s_profit              = 0,
                        best_move                   = matemove,
                        length_by_cshogi            = length_by_cshogi,
                        length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                        length_by_kifuwarabe        = length_by_kifuwarabe)

        ################
        # MARK: 静止探索
        ################

        remaining_moves = _quiescence_search(
                depth           = 2,                # 何手読みか。
                remaining_moves = remaining_moves,
                gymnasium       = self._gymnasium)

        length_of_quiescence_search_by_kifuwarabe   = len(remaining_moves)



        # 合法手から、１手を選び出します。
        # （必ず、投了ではない手が存在します）
        #
        # ［指前］
        #       制約：
        #           指し手は必ず１つ以上残っています。
        remaining_moves = MovesReductionFilterLogics.before_move_o1x(
                remaining_moves = remaining_moves,
                gymnasium       = self._gymnasium)
        #print(f"D-98: {len(remaining_moves)=}")

        length_by_kifuwarabe = len(remaining_moves)

        # １手に絞り込む
        best_move = random.choice(remaining_moves)
        #print(f"D-102: {best_move=}")
        #print(f"D-103: {cshogi.move_to_usi(best_move)=}")

        # ［指後］
        MovesReductionFilterLogics.after_best_moving(
                move        = best_move,
                gymnasium   = self._gymnasium)

        return ResultOfGo(
                search_result_state_model   = SearchResultStateModel.BEST_MOVE,
                alice_s_profit              = 0,
                best_move                   = best_move,
                length_by_cshogi            = length_by_cshogi,
                length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                length_by_kifuwarabe        = length_by_kifuwarabe)


def _quiescence_search(depth, remaining_moves, gymnasium):
    """静止探索。
    
    Returns
    -------
    remaining_moves : list
        指し手のリスト。
    """
    max_depth                   = gymnasium.config_doc['search']['capture_depth']   # 2
    alice_s_remaining_moves_before_move = []

    # 駒の取り合いのための静止探索
    scramble_search = QuiescenceSearchForScramble(
            max_depth   = max_depth,
            gymnasium   = gymnasium)

    old_remaining_moves = remaining_moves.copy()

    if max_depth < 1:
        #print(f"D-132: _quiescence_search {max_depth=}")
        return remaining_moves

    (
        alice_s_best_piece_value,
        alice_s_remaining_moves_before_move,    # NOTE 入玉宣言勝ちは空リストが返ってくるが、事前に省いているからＯｋ。
        alice_s_move_ex_list
    ) = scramble_search.search_alice(
            depth                           = max_depth,
            alice_s_remaining_moves         = remaining_moves)

    #print(f"{alice_s_best_piece_value=} {len(alice_s_remaining_moves_before_move)=}")


    def _eliminate_not_capture_not_positive(alice_s_move_ex_list):
        """駒を取らない手で非正の手は邪魔だ。除去する。
        """
        alice_s_move_ex_list_2 = []
        for alice_s_move_ex in alice_s_move_ex_list:

            if alice_s_move_ex.is_capture or 0 < alice_s_move_ex.piece_value:
                print(f"D-153: _quiescence_search select    {alice_s_move_ex.stringify()}")
                alice_s_move_ex_list_2.append(alice_s_move_ex)
            else:
                print(f"D-156: _quiescence_search eliminate {alice_s_move_ex.stringify()}")
            
        print(f"D-158: _quiescence_search list length {len(alice_s_move_ex_list_2)}")
        return alice_s_move_ex_list_2

    #print(f"D-155: _quiescence_search before _eliminate_not_capture_not_positive {len(alice_s_move_ex_list)=}")

    alice_s_move_ex_list = _eliminate_not_capture_not_positive(
            alice_s_move_ex_list = alice_s_move_ex_list)


    # # DEBUG
    # for alice_s_move_ex in alice_s_move_ex_list:
    #     #print(f"D-149: _quiescence_search {alice_s_best_piece_value=} {alice_s_move_ex.stringify()=}")

    # 最善手があるなら、最善手を返します。
    if 0 < len(alice_s_remaining_moves_before_move):
        #print(f"D-153: _quiescence_search {alice_s_best_piece_value=} {len(alice_s_remaining_moves_before_move)=}")
        return alice_s_remaining_moves_before_move

    # 最善手が無ければ（全ての手がフラットなら）、元に戻します。
    #print(f"D-157: _quiescence_search {alice_s_best_piece_value=} {len(alice_s_remaining_moves_before_move)=}")
    return old_remaining_moves

    # if len(alice_s_remaining_moves_before_move) < 1:
    #     print(f"D-113: {len(alice_s_remaining_moves_before_move)=}")
    #     return old_remaining_moves

    # # 最善手がアリスに得のある手であれば、その手に制限します。
    # if 0 < alice_s_best_piece_value:
    #     print(f"D-118: {alice_s_best_piece_value=}")
    #     return alice_s_remaining_moves_before_move
    
    # # アリスに非得の手しかなければ、非損の手に制限します。
    # alice_s_move_list_2 = []
    # for alice_s_move_ex in alice_s_move_ex_list:
    #     print(f"D-187: {alice_s_move_ex.stringify()=}")
    #     if 0 <= alice_s_move_ex.piece_value:
    #         alice_s_move_list_2.append(alice_s_move_ex.move)
    
    # # 非損の手もなければ、元に戻します。
    # if len(alice_s_move_list_2) == 0:
    #     print(f"D-193: {len(alice_s_move_list_2)=}")
    #     return old_remaining_moves

    # # 非損の手のリスト。
    # print(f"D-133: {len(alice_s_move_list_2)=}")
    # return alice_s_move_list_2
