import cshogi
import random
import sys

from ...models.layer_o1o0 import constants, ResultOfGoModel, SearchResultStateModel
from ...models.layer_o5o0_qs import QuiescenceSearchForAllLegalMovesAtFirstModel
from ...views import TableView
from ..layer_o3o0 import MovesPickupFilterLogics, MovesReductionFilterLogics


class GoLogic():


    @staticmethod
    def start_with_health_check(gymnasium):
        """盤面が与えられるので、次の１手を返します。

        Returns
        -------
        best_move : int
            ［指す手］
        """
        gymnasium.health_check.on_go_started()

        go_2nd = _Go2nd(gymnasium)

        gymnasium.health_check.on_go_finished()

        return go_2nd.start_all_phases()


class _Go2nd():


    def __init__(self, gymnasium):
        self._gymnasium = gymnasium


    def start_all_phases(self):
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

        all_regal_moves = list(self._gymnasium.table.legal_moves)

        for move in all_regal_moves:
            self._gymnasium.health_check.append(
                    move    = move,
                    name    = 'legal',
                    value   =  True)

        length_by_cshogi        = len(all_regal_moves)  # cshogi が示した合法手の数
        length_of_quiescence_search_by_kifuwarabe   = length_by_cshogi  # きふわらべ が静止探索で絞り込んだ指し手の数
        length_by_kifuwarabe    = length_by_cshogi      # きふわらべ が最終的に絞り込んだ指し手の数
        #print(f"D-74: {len(all_regal_moves)=}")

        if self._gymnasium.table.is_game_over():
            """投了局面時。
            """
            self._gymnasium.thinking_logger_module.append(f"Game over.")
            return ResultOfGoModel(
                    search_result_state_model   = SearchResultStateModel.RESIGN,
                    alice_s_profit              = 0,
                    best_move                   = None,
                    length_by_cshogi            = length_by_cshogi,
                    length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                    length_by_kifuwarabe        = length_by_kifuwarabe,
                    number_of_visited_nodes     = 0)

        if self._gymnasium.table.is_nyugyoku():
            """入玉宣言局面時。
            """
            self._gymnasium.thinking_logger_module.append(f"Nyugyoku win.")
            return ResultOfGoModel(
                    search_result_state_model   = SearchResultStateModel.NYUGYOKU_WIN,
                    alice_s_profit              = 0,
                    best_move                   = None,
                    length_by_cshogi            = length_by_cshogi,
                    length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                    length_by_kifuwarabe        = length_by_kifuwarabe,
                    number_of_visited_nodes     = 0)

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                self._gymnasium.thinking_logger_module.append(f"Ittedume.")
                return ResultOfGoModel(
                        search_result_state_model   = SearchResultStateModel.MATE_IN_1_MOVE,
                        alice_s_profit              = 0,
                        best_move                   = matemove,
                        length_by_cshogi            = length_by_cshogi,
                        length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                        length_by_kifuwarabe        = length_by_kifuwarabe,
                        number_of_visited_nodes     = 0)

        ################
        # MARK: 静止探索
        ################

        old_all_legal_moves = all_regal_moves.copy()

        (
            remaining_moves_qs,
            number_of_visited_nodes
        ) = _quiescence_search_at_first(
                remaining_moves = all_regal_moves,
                gymnasium       = self._gymnasium)
        length_of_quiescence_search_by_kifuwarabe   = len(remaining_moves_qs)
        self._gymnasium.thinking_logger_module.append(f"QS_select_length={length_of_quiescence_search_by_kifuwarabe}")

        if len(remaining_moves_qs) == 0:
            remaining_moves_qs = old_all_legal_moves
            self._gymnasium.thinking_logger_module.append(f"QS is 0. Rollback to old_all_legal_moves. len={len(remaining_moves_qs)}.")
            for move in remaining_moves_qs:
                self._gymnasium.health_check.append(
                        move    = move,
                        name    = 'QS_select',
                        value   = 'QS_cancel')

        else:
            for move in remaining_moves_qs:
                self._gymnasium.health_check.append(
                        move    = move,
                        name    = 'QS_select',
                        value   = 'QS_select')

        old_remaining_moves_qs = remaining_moves_qs.copy()

        # 枝の前でポジティブ・ルール
        remaining_moves_pr = MovesPickupFilterLogics.before_branches_o1x(
                remaining_moves = remaining_moves_qs,
                gymnasium       = self._gymnasium)
        
        if 0 < len(remaining_moves_pr):
            # ピックアップされた手の中から選びます。
            remaining_moves_r = remaining_moves_pr

        else:
            # 合法手から、１手を選び出します。
            # （必ず、投了ではない手が存在します）
            #
            # ［指前］
            #       制約：
            #           指し手は必ず１つ以上残っています。
            remaining_moves_nr = MovesReductionFilterLogics.before_branches_o1x(
                    remaining_moves = remaining_moves_qs,
                    gymnasium       = self._gymnasium)
            length_by_kifuwarabe = len(remaining_moves_nr)
            self._gymnasium.thinking_logger_module.append(f"{length_by_kifuwarabe=}")

            if len(remaining_moves_nr) == 0:
                remaining_moves_nr = old_remaining_moves_qs
                self._gymnasium.thinking_logger_module.append(f"NR is 0. Rollback to QS. len={len(remaining_moves_nr)}.")

                for move in remaining_moves_nr:
                    self._gymnasium.health_check.append(
                            move    = move,
                            name    = 'NR_remaining',
                            value   = 'NR_cancel')
            else:
                for move in remaining_moves_nr:
                    self._gymnasium.health_check.append(
                            move    = move,
                            name    = 'NR_remaining',
                            value   = 'NR_remaining')

            remaining_moves_r = remaining_moves_nr

        # １手に絞り込む
        if self._gymnasium.config_doc['search']['there_is_randomness']:
            best_move = random.choice(remaining_moves_r)
        else:
            best_move = remaining_moves_r[0]
        
        self._gymnasium.health_check.append(
                move    = best_move,
                name    = 'BM_bestmove',
                value   =  True)
        self._gymnasium.thinking_logger_module.append(f"Best move={cshogi.move_to_usi(best_move)}")

        # ログ
        message = f"""\
{TableView(self._gymnasium.table).stringify()}
HEALTH CHECK
------------
{self._gymnasium.health_check.stringify()}

{self._gymnasium.gourei_collection_model.stringify()}
"""
        # TODO ネガティブ・ルールの一覧も表示したい。
        self._gymnasium.thinking_logger_module.append(message)
        # NOTE これを書くと、将棋ホームでフリーズ： print(message, file=sys.stderr)

        # ［指後］
        MovesReductionFilterLogics.after_best_moving_o1o0(
                move        = best_move,
                gymnasium   = self._gymnasium)

        return ResultOfGoModel(
                search_result_state_model   = SearchResultStateModel.BEST_MOVE,
                alice_s_profit              = 0,
                best_move                   = best_move,
                length_by_cshogi            = length_by_cshogi,
                length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                length_by_kifuwarabe        = length_by_kifuwarabe,
                number_of_visited_nodes     = number_of_visited_nodes)


def _quiescence_search_at_first(remaining_moves, gymnasium):
    """静止探索。
    
    Returns
    -------
    remaining_moves : list
        指し手のリスト。
    number_of_visited_nodes : int
        ［訪問ノード数］
    """
    max_depth                   = gymnasium.config_doc['search']['capture_depth']   # 2

    # 駒の取り合いのための静止探索
    qs_at_first = QuiescenceSearchForAllLegalMovesAtFirstModel(
            max_depth   = max_depth,
            gymnasium   = gymnasium)

    if max_depth < 1:
        #print(f"D-132: _q uiescence_search {max_depth=}")
        return remaining_moves, 0

    all_backwards_plot_models_at_first = qs_at_first.search_at_first(
            #best_plot_model_in_older_sibling    = None,
            depth                               = max_depth,
            is_mars                             = False,
            #beta_cutoff_value                   = constants.value.BETA_CUTOFF_VALUE,    # すごい高い点数。
            remaining_moves                     = remaining_moves)

    #print(f"{alice_s_best_piece_value=} {len(all_backwards_plot_models_at_first)=}")
    number_of_visited_nodes = qs_at_first.search_model.number_of_visited_nodes

    def _eliminate_not_capture_not_positive(all_backwards_plot_models_at_first, gymnasium):
        """次の１つの手は、候補に挙げる必要がないので除去します。
        （１）駒を取らない手で非正の手（最高点のケースを除く）。このとき、［零点の手］があるかどうか調べます。
        次の手は、候補に挙げる必要がないので除去します。
        （２）最高点でない手。
        （３）［零点の手」が存在し、かつ、負の手。（リスクヘッジの手でもないから）
        それ以外の手は選択します。

        Returns
        -------
        alice_s_move_list : list(int)
            指し手のリスト。
        """
        alice_s_move_list = []
        exists_zero_value_move = False

        # まず、最高点を調べます。
        best_exchange_value = constants.value.NOTHING_CAPTURE_MOVE
        for backwards_plot_model in all_backwards_plot_models_at_first:
            if best_exchange_value < backwards_plot_model.peek_piece_exchange_value_on_earth:
                best_exchange_value = backwards_plot_model.peek_piece_exchange_value_on_earth

        # 最高点が 0 点のケース。 FIXME 千日手とかを何点に設定しているか？
        if best_exchange_value == 0:
            exists_zero_value_move = True

        gymnasium.thinking_logger_module.append(f"all_backwards_plot_models_at_first len={len(all_backwards_plot_models_at_first)}")

        for backwards_plot_model in all_backwards_plot_models_at_first:

            gymnasium.health_check.append(
                    move    = backwards_plot_model.peek_move,
                    name    = 'QS_backwards_plot_model',
                    value   = backwards_plot_model)

            # （１）駒を取らない手で非正の手（最高点のケースを除く）。
            if not backwards_plot_model.is_capture_at_last and backwards_plot_model.peek_piece_exchange_value_on_earth < 1 and backwards_plot_model.peek_piece_exchange_value_on_earth != best_exchange_value:
                if backwards_plot_model.peek_piece_exchange_value_on_earth == 0:
                    exists_zero_value_move = True
                
                gymnasium.health_check.append(
                        move    = backwards_plot_model.peek_move,
                        name    = 'eliminate171',
                        value   = f"{backwards_plot_model.stringify_2():10} not_cap_not_posite")

            # （２）最高点でない手。
            elif backwards_plot_model.peek_piece_exchange_value_on_earth < best_exchange_value:
                gymnasium.health_check.append(
                        move    = backwards_plot_model.peek_move,
                        name    = 'eliminate171',
                        value   = f"{backwards_plot_model.stringify_2():10} not_best")

            # （３）リスクヘッジにならない手
            elif exists_zero_value_move and backwards_plot_model.peek_piece_exchange_value_on_earth < 0:
                gymnasium.health_check.append(
                        move    = backwards_plot_model.peek_move,
                        name    = 'eliminate171',
                        value   = f"{backwards_plot_model.stringify_2():10} not_risk_hedge")

            # それ以外の手は選択します。
            else:
                alice_s_move_list.append(backwards_plot_model.peek_move)
                gymnasium.health_check.append(
                        move    = backwards_plot_model.peek_move,
                        name    = 'eliminate171',
                        value   = f"{backwards_plot_model.stringify_2():10} ok")

        return alice_s_move_list


    return (
        _eliminate_not_capture_not_positive(
                all_backwards_plot_models_at_first  = all_backwards_plot_models_at_first,
                gymnasium                           = gymnasium),
        number_of_visited_nodes
    )
