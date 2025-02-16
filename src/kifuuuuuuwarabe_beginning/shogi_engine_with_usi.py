import cshogi
import datetime
import random
import sys

from . import Mind
from .definitions_of_will import WillNotToBeCut88Bishop, WillNotToBuildRightWall, WillNotToMove37Pawn, WillSwingingRook, WillToClearWayOfRook


class ShogiEngineCompatibleWithUSIProtocol():
    """USIプロトコル互換の将棋エンジン
    """


    def __init__(self, config_doc):
        """初期化
        """

        # 設定ファイル
        self._config_doc = config_doc

        # 盤
        self._board = cshogi.Board()


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
            self._board.reset()

        # 指定局面に変更
        elif sfen_text[:5] == 'sfen ':
            self._board.set_sfen(sfen_text[5:])

        # 棋譜再生
        for move_as_usi in moves_text_as_usi:
            self._board.push_usi(move_as_usi)


    def go(self):
        """思考開始～最善手返却
        """

        if self._board.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if self._board.is_nyugyoku():
            """入玉宣言局面時"""

            # 勝利宣言
            print(f'bestmove win', flush=True)
            return

        # 一手詰めを詰める
        if not self._board.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := self._board.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""

                best_move = cshogi.move_to_usi(matemove)
                print('info score mate 1 pv {}'.format(best_move), flush=True)
                print(f'bestmove {best_move}', flush=True)
                return


        will_moves = list(self._board.legal_moves)


        # ［３七の歩を突かない意志］
        if self._config_doc['will']['will_not_to_move_37_pawn']:
            for i in range(len(will_moves))[::-1]:
                m = will_moves[i]
                mind = WillNotToMove37Pawn.will_on_move(board=self._board, move=m)
                if mind == Mind.WILL_NOT:
                    del will_moves[i]


        # ［右壁を作らない意志］
        if self._config_doc['will']['will_not_to_build_right_wall']:
            for i in range(len(will_moves))[::-1]:
                m = will_moves[i]
                mind = WillNotToBuildRightWall.will_on_move(board=self._board, move=m)
                if mind == Mind.WILL_NOT:
                    del will_moves[i]

        #print(f'★ go: ［振り飛車する意志］を残してるか尋ねる前の指し手数={len(will_moves)}', file=sys.stderr)


        # ［振り飛車をする意志］
        if self._config_doc['will']['will_swinging_rook']:
            if Mind.WILL == WillSwingingRook.will_on_board(board=self._board):
                print('★ go: 盤は［振り飛車する意志］を残しています', file=sys.stderr)

                for i in range(len(will_moves))[::-1]:
                    m = will_moves[i]

                    # ［飛車道を開ける意志］
                    if self._config_doc['will']['will_to_clear_way_of_rook']:
                        mind = WillToClearWayOfRook.will_on_move(board=self._board, move=m)
                        if mind == Mind.WILL_NOT:
                            del will_moves[i]

                    # ［振り飛車をする意志］
                    mind = WillSwingingRook.will_on_move(board=self._board, move=m)
                    if mind == Mind.WILL_NOT:
                        del will_moves[i]
            
            else:
                print('★ go: 盤は［振り飛車する意志］はありません', file=sys.stderr)
                pass

        # #print(f'★ go: ［振り飛車する意志］を残してるか尋ねた後の指し手数={len(will_moves)}', file=sys.stderr)


        print(f'★ go: ［８八の角を素抜かれない意志］を残してるか尋ねる前の指し手数={len(will_moves)}', file=sys.stderr)

        # １手指してから判定
        for i in range(len(will_moves))[::-1]:
            m = will_moves[i]
            self._board.push(m)   # １手指す

            # ［８八の角を素抜かれない意志］
            if self._config_doc['will']['will_not_to_be_cut_88_bishop']:
                mind = WillNotToBeCut88Bishop.have_will_after_moving_on_board(self._board)
                if mind == Mind.WILL_NOT:
                    del will_moves[i]

            self._board.pop() # １手戻す

        print(f'★ go: ［８八の角を素抜かれない意志］を残してるか尋ねた後の指し手数={len(will_moves)}', file=sys.stderr)


        # 指し手が全部消えてしまった場合、何でも指すようにします
        if len(will_moves) < 1:
            will_moves = list(self._board.legal_moves)


        # １手指す（投了のケースは対応済みなので、ここで対応しなくていい）
        best_move = cshogi.move_to_usi(random.choice(will_moves))


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


    def do(self, cmd):
        """一手指す
        example: ７六歩
            code: do 7g7f
        """
        self._board.push_usi(cmd[1])


    def undo(self):
        """一手戻す
            code: undo
        """
        self._board.pop()



    def test(self):
        """TODO 使い終わったら消す
        """
        from .sente_perspective import Ban, Helper, Ji

        ji = Ji(self._board)
        ban = Ban(self._board)

        # for suji in range(1, 10):
        #     for dan in range(1, 10):
        #         masu = Helper.suji_dan_to_masu(suji, dan)
        #         print(f'{masu=:2} {ban.masu(masu)=:2}')

        if ji.pc(cshogi.BISHOP) != cshogi.BBISHOP:
            raise ValueError('先手の角')

        self._board.push_usi('7g7f')

        if ji.pc(cshogi.BISHOP) != cshogi.WBISHOP:
            raise ValueError('後手の角')

        # if self._board.piece(ban.masu(88)) == ji.pc(cshogi.BISHOP):
        #     print('８八は自角だ')
        # else:
        #     print(f'８八は自角でない {self._board.piece(ban.masu(88))} {ji.pc(cshogi.BISHOP)=}')

        # if self._board.piece(ban.masu(79)) == ji.pc(cshogi.SILVER):
        #     print('７九は自銀だ')
        # else:
        #     print(f'７九は自銀でない')

