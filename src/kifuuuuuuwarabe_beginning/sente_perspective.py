"""手番を持っている側視点でプログラムを記述できるようにする仕組み。
"""
import cshogi

from .models import Masu, Square


class Ban():
    """盤
    """


    def __init__(self, table, after_moving=False):
        """
        Parameters
        ----------
        after_moving : bool
            １手指した後か。（相手の番になっています）
        """
        self._table = table
        self._after_moving = after_moving


    def is_opponent_turn(self):
        return self._table.turn == cshogi.WHITE and not self._after_moving


    def masu(self, masu):
        """マス番号。先手の sq に変換する。
        """
        if self.is_opponent_turn():
            return self.suji_dan(
                    suji=Helper.masu_to_suji(masu),
                    dan=Helper.masu_to_dan(masu))

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


    def suji_range(self, start, end):
        if self.is_opponent_turn():
            return range(9 - end, 9 - start)    # masu → sq 変換しながら、１８０°回転

        return range(start - 1, end - 1)


    def dan_range(self, start, end):
        return self.suji_range(start, end)      # 処理内容は同じ


    def top_left(self, masu):
        """左上
        """

        masu_obj = Masu(masu)

        # １段目だ
        if self.masu(masu) == self.dan(1):
            return None

        # ９列目だ
        if self.suji(masu_obj.to_suji()) == self.suji(9):
            return None

        rel_sq = 8

        if self.is_opponent_turn():
            rel_sq *= -1

        return self.masu(masu) + rel_sq


    def bottom_right(self, masu):
        """右下
        """

        masu_obj = Masu(masu)

        # ９段目だ
        if self.masu(masu) == self.dan(9):
            return None

        # １列目だ
        if self.suji(masu_obj.to_suji()) == self.suji(1):
            return None

        rel_sq = -8

        if self.is_opponent_turn():
            rel_sq *= -1

        return self.masu(masu) + rel_sq


class Comparison():
    """［比較］
    """
    def __init__(self, table, after_moving=False):
        self._table = table
        self._after_moving = after_moving


    def is_opponent_turn(self):
        return self._table.turn == cshogi.WHITE and not self._after_moving


    def swap(self, a, b):
        if self.is_opponent_turn():
            return b, a
        
        return a, b


class Ji():
    """［自］。手番を持っている側。
    """


    def __init__(self, table, after_moving=False):
        self._table = table
        self._after_moving = after_moving


    def is_opponent_turn(self):
        return self._table.turn == cshogi.WHITE and not self._after_moving


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

    # D

    @staticmethod
    def dan_to_rank(dan):
        return dan - 1


    # F

    @staticmethod
    def file_rank_to_masu(file, rank):
        return (file + 1) * 10 + (rank + 1)

    @staticmethod
    def file_rank_to_sq(file, rank):
        return file * 9 + rank


    # M

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


    # S

    @staticmethod
    def suji_to_file(suji):
        return suji - 1


    @staticmethod
    def suji_dan_to_masu(suji, dan):
        return suji * 10 + dan

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


    # T

    @staticmethod
    def turn_name(turn):
        if turn == 0:
            return 'Black'
        elif turn == 1:
            return 'White'
        else:
            raise ValueError(f'{turn=}')
