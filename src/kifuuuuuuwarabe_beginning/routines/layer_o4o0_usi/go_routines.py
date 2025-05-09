import cshogi
import random
import time

from ...models.layer_o1o0 import constants, ResultOfGoModel, SearchResultStateModel
from ...models.layer_o1o0o1o0_japanese import JapaneseMoveModel
from ...models.layer_o5o0_search import PrincipalVariationModel, SearchContextModel
from ...views import TableView
from ..layer_o4o_9o0_search import EndOfSearchRoutines, O0NoSearchRoutines, O1RootSearchRoutines, OutOfSearchRoutines, SearchRoutines
from ..layer_o3o0 import MovesPickupFilterRoutines, MovesReductionFilterRoutines


INFO_DEPTH_0 = 0


class GoRoutines:


    @staticmethod
    def start_with_health_check(move_list, gymnasium):
        """盤面が与えられるので、次の１手を返します。

        Parameters
        ----------
        move_list : list
            指し手のリスト。
        gymnasium : Gymnasium
            ［体育館］

        Returns
        -------
        result_of_go_model : ResultOfGoModel
            探索の結果。
        """
        gymnasium.health_check_go_model.on_go_started()

        result_of_go_model = _Go2nd.start_all_phases(
                move_list=move_list,
                gymnasium=gymnasium)

        gymnasium.health_check_go_model.on_go_finished()

        return result_of_go_model


class _Go2nd():


    @staticmethod
    def start_all_phases(move_list, gymnasium):
        """盤面が与えられるので、次の１手を返します。

        最初の１手だけの処理です。

        Parameters
        ----------
        move_list : list
            指し手のリスト。
        
        Returns
        -------
        result_of_go_model : ResultOfGoModel
            探索の結果。
        """

        for move in move_list:
            # 指し手のUSI表記に、独自形式を併記。
            move_jp_str = JapaneseMoveModel.from_move(
                    move    = move,
                    cap_pt  = gymnasium.table.piece_type(sq=cshogi.move_to(move)),
                    is_mars = False,
                    is_gote = gymnasium.table.is_gote).stringify()

            gymnasium.health_check_go_model.append_health(
                    move    = move,
                    name    = 'GO_move_jp',
                    value   = move_jp_str)

        length_by_cshogi                            = len(move_list)    # cshogi が示した合法手の数
        length_of_quiescence_search_by_kifuwarabe   = length_by_cshogi  # きふわらべ が静止探索で絞り込んだ指し手の数
        length_by_kifuwarabe                        = length_by_cshogi  # きふわらべ が最終的に絞り込んだ指し手の数
        #print(f"D-74: {len(all_regal_moves)=}")

        if gymnasium.table.is_game_over():
            """投了局面時。
            """
            gymnasium.thinking_logger_module.append_message(f"Game over.")
            return ResultOfGoModel(
                    search_result_state_model   = SearchResultStateModel.RESIGN,
                    alice_s_profit              = 0,
                    best_move                   = None,
                    length_by_cshogi            = length_by_cshogi,
                    length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                    length_by_kifuwarabe        = length_by_kifuwarabe,
                    number_of_visited_nodes     = 0)

        if gymnasium.table.is_nyugyoku():
            """入玉宣言勝ち局面時。
            """
            gymnasium.thinking_logger_module.append_message(f"Nyugyoku win.")
            return ResultOfGoModel(
                    search_result_state_model   = SearchResultStateModel.NYUGYOKU_WIN,
                    alice_s_profit              = 0,
                    best_move                   = None,
                    length_by_cshogi            = length_by_cshogi,
                    length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                    length_by_kifuwarabe        = length_by_kifuwarabe,
                    number_of_visited_nodes     = 0)

        # 一手詰めを詰める
        if not gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                gymnasium.thinking_logger_module.append_message(f"Ittedume.")
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

        old_all_legal_moves = move_list.copy()

        search_context_model = SearchContextModel(
                gymnasium = gymnasium)
        search_context_model.start_time = time.time()          # 探索開始時間
        search_context_model.restart_time = search_context_model.start_time   # 前回の計測開始時間

        (
            next_pv_list,
            number_of_visited_nodes
        ) = _main_search_at_first(
                remaining_moves         = move_list,
                search_context_model    = search_context_model)
        
        remaining_moves_qs, = EndOfSearchRoutines.eliminate_qs_171(
                pv_list     = next_pv_list,
                gymnasium   = gymnasium),

        search_context_model.end_time = time.time()    # 計測終了時間
        

        length_of_quiescence_search_by_kifuwarabe   = len(remaining_moves_qs)
        gymnasium.thinking_logger_module.append_message(f"QS_select_length={length_of_quiescence_search_by_kifuwarabe}")

        # 指し手が全部消えたとき。ロールバックします。
        if len(remaining_moves_qs) == 0:
            remaining_moves_qs = old_all_legal_moves
            gymnasium.thinking_logger_module.append_message(f"QS is 0. Rollback to old_all_legal_moves. len={len(remaining_moves_qs)}.")
            for move in remaining_moves_qs:
                gymnasium.health_check_go_model.append_health(
                        move    = move,
                        name    = 'QS_select',
                        value   = 'QS_annihilation')

        else:
            for move in remaining_moves_qs:
                gymnasium.health_check_go_model.append_health(
                        move    = move,
                        name    = 'QS_select',
                        value   = 'QS_select')

        old_remaining_moves_qs = remaining_moves_qs.copy()

        # 枝の前でポジティブ・ルール
        remaining_moves_pr = MovesPickupFilterRoutines.on_node_entry_positive_main(
                remaining_moves = remaining_moves_qs,
                gymnasium       = gymnasium)
        
        if 0 < len(remaining_moves_pr):
            for move in remaining_moves_pr:
                gymnasium.health_check_go_model.append_health(
                        move    = move,
                        name    = 'PR_remaining',
                        value   = 'PR_remaining')

            # ピックアップされた手の中から選びます。
            remaining_moves_r = remaining_moves_pr

        else:
            # 合法手から、１手を選び出します。
            # （必ず、投了ではない手が存在します）
            #
            # ［指前］
            #       制約：
            #           指し手は必ず１つ以上残っています。
            remaining_moves_nr = MovesReductionFilterRoutines.on_node_entry_negative(
                    remaining_moves = remaining_moves_qs,
                    gymnasium       = gymnasium)
            length_by_kifuwarabe = len(remaining_moves_nr)
            gymnasium.thinking_logger_module.append_message(f"{length_by_kifuwarabe=}")

            if len(remaining_moves_nr) == 0:
                remaining_moves_nr = old_remaining_moves_qs
                gymnasium.thinking_logger_module.append_message(f"NR is 0. Rollback to QS. len={len(remaining_moves_nr)}.")

                for move in remaining_moves_nr:
                    gymnasium.health_check_go_model.append_health(
                            move    = move,
                            name    = 'NR_remaining',
                            value   = 'NR_cancel')
            else:
                for move in remaining_moves_nr:
                    gymnasium.health_check_go_model.append_health(
                            move    = move,
                            name    = 'NR_remaining',
                            value   = 'NR_remaining')

            remaining_moves_r = remaining_moves_nr

        # １手に絞り込む
        if gymnasium.config_doc['search']['there_is_randomness']:
            best_move = random.choice(remaining_moves_r)
        else:
            best_move = remaining_moves_r[0]
        
        gymnasium.health_check_go_model.append_health(
                move    = best_move,
                name    = 'BM_bestmove',
                value   =  True)
        
        # 指し手のUSI表記に、独自形式を併記。
        move_jp_str = JapaneseMoveModel.from_move(
                move    = best_move,
                cap_pt  = gymnasium.table.piece_type(sq=cshogi.move_to(best_move)),
                is_mars = False,
                is_gote = gymnasium.table.is_gote).stringify()

        gymnasium.thinking_logger_module.append_message(f"Best move={cshogi.move_to_usi(best_move)} {move_jp_str}")

        # ログ
        message = f"""\
{TableView(gymnasium=gymnasium).stringify()}

{gymnasium.health_check_go_model.stringify()}
"""
        
        if gymnasium.health_check_qs_model.enabled:
            message = f"""\
{message}

{gymnasium.health_check_qs_model.stringify()}
"""

        message = f"""\
{message}

GOREI COLLECTION
----------------
{gymnasium.gourei_collection_model.stringify()}
"""

        # TODO ネガティブ・ルールの一覧も表示したい。
        gymnasium.thinking_logger_module.append_message(message)
        # NOTE これを書くと、将棋ホームでフリーズ： print(message, file=sys.stderr)

        # ［指後］
        MovesReductionFilterRoutines.after_best_moving_o1o0(
                move        = best_move,
                gymnasium   = gymnasium)

        return ResultOfGoModel(
                search_result_state_model                   = SearchResultStateModel.BEST_MOVE,
                alice_s_profit                              = 0,
                best_move                                   = best_move,
                length_by_cshogi                            = length_by_cshogi,
                length_of_quiescence_search_by_kifuwarabe   = length_of_quiescence_search_by_kifuwarabe,
                length_by_kifuwarabe                        = length_by_kifuwarabe,
                number_of_visited_nodes                     = number_of_visited_nodes)


@staticmethod
def _main_search_at_first(remaining_moves, search_context_model):
    """探索。
    
    Returns
    -------
    remaining_moves : list
        指し手のリスト。
    number_of_visited_nodes : int
        ［訪問ノード数］
    """

    # 次のPVリストを集める
    # --------------------

    # ［ゼロPV］。［指し手］が追加されなければ、［終端外］がセットされるだけのものです。
    pv = PrincipalVariationModel.create_zeroth_pv(
            out_of_termination_is_gote_arg  = search_context_model.gymnasium.table.turn == cshogi.WHITE,
            search_context_model            = search_context_model)

    next_pv_list = [pv]

    # ノード訪問時
    # ------------

    # 各PV
    # ----

    
    # 履歴を全部指す
    # --------------

    # 手番の処理
    # ----------

    # （無し）探索不要なら。

    # （無し）［水平指し手一覧］をクリーニング。

    # （無し）［駒を取る手］がないことを、［静止］と呼ぶ。

    # （無し）［水平指し手一覧］を［PV］へ変換。

    # 縦の辺を伸ばす。（０階では、［終端外］判定するだけ）
    O0NoSearchRoutines.extend_vertical_edges_o0(pv_list=next_pv_list, search_context_model=search_context_model)

    # TODO 残りのPVリストを集める

    # TODO （奇数＋１階なら火星、偶数＋１階なら地球）が嫌な手は削除。

    # ０階で終了。
    if pv.termination_model_pv is not None:
        next_pv_list = [pv]

    else:
        # １階の操作A。
        (terminated_pv_list_1, live_pv_list) = O1RootSearchRoutines.main_a_o1(remaining_moves_o1=remaining_moves, pv=pv, search_context_model=search_context_model)

        # １階の操作B。
        if len(live_pv_list) != 0:
            # 縦の辺を伸ばす。
            O1RootSearchRoutines.extend_vertical_edges_o1(pv_list=live_pv_list, search_context_model=search_context_model)

            # FIXME この関数から、O2 の呼出を取り除きたい。
            (terminated_pv_list_2, live_pv_list) = O1RootSearchRoutines.main_b_o1_to_o2(live_pv_list=live_pv_list, parent_pv=pv, search_context_model=search_context_model)

        # 次のPVリストを集める
        next_pv_list = OutOfSearchRoutines.filtering_next_pv_list(
                terminated_pv_list_1    = terminated_pv_list_1,
                terminated_pv_list_2    = terminated_pv_list_2,
                live_pv_list            = live_pv_list)

    return next_pv_list, search_context_model.number_of_visited_nodes
