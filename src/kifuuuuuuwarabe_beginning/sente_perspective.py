"""手番を持っている側視点でプログラムを記述できるようにする仕組み。
"""
import cshogi


class Ban():
    """盤
    """


    def __init__(self, board, after_moving=False):
        """
        Parameters
        ----------
        after_moving : bool
            １手指した後か。（相手の番になっています）
        """
        self._board = board
        self._after_moving = after_moving


    def is_opponent_turn(self):
        return self._board.turn == cshogi.WHITE and not self._after_moving


    def masu(self, masu):
        """マス番号。先手の sq に変換する。
        """
        if self.is_opponent_turn():
            return self.suji_dan(
                    suji=Helper.masu_to_suji(masu),
                    dan=Helper.masu_to_dan(masu))
            masu = dan * 10 + suji  # １８０°回転

        return Helper.masu_to_file(masu) * 9 + Helper.masu_to_rank(masu)


    def suji_dan(self, suji, dan):
        """筋と段番号。先手の sq に変換する。
        """
        if self.is_opponent_turn():
            return (9 - suji) * 9 + (9 - dan)  # masu → sq 変換しながら、１８０°回転

        return (suji - 1) * 9 + (dan - 1)


    def suji(self, suji):
        """筋番号。先手の file に変換する。
        """
        if self.is_opponent_turn():
            suji = 10 - suji

        return suji - 1


    def dan(self, dan):
        return self.suji(suji=dan)    # 処理内容は同じ


class Comparison():
    """［比較］
    """
    def __init__(self, board, after_moving=False):
        self._board = board
        self._after_moving = after_moving


    def is_opponent_turn(self):
        return self._board.turn == cshogi.WHITE and not self._after_moving


    def swap(self, a, b):
        if self.is_opponent_turn():
            return b, a
        
        return a, b


class Ji():
    """［自］。手番を持っている側。
    """


    def __init__(self, board, after_moving=False):
        self._board = board
        self._after_moving = after_moving


    def is_opponent_turn(self):
        return self._board.turn == cshogi.WHITE and not self._after_moving


    def pc(self, piece_type):
        """駒種類を手番の駒へ変換
        """
        if self.is_opponent_turn():
            piece = piece_type + 16
        else:
            piece = piece_type

        return piece


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
    def suji_dan_to_masu(suji, dan):
        return suji * 10 + dan


    @staticmethod
    def file_rank_to_masu(file, rank):
        return (file + 1) * 10 + (rank + 1)


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
