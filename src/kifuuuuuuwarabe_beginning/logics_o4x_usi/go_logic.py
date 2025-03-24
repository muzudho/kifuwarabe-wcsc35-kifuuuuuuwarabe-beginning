import cshogi
import random
import sys

from ..logics_o1x import MovesReductionFilterLogics
from ..models_o1x import constants, ResultOfGoModel, SearchResultStateModel
from ..views import TableView
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
        gymnasium.health_check.on_go_started()

        search = _Search(gymnasium)

        gymnasium.health_check.on_go_finished()

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

        for move in remaining_moves:
            self._gymnasium.health_check.append(
                    move    = move,
                    name    = 'legal',
                    value   =  True)

        length_by_cshogi        = len(remaining_moves)  # cshogi が示した合法手の数
        length_of_quiescence_search_by_kifuwarabe   = length_by_cshogi  # きふわらべ が静止探索で絞り込んだ指し手の数
        length_by_kifuwarabe    = length_by_cshogi      # きふわらべ が最終的に絞り込んだ指し手の数
        #print(f"D-74: {len(remaining_moves)=}")

        if self._gymnasium.table.is_game_over():
            """投了局面時。
            """
            return ResultOfGoModel(
                    search_result_state_model   = SearchResultStateModel.RESIGN,
                    alice_s_profit              = 0,
                    best_move                   = None,
                    length_by_cshogi            = length_by_cshogi,
                    length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                    length_by_kifuwarabe        = length_by_kifuwarabe)

        if self._gymnasium.table.is_nyugyoku():
            """入玉宣言局面時。
            """
            return ResultOfGoModel(
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
                return ResultOfGoModel(
                        search_result_state_model   = SearchResultStateModel.MATE_IN_1_MOVE,
                        alice_s_profit              = 0,
                        best_move                   = matemove,
                        length_by_cshogi            = length_by_cshogi,
                        length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                        length_by_kifuwarabe        = length_by_kifuwarabe)

        ################
        # MARK: 静止探索
        ################

        old_remaining_moves = remaining_moves.copy()

        remaining_moves = _quiescence_search(
                depth           = 2,                # 何手読みか。
                remaining_moves = remaining_moves,
                gymnasium       = self._gymnasium)
        length_of_quiescence_search_by_kifuwarabe   = len(remaining_moves)
        self._gymnasium.thinking_logger_module.append(f"{length_of_quiescence_search_by_kifuwarabe=}")

        for move in remaining_moves:
            self._gymnasium.health_check.append(
                    move    = move,
                    name    = 'quiescence_search',
                    value   =  True)

        if len(remaining_moves) == 0:
            remaining_moves = old_remaining_moves
            self._gymnasium.thinking_logger_module.append(f"Restore after quiescence_search. len={len(remaining_moves)}.")

        old_remaining_moves = remaining_moves.copy()

        # 合法手から、１手を選び出します。
        # （必ず、投了ではない手が存在します）
        #
        # ［指前］
        #       制約：
        #           指し手は必ず１つ以上残っています。
        remaining_moves = MovesReductionFilterLogics.before_move_o1x(
                remaining_moves = remaining_moves,
                gymnasium       = self._gymnasium)
        length_by_kifuwarabe = len(remaining_moves)
        self._gymnasium.thinking_logger_module.append(f"{length_by_kifuwarabe=}")

        for move in remaining_moves:
            self._gymnasium.health_check.append(
                    move    = move,
                    name    = 'nr_select',
                    value   =  True)

        if len(remaining_moves) == 0:
            remaining_moves = old_remaining_moves
            self._gymnasium.thinking_logger_module.append(f"Restore after MovesReductionFilterLogics. len={len(remaining_moves)}.")

            for move in remaining_moves:
                self._gymnasium.health_check.append(
                        move    = move,
                        name    = 'nr_reselect',
                        value   =  True)

        # ログ
        message = f"""\
{TableView(self._gymnasium.table).stringify()}
HEALTH CHECK
------------
{self._gymnasium.health_check.stringify()}

{self._gymnasium.negative_rule_collection_model.stringify()}
"""
        # TODO ネガティブ・ルールの一覧も表示したい。
        self._gymnasium.thinking_logger_module.append(message)
        # NOTE これを書くと、将棋ホームでフリーズ： print(message, file=sys.stderr)

        # １手に絞り込む
        best_move = random.choice(remaining_moves)
        self._gymnasium.thinking_logger_module.append(f"Best move={cshogi.move_to_usi(best_move)}")

        # ［指後］
        MovesReductionFilterLogics.after_best_moving(
                move        = best_move,
                gymnasium   = self._gymnasium)

        return ResultOfGoModel(
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

    # 駒の取り合いのための静止探索
    scramble_search = QuiescenceSearchForScramble(
            max_depth   = max_depth,
            gymnasium   = gymnasium)

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


    def _eliminate_not_capture_not_positive(alice_s_move_ex_list, gymnasium):
        """次の１つの手は、候補に挙げる必要がないので除去します。
        （１）駒を取らない手で非正の手。
        次の手は、候補に挙げる必要がないので除去します。
        （２）最高点でない手。
        それ以外の手は選択します。

        Returns
        -------
        alice_s_move_list : list(int)
            指し手のリスト。
        """
        alice_s_move_list = []

        # まず、最高点を調べます。
        best_exchange_value = constants.value.NOTHING_CAPTURE_MOVE
        for alice_s_move_ex in alice_s_move_ex_list:
            if best_exchange_value < alice_s_move_ex.piece_exchange_value:
                best_exchange_value = alice_s_move_ex.piece_exchange_value

        for alice_s_move_ex in alice_s_move_ex_list:

            # （１）駒を取らない手で非正の手。
            if not alice_s_move_ex.is_capture and alice_s_move_ex.piece_exchange_value < 1:
                gymnasium.health_check.append(
                        move    = alice_s_move_ex.move,
                        name    = 'eliminate171',
                        value   = f"{alice_s_move_ex.stringify_2():10} not_cap_not_posite")

            # （２）最高点でない手。
            elif alice_s_move_ex.piece_exchange_value < best_exchange_value:
                gymnasium.health_check.append(
                        move    = alice_s_move_ex.move,
                        name    = 'eliminate171',
                        value   = f"{alice_s_move_ex.stringify_2():10} not_best")

            # それ以外の手は選択します。
            else:
                alice_s_move_list.append(alice_s_move_ex.move)
                gymnasium.health_check.append(
                        move    = alice_s_move_ex.move,
                        name    = 'eliminate171',
                        value   = f"{alice_s_move_ex.stringify_2():10} select")

        return alice_s_move_list


    return _eliminate_not_capture_not_positive(
            alice_s_move_ex_list    = alice_s_move_ex_list,
            gymnasium               = gymnasium)
