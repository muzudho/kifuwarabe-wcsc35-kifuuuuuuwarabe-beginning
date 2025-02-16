"""手番を持っている側視点でプログラムを記述できるようにする仕組み。
"""
import cshogi


class Ban():
    """盤
    """


    def __init__(self, board):
        self._board = board
        self._turned = Turned(self._board)


    def masu(self, masu):
        """マス番号。先手の sq に変換する
        """
        if self._board.turn == cshogi.WHITE:
            suji = self._turned.suji(Helper.masu_to_suji(masu))
            dan = self._turned.dan(Helper.masu_to_dan(masu))
            masu = dan * 10 + suji  # １８０°回転

        return Helper.masu_to_file(masu) * 9 + Helper.masu_to_rank(masu)


class Comparison():
    """［比較］
    """
    def __init__(self, board):
        self._board = board


    def swap(self, a, b):
        if self._board.turn == cshogi.WHITE:
            return b, a
        
        return a, b


class Ji():
    """［自］。手番を持っている側。
    """


    def __init__(self, board):
        self._board = board


    def pc(self, piece_type):
        """駒種類を手番の駒へ変換
        """
        if self._board.turn == cshogi.WHITE:
            piece_type += 16

        return piece_type


class Turned():
    """手番を持っている側視点でプログラムを記述できるようにする仕組み。
    """


    def __init__(self, board):
        self._board = board


    def sign(self, number):
        if self._board.turn == cshogi.WHITE:
            number *= -1

        return number


    def masu(self, masu):
        if self._board.turn == cshogi.WHITE:
            suji = self.suji(Helper.masu_to_suji(masu))
            dan = self.dan(Helper.masu_to_dan(masu))
            masu = dan * 10 + suji

        return masu


    def suji(self, suji):
        if self._board.turn == cshogi.WHITE:
            suji = 10 - suji

        return suji


    def dan(self, dan):
        return self.suji(dan)    # 処理内容は同じ


class Helper():
    """ヘルパー関数集
    """


    @staticmethod
    def suji_to_file(suji):
        return suji - 1


    @staticmethod
    def dan_to_rank(dan):
        return dan - 1


    @staticmethod
    def masu_to_suji(masu):
        return masu // 10


    @staticmethod
    def masu_to_dan(masu):
        return masu % 10


    @staticmethod
    def masu_to_file(masu):
        return masu // 10 - 1


    @staticmethod
    def masu_to_rank(masu):
        return masu % 10 - 1


    @staticmethod
    def sq_to_masu(sq):
        return Helper.sq_to_suji(sq) * 10 + Helper.sq_to_dan(sq)


    @staticmethod
    def sq_to_suji(sq):
        return sq // 9 + 1


    @staticmethod
    def sq_to_dan(sq):
        return sq % 9 + 1


    @staticmethod
    def sq_to_file(sq):
        return sq // 9


    @staticmethod
    def sq_to_rank(sq):
        return sq % 9
