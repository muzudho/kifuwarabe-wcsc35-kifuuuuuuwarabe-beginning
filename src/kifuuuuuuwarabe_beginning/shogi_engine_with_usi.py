import cshogi
import datetime
import sys

from .logics_o1x import MovesReductionFilterLogics
from .logics_o4x_usi import GoLogic
from .models.layer_o1o0 import SearchResultStateModel
from .views import HistoryView, TableView


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
        print(f'id name {self._gymnasium.config_doc['engine']['name']}')
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

        result_of_go = GoLogic.Go(
                gymnasium = self._gymnasium)

        if result_of_go.search_result_state_model == SearchResultStateModel.RESIGN:
            # 投了。
            print(f'bestmove resign', flush=True)
            return

        if result_of_go.search_result_state_model == SearchResultStateModel.NYUGYOKU_WIN:
            # 勝利宣言。
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
        board_view = TableView(self._gymnasium.table)
        print(board_view.stringify())


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


    def test_will(self):
        """テスト
        """

        if self._gymnasium.table.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if self._gymnasium.table.is_nyugyoku():
            """入玉宣言局面時"""

            # 勝利宣言
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
        remaining_moves = MovesReductionFilterLogics.get_will_not_to_move_37_pawn(
                config_doc      = self._gymnasium.config_doc,
                table           = self._gymnasium.table,
                remaining_moves = remaining_moves)
        print(f'★ go: ［３七の歩を突かない］意志を残してるか尋ねた後の指し手数={len(remaining_moves)}', file=sys.stderr)
        print_moves(remaining_moves)


        print(f'★ go: ［右壁を作らない］意志を残してるか尋ねる前の指し手数={len(remaining_moves)}', file=sys.stderr)
        remaining_moves = MovesReductionFilterLogics.get_do_not_build_right_wall(
                config_do       =self._gymnasium.config_doc,
                table           =self._gymnasium.table,
                remaining_moves =remaining_moves)
        print(f'★ go: ［右壁を作らない］意志を残してるか尋ねた後の指し手数={len(remaining_moves)}', file=sys.stderr)
        print_moves(remaining_moves)


        print(f'★ go: ［振り飛車をする］意志を残してるか尋ねる前の指し手数={len(remaining_moves)}', file=sys.stderr)
        remaining_moves = MovesReductionFilterLogics.get_will_swinging_rook(
                config_doc      = self._gymnasium.config_doc,
                table           = self._gymnasium.table,
                remaining_moves = remaining_moves)
        print(f'★ go: ［振り飛車をする］意志を残してるか尋ねた後の指し手数={len(remaining_moves)}', file=sys.stderr)
        print_moves(remaining_moves)


        print(f'★ go: ［８八の角を素抜かれない］意志を残してるか尋ねる前の指し手数={len(remaining_moves)}', file=sys.stderr)
        remaining_moves = MovesReductionFilterLogics.get_will_not_to_be_cut_88_bishop(
                config_doc      = self._gymnasium.config_doc,
                table           = self._gymnasium.table,
                remaining_moves = remaining_moves)
        print(f'★ go: ［８八の角を素抜かれない］意志を残してるか尋ねた後の指し手数={len(remaining_moves)}', file=sys.stderr)
        print_moves(remaining_moves)


    def test(self):
        """TODO 使い終わったら消す
        """
        from .logics_o1x.helper import Helper
        from .layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel


        np = NineRankSidePerspectiveModel(self._gymnasium.table)

        # for suji in range(1, 10):
        #     for dan in range(1, 10):
        #         masu = Helper.suji_dan_to_masu(suji, dan)
        #         print(f'{masu=:2} {np.masu(masu)=:2}')

        # if np.ji_pc(cshogi.BISHOP) != cshogi.BBISHOP:
        #     raise ValueError('先手の角')

        # self._gymnasium.table.do_move_o1o1x(self._gymnasium.table.move_from_usi('7g7f'))

        # if np.ji_pc(cshogi.BISHOP) != cshogi.WBISHOP:
        #     raise ValueError('後手の角')

        # if self._gymnasium.table.piece(np.masu(88)) == np.ji_pc(cshogi.BISHOP):
        #     print('８八は自角だ')
        # else:
        #     print(f'８八は自角でない {self._gymnasium.table.piece(np.masu(88))} {np.ji_pc(cshogi.BISHOP)=}')

        # if self._gymnasium.table.piece(np.masu(79)) == np.ji_pc(cshogi.SILVER):
        #     print('７九は自銀だ')
        # else:
        #     print(f'７九は自銀でない')

        print(f"{self._gymnasium.table.sfen()=}")

        # 盤を複製
        copied_table = self._gymnasium.table.copy_table_with_0_moves()
        table_view = TableView(table=copied_table)
        print(table_view.stringify())   # 平手初期局面に戻ってる

        # 指定局面（現局面）の SFEN を取得（棋譜は付いていない）
        designated_sfen = copied_table.sfen()
        print(f"コピー盤 {designated_sfen=}")

        piece_moved_list = copied_table.copy_piece_moved_list()
        print(f"{piece_moved_list=}")
