import cshogi
import datetime
import random
import sys

from .models import Table
from .usi_api import Go
from .views import TableView


class ShogiEngineCompatibleWithUSIProtocol():
    """USIプロトコル互換の将棋エンジン
    """


    def __init__(self, config_doc):
        """初期化
        """

        # 設定ファイル
        self._config_doc = config_doc

        # 盤
        self._table = Table.create_table()


    def start_usi_loop(self):
        """USIループ開始
        """

        while True:

            # 入力
            cmd = input().split(' ', 1)

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
            #       code: will
            elif cmd[0] == 'will':
                self.test_will()

            # テスト
            #       code: test
            elif cmd[0] == 'test':
                self.test()


    def usi(self):
        """USIエンジン握手
        """
        print(f'id name {self._config_doc['engine']['name']}')
        print('usiok', flush=True)


    def isready(self):
        """対局準備
        """
        print('readyok', flush=True)


    def usinewgame(self):
        """新しい対局
        """
        print(f"[{datetime.datetime.now()}] usinewgame end", flush=True)


    def position(self, cmd):
        """局面データ解析
        """
        pos = cmd[1].split('moves')
        sfen_text = pos[0].strip()
        # 区切りは半角空白１文字とします
        moves_text = (pos[1].split(' ') if len(pos) > 1 else [])
        self.position_detail(sfen_text, moves_text)


    def position_detail(self, sfen_text, moves_text_as_usi):
        """局面データ解析
        """

        # 平手初期局面に変更
        if sfen_text == 'startpos':
            self._table.reset()

        # 指定局面に変更
        elif sfen_text[:5] == 'sfen ':
            self._table.set_sfen(sfen_text[5:])

        # 棋譜再生
        for move_as_usi in moves_text_as_usi:
            self._table.push_usi(move_as_usi)


    def go(self):
        """思考開始～最善手返却
        """

        if self._table.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if self._table.is_nyugyoku():
            """入玉宣言局面時"""

            # 勝利宣言
            print(f'bestmove win', flush=True)
            return

        # 一手詰めを詰める
        if not self._table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""

                best_move = cshogi.move_to_usi(matemove)
                print('info score mate 1 pv {}'.format(best_move), flush=True)
                print(f'bestmove {best_move}', flush=True)
                return


        will_play_moves = Go.get_will_play_moves(
                config_doc=self._config_doc,
                table=self._table,
                will_play_moves=list(self._table.legal_moves))


        # 指し手が全部消えてしまった場合、何でも指すようにします
        if len(will_play_moves) < 1:
            will_play_moves = list(self._table.legal_moves)


        # １手指す（投了のケースは対応済みなので、ここで対応しなくていい）
        best_move = cshogi.move_to_usi(random.choice(will_play_moves))


        print(f"info depth 0 seldepth 0 time 1 nodes 0 score cp 0 string Go kifuuuuuuWarabe")
        print(f'bestmove {best_move}', flush=True)


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
        board_view = TableView(self._table)
        print(board_view.stringify())


    def do(self, cmd):
        """一手指す
        example: ７六歩
            code: do 7g7f
        """
        self._table.push_usi(cmd[1])


    def undo(self):
        """一手戻す
            code: undo
        """
        self._table.pop()


    def test_will(self):
        """テスト
        """

        if self._table.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if self._table.is_nyugyoku():
            """入玉宣言局面時"""

            # 勝利宣言
            print(f'bestmove win', flush=True)
            return

        # 一手詰めを詰める
        if not self._table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""

                best_move = cshogi.move_to_usi(matemove)
                print('info score mate 1 pv {}'.format(best_move), flush=True)
                print(f'bestmove {best_move}', flush=True)
                return


        def print_moves(will_play_moves):
            print('----ここから----', flush=True, file=sys.stderr)

            for move in will_play_moves:
                print(f'willmove {cshogi.move_to_usi(move)}', flush=True, file=sys.stderr)

            print(f'----ここまで----', flush=True, file=sys.stderr)


        will_play_moves = list(self._table.legal_moves)


        print(f'★ go: ［３七の歩を突かない意志］を残してるか尋ねる前の指し手数={len(will_play_moves)}', file=sys.stderr)
        will_play_moves = Go.get_will_not_to_move_37_pawn(
                config_doc=self._config_doc,
                table=self._table,
                will_play_moves=will_play_moves)
        print(f'★ go: ［３七の歩を突かない意志］を残してるか尋ねた後の指し手数={len(will_play_moves)}', file=sys.stderr)
        print_moves(will_play_moves)


        print(f'★ go: ［右壁を作らない意志］を残してるか尋ねる前の指し手数={len(will_play_moves)}', file=sys.stderr)
        will_play_moves = Go.get_will_not_to_build_right_wall(
                config_doc=self._config_doc,
                table=self._table,
                will_play_moves=will_play_moves)
        print(f'★ go: ［右壁を作らない意志］を残してるか尋ねた後の指し手数={len(will_play_moves)}', file=sys.stderr)
        print_moves(will_play_moves)


        print(f'★ go: ［振り飛車する意志］を残してるか尋ねる前の指し手数={len(will_play_moves)}', file=sys.stderr)
        will_play_moves = Go.get_will_swinging_rook(
                config_doc=self._config_doc,
                table=self._table,
                will_play_moves=will_play_moves)
        print(f'★ go: ［振り飛車する意志］を残してるか尋ねた後の指し手数={len(will_play_moves)}', file=sys.stderr)
        print_moves(will_play_moves)


        print(f'★ go: ［８八の角を素抜かれない意志］を残してるか尋ねる前の指し手数={len(will_play_moves)}', file=sys.stderr)
        will_play_moves = Go.get_will_not_to_be_cut_88_bishop(
                config_doc=self._config_doc,
                table=self._table,
                will_play_moves=will_play_moves)
        print(f'★ go: ［８八の角を素抜かれない意志］を残してるか尋ねた後の指し手数={len(will_play_moves)}', file=sys.stderr)
        print_moves(will_play_moves)


    def test(self):
        """TODO 使い終わったら消す
        """
        from .sente_perspective import Ban, Helper, Ji

        ji = Ji(self._table)
        ban = Ban(self._table)

        # for suji in range(1, 10):
        #     for dan in range(1, 10):
        #         masu = Helper.suji_dan_to_masu(suji, dan)
        #         print(f'{masu=:2} {ban.masu(masu)=:2}')

        if ji.pc(cshogi.BISHOP) != cshogi.BBISHOP:
            raise ValueError('先手の角')

        self._table.push_usi('7g7f')

        if ji.pc(cshogi.BISHOP) != cshogi.WBISHOP:
            raise ValueError('後手の角')

        # if self._table.piece(ban.masu(88)) == ji.pc(cshogi.BISHOP):
        #     print('８八は自角だ')
        # else:
        #     print(f'８八は自角でない {self._table.piece(ban.masu(88))} {ji.pc(cshogi.BISHOP)=}')

        # if self._table.piece(ban.masu(79)) == ji.pc(cshogi.SILVER):
        #     print('７九は自銀だ')
        # else:
        #     print(f'７九は自銀でない')

        table = self._table.copy_table()
        table_view = TableView(table=table)
        print(table_view.stringify())
