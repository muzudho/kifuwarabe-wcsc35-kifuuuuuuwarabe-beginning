"""常に［大盤に向かって下側］視点でコーディングするようにするためのクラスです。［大盤に向かって下側］視点でコーディングすることで、現在の手番の視点に変換してくれます。
"""
import cshogi

from ..layer_o1o0 import MasuModel, SquareModel
from ...routines.layer_o1o0.helper_routines import HelperRoutines


class NineRankSidePerspectiveModel():
    """［筆記具のペン］
    常に［将棋盤の９段目の方からの視点］でコーディングできるようにするための仕組みです。
    """


    def __init__(self, table, after_moving=False):
        """［初期化］

        Parameters
        ----------
        after_moving : bool
            １手指した後か。（相手の番になっています）
        """
        self._table = table
        self._after_moving = after_moving


    def is_opponent_turn(self):
        if self._after_moving:
            return self._table.turn == cshogi.BLACK
        else:
            return self._table.turn == cshogi.WHITE
    
        #return self._table.turn == cshogi.WHITE and not self._after_moving

    ################
    # MARK: 盤上関連
    ################

    def masu(self, masu):
        """［マス番号］
        
        先手の sq に変換します。
        """
        if self.is_opponent_turn():
            return self.suji_dan(
                    suji=HelperRoutines.masu_to_suji(masu),
                    dan=HelperRoutines.masu_to_dan(masu))

        return HelperRoutines.masu_to_file(masu) * 9 + HelperRoutines.masu_to_rank(masu)


    def file_rank(self, file, rank):
        """［ファイルとランクで示されるスクウェア番号］
        
        先手の sq に変換します。
        """
        if self.is_opponent_turn():
            return (9 - file) * 9 + (9 - rank)  # masu → sq 変換しながら、１８０°回転

        return (file - 1) * 9 + (rank - 1)


    def suji_dan(self, suji, dan):
        """［筋と段で示されるスクウェア番号］
        
        先手の sq に変換します。
        """
        return self.file_rank(file=suji, rank=dan)  # 処理内容は file_rank() と同じ


    def file(self, file):
        """［ファイル番号］
        
        先手の file に変換します。
        変域： 1 ～ 9。
        """
        if self.is_opponent_turn():
            file = 10 - file

        return file - 1


    def suji(self, suji):
        """［筋番号］
        
        先手の file に変換します。
        変域： 1 ～ 9。
        """
        return self.file(file=suji)     # 処理内容は file と同じ


    def rank(self, rank):
        """［ランク番号］
        
        先手の rank に変換します。
        変域： 1 ～ 9。
        """
        return self.file(file=rank)     # 処理内容は file と同じ


    def dan(self, dan):
        """［段番号］
        
        先手の rank に変換します。
        変域： 1 ～ 9。
        """
        return self.file(file=dan)      # 処理内容は file と同じ


    def suji_range(self, start, end):
        if self.is_opponent_turn():
            return range(9 - end, 9 - start)    # masu → sq 変換しながら、１８０°回転

        return range(start - 1, end - 1)


    def dan_range(self, start, end):
        return self.suji_range(start, end)      # 処理内容は同じ


    def top_of_sq(self, sq):
        """［上］
        """
        sq_obj = SquareModel(sq)

        # 対象外なケース：        
        if sq_obj.rank == self.dan(1):      # １段目だ。
            return None     # 盤外

        rel_sq = -1     # 上

        if self.is_opponent_turn():     # 相手番なら盤を１８０°反転
            rel_sq *= -1

        return sq + rel_sq


    def top_of_masu(self, masu):
        """［上］
        """
        return self.top_of_sq(sq=MasuModel(masu).to_sq())


    def top_right_of_sq(self, sq):
        """［右上］
        """

        sq_obj = SquareModel(sq)

        # 対象外なケース：
        if (
                sq_obj.rank == self.dan(1)      # １段目だ。
            or  sq_obj.file == self.suji(9)     # ９筋目だ。
        ):
            return None     # 盤外

        rel_sq = -10    # 右上

        if self.is_opponent_turn():     # 相手番なら盤を１８０°反転
            rel_sq *= -1

        return sq + rel_sq


    def top_right_of_masu(self, masu):
        """［右上］
        """
        return self.top_right_of_sq(sq=MasuModel(masu).to_sq())


    def top_left_of_sq(self, sq):
        """［左上］
        """

        sq_obj = SquareModel(sq)

        # 対象外なケース：
        if (
                sq_obj.rank == self.dan(1)      # １段目だ。
            or  sq_obj.file == self.suji(9)     # ９筋目だ。
        ):
            return None     # 盤外

        rel_sq = 8      # 左上

        if self.is_opponent_turn():     # 相手番なら盤を１８０°反転
            rel_sq *= -1

        return sq + rel_sq


    def top_left_of_masu(self, masu):
        """［左上］
        """
        return self.top_left_of_sq(sq=MasuModel(masu).to_sq())


    def bottom_left_of_sq(self, sq):
        """［左下］
        """

        sq_obj = SquareModel(sq)

        # 対象外なケース：
        if (
                sq_obj.rank == self.dan(9)     # ９段目だ。
            or  sq_obj.file == self.suji(9)    # ９筋目だ。
        ):
            return None     # 盤外

        rel_sq = 10     # 左下

        if self.is_opponent_turn():     # 相手番なら盤を１８０°反転
            rel_sq *= -1

        return sq + rel_sq


    def bottom_left_of_masu(self, masu):
        """［左下］
        """
        return self.bottom_left_of_sq(sq=MasuModel(masu).to_sq())


    def bottom_right_of_sq(self, sq):
        """［右下］
        """
        sq_obj = SquareModel(sq)

        # 対象外なケース：
        if (
                sq_obj.rank == self.dan(9)      # ９段目だ。
            or  sq_obj.file == self.suji(1)     # １筋目だ。
        ):
            return None     # 盤外

        rel_sq = -8     # 右下

        if self.is_opponent_turn():     # 相手番なら盤を１８０°反転
            rel_sq *= -1

        return sq + rel_sq


    def bottom_right_of_masu(self, masu):
        """［右下］
        """
        return self.bottom_right_of_sq(sq=MasuModel(masu).to_sq())


    ##############
    # MARK: 式関連
    ##############

    def swap(self, a, b):
        """［比較］
        """
        if self.is_opponent_turn():
            return b, a
        
        return a, b


    ##############
    # MARK: 駒関連
    ##############

    def ji_pc(self, piece_type):
        """［自］。手番を持っている側。駒種類を手番の駒へ変換
        """
        if self.is_opponent_turn():
            piece = piece_type + 16
        else:
            piece = piece_type

        return piece


    def aite_pc(self, piece_type):
        """［相手］。手番を持ってない側。駒種類を相手番の駒へ変換
        """
        if self.is_opponent_turn():
            piece = piece_type
        else:
            piece = piece_type + 16

        return piece


    ##################
    # MARK: 評価値関連
    ##################

    def value(self, value):
        """評価値"""
        if self.is_opponent_turn():
            return - value
        return value
