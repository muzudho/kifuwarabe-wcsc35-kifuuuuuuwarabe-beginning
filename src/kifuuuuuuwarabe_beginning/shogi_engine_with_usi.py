import cshogi
import datetime
import exshell as xs
import sys

from pathlib import Path
from .routines.layer_o3o0 import MovesReductionFilterRoutines
from .routines.layer_o4o0_usi import GoRoutines
from .models.layer_o1o0 import SearchResultStateModel
from .modules.exshell_mod.views import XsBoardView
from .views import HistoryView, TableView

PATH_TO_EXSHELL_CONFIG = './exshell_config.toml'
PATH_TO_EXSHELL_WORKSHEET = './temp/exshell_work.xlsx'


class ShogiEngineCompatibleWithUSIProtocol():
    """［USIプロトコル互換の将棋エンジン］
    """


    def __init__(self, gymnasium):
        """［初期化］

        Parameters
        ----------
        gymnasium : GymnasiumModel
            ［体育館］
            記憶は全部この中に詰め込めます。
        """
        self._gymnasium = gymnasium


    def start_usi_loop(self):
        """USIループ開始
        """

        while True:

            # 入力
            cmd = input().split(' ', 1)
            #print(f"★ [shogi_engine_with_usi.py > start_usi_loop] {cmd=}")

            # USIエンジン握手
            if cmd[0] == 'usi':
                self.usi()

            # 対局準備
            elif cmd[0] == 'isready':
                self.isready()

            # 新しい対局
            elif cmd[0] == 'usinewgame':
                self.usinewgame()

            # 局面データ解析
            elif cmd[0] == 'position':
                self.position(cmd)

            # 思考開始～最善手返却
            elif cmd[0] == 'go':
                self.go()

            # 中断
            elif cmd[0] == 'stop':
                self.stop()

            # 対局終了
            elif cmd[0] == 'gameover':
                self.gameover(cmd)

            # アプリケーション終了
            elif cmd[0] == 'quit':
                break

            # 以下、独自拡張
            # --------------

            # 盤表示
            #       code: board
            elif cmd[0] == 'board':
                self.board(cmd)

            # 盤表示
            #       code: xs_board
            elif cmd[0] == 'xs_board':
                self.xs_board(cmd)

            # 棋譜表示
            #       code: history
            elif cmd[0] == 'history':
                self.history(cmd)

            # 一手指す
            # example: ７六歩
            #       code: do 7g7f
            elif cmd[0] == 'do':
                self.do(cmd)

            # 一手戻す
            #       code: undo
            elif cmd[0] == 'undo':
                self.undo()

            # エクシェル
            #       code: use_exshell
            elif cmd[0] == 'use_exshell':
                self.use_exshell()

            # 静止探索のテスト
            #       code: go_qs
            elif cmd[0] == 'go_qs':
                self.go_qs(cmd)

            # テスト
            #       code: march
            elif cmd[0] == 'march':
                self.test_will()

            # テスト
            #       code: test
            elif cmd[0] == 'test':
                self.test()

            #print(f"★ [shogi_engine_with_usi.py > start_usi_loop] end loop.")


    def usi(self):
        """USIエンジン握手
        """
        print(f"id name {self._gymnasium.config_doc['engine']['name']}")
        print('usiok', flush=True)


    def isready(self):
        """対局準備
        """
        print('readyok', flush=True)


    def usinewgame(self):
        """［新しい対局］
        """

        self._gymnasium.on_new_game()   # 体育館の［初期化］

        # プロトコルにない独自出力
        message = f"[{datetime.datetime.now()}] usinewgame end"
        print(message, flush=True)


    def position(self, cmd):
        """局面データ解析
        """
        pos = cmd[1].split('moves')
        sfen_text = pos[0].strip()

        # pos[1]は半角空白から始まるので、.lstrip() で先頭の空白を除去します。
        # 区切りは半角空白１文字とします。
        move_usi_list = (pos[1].lstrip().split(' ') if len(pos) > 1 else [])

        # 平手初期局面に変更。
        if sfen_text == 'startpos':
            self._gymnasium.table.reset()

        # 指定局面に変更。
        elif sfen_text[:5] == 'sfen ':
            self._gymnasium.table.set_sfen(sfen_text[5:])

        # 盤をスキャン。
        self._gymnasium.np_value = self._gymnasium.piece_value_tao.scan_table()

        #print(f"★ [shogi_engine_with_usi.py > position] before replay.")

        # 棋譜再生。
        for move_as_usi in move_usi_list:
            #print(f"★ [shogi_engine_with_usi.py > position] {move_as_usi=}")
            self._gymnasium.do_move_o1x(
                    move = self._gymnasium.table.move_from_usi(move_as_usi))

        #print(f"★ [shogi_engine_with_usi.py > position] after replay.")

        self._gymnasium.on_position(
                command = f'{cmd[0]} {cmd[1]}')


    def go(self):
        """思考開始～最善手返却
        """

        result_of_go = GoRoutines.start_with_health_check(
                move_list   = list(self._gymnasium.table.legal_moves),
                gymnasium   = self._gymnasium)

        if result_of_go.search_result_state_model == SearchResultStateModel.GAME_OVER:
            # 投了。
            print(f'bestmove resign', flush=True)
            return

        if result_of_go.search_result_state_model == SearchResultStateModel.NYUGYOKU_WIN:
            # 入玉宣言勝ち。
            print(f'bestmove win', flush=True)
            return

        best_move_as_usi = cshogi.move_to_usi(result_of_go.best_move)

        if result_of_go.search_result_state_model == SearchResultStateModel.MATE_IN_1_MOVE:
            # １手詰め時。

            print('info score mate 1 pv {}'.format(best_move_as_usi), flush=True)
            print(f'bestmove {best_move_as_usi}', flush=True)
            return

        print(f"info depth 0 seldepth 0 time 1 nodes {result_of_go._number_of_visited_nodes} score cp 0 string Number of branches of first move: {result_of_go.length_by_cshogi} -> {result_of_go.length_of_quiescence_search_by_kifuwarabe} -> {result_of_go.length_by_kifuwarabe}")
        print(f'bestmove {best_move_as_usi}', flush=True)


    def stop(self):
        """中断
        """
        print('bestmove resign', flush=True)


    def gameover(self, cmd):
        """対局終了
        """

        if 2 <= len(cmd):
            # 負け
            if cmd[1] == 'lose':
                print("（＞＿＜）負けた")

            # 勝ち
            elif cmd[1] == 'win':
                print("（＾▽＾）勝ったぜ！")

            # 持将棋
            elif cmd[1] == 'draw':
                print("（ー＿ー）持将棋か～")

            # その他
            else:
                print(f"（・＿・）何だろな？：'{cmd[1]}'")


    def board(self, cmd):
        board_view = TableView(gymnasium=self._gymnasium)
        print(board_view.stringify())


    def xs_board(self, cmd):
        try:
            XsBoardView().render(
                    gymnasium=self._gymnasium)
        except Exception as ex:
            print(f"エクシェルによる盤表示に失敗しました。 {ex}")


    def do(self, cmd):
        """一手指す
        example: ７六歩
            code: do 7g7f
        """
        self._gymnasium.do_move_o1x(
                move = self._gymnasium.table.move_from_usi(cmd[1]))


    def undo(self):
        """一手戻す
            code: undo
        """
        self._gymnasium.undo_move_o1x()


    def history(self, cmd):
        history_view = HistoryView(self._gymnasium.table)
        print(f"""\

{history_view.stringify()}
""")


    def use_exshell(self):
        # ［エクシェル・ビルダー］生成
        exshell_builder = xs.ExshellBuilder(
                abs_path_to_workbook=Path(PATH_TO_EXSHELL_WORKSHEET).resolve())

        # ［エクシェル設定ファイル］読込
        exshell_builder.load_config(
                abs_path=Path(PATH_TO_EXSHELL_CONFIG).resolve(),
                create_if_not_exists=True)

        # エクシェル設定ファイルが不完全ならチュートリアル開始
        if not exshell_builder.config_is_ok():
            exshell_builder.start_tutorial()

        # ［エクシェル］生成
        self._gymnasium.exshell = exshell_builder.build()
        exshell_builder = None


    def go_qs(self, cmd):
        """静止探索のテスト。
        example: ７六歩
            code: go_qs 7g7f
        """
        move_list = [
            self._gymnasium.table.move_from_usi(cmd[1])
        ]

        self._gymnasium.health_check_qs_model.start_monitor()

        result_of_go = GoRoutines.start_with_health_check(
                move_list   = move_list,
                gymnasium   = self._gymnasium)

        self._gymnasium.health_check_qs_model.end_monitor()

        print(f"end go_qs")


    def test_will(self):
        """テスト
        """

        if self._gymnasium.table.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if self._gymnasium.table.is_nyugyoku():
            """入玉宣言勝ち局面時"""

            # 入玉宣言勝ち
            print(f'bestmove win', flush=True)
            return

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""

                best_move = cshogi.move_to_usi(matemove)
                print('info score mate 1 pv {}'.format(best_move), flush=True)
                print(f'bestmove {best_move}', flush=True)
                return


        def print_moves(remaining_moves):
            print('----ここから----', flush=True, file=sys.stderr)

            for move in remaining_moves:
                print(f'willmove {cshogi.move_to_usi(move)}', flush=True, file=sys.stderr)

            print(f'----ここまで----', flush=True, file=sys.stderr)


        remaining_moves = list(self._gymnasium.table.legal_moves)


        print(f'★ go: ［３七の歩を突かない］意志を残してるか尋ねる前の指し手数={len(remaining_moves)}', file=sys.stderr)
        remaining_moves = MovesReductionFilterRoutines.get_will_not_to_move_37_pawn(
                config_doc      = self._gymnasium.config_doc,
                table           = self._gymnasium.table,
                remaining_moves = remaining_moves)
        print(f'★ go: ［３七の歩を突かない］意志を残してるか尋ねた後の指し手数={len(remaining_moves)}', file=sys.stderr)
        print_moves(remaining_moves)


        print(f'★ go: ［右壁を作らない］意志を残してるか尋ねる前の指し手数={len(remaining_moves)}', file=sys.stderr)
        remaining_moves = MovesReductionFilterRoutines.get_do_not_build_right_wall(
                config_do       =self._gymnasium.config_doc,
                table           =self._gymnasium.table,
                remaining_moves =remaining_moves)
        print(f'★ go: ［右壁を作らない］意志を残してるか尋ねた後の指し手数={len(remaining_moves)}', file=sys.stderr)
        print_moves(remaining_moves)


        print(f'★ go: ［振り飛車をする］意志を残してるか尋ねる前の指し手数={len(remaining_moves)}', file=sys.stderr)
        remaining_moves = MovesReductionFilterRoutines.get_will_swinging_rook(
                config_doc      = self._gymnasium.config_doc,
                table           = self._gymnasium.table,
                remaining_moves = remaining_moves)
        print(f'★ go: ［振り飛車をする］意志を残してるか尋ねた後の指し手数={len(remaining_moves)}', file=sys.stderr)
        print_moves(remaining_moves)


        print(f'★ go: ［８八の角を素抜かれない］意志を残してるか尋ねる前の指し手数={len(remaining_moves)}', file=sys.stderr)
        remaining_moves = MovesReductionFilterRoutines.get_will_not_to_be_cut_88_bishop(
                config_doc      = self._gymnasium.config_doc,
                table           = self._gymnasium.table,
                remaining_moves = remaining_moves)
        print(f'★ go: ［８八の角を素抜かれない］意志を残してるか尋ねた後の指し手数={len(remaining_moves)}', file=sys.stderr)
        print_moves(remaining_moves)


    def test(self):
        """TODO 使い終わったら消す
        """
        board = cshogi.Board()
        board.push_usi('7g7f')
        board.push_usi('3c3d')
        board.push_usi('8h2b')
        board.push_usi('3a2b')
        board.push_usi('B*8h')  # 打
