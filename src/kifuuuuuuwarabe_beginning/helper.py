import cshogi


class Turned():
    """先後両用ヘルパー関数
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
    def masu_to_sq(masu):
        return Helper.suji_to_file(Helper.masu_to_suji(masu)) * 9 + Helper.dan_to_rank(Helper.masu_to_dan(masu))


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
    def sq_to_masu(sq):
        return Helper.sq_to_suji(sq) * 10 + Helper.sq_to_dan(sq)


    @staticmethod
    def sq_to_suji(sq):
        return sq // 9 + 1


    @staticmethod
    def sq_to_dan(sq):
        return sq % 9 + 1
