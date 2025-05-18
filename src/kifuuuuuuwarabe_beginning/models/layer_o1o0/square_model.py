class SquareModel():


    @staticmethod
    def from_masu(masu):
        suji = masu // 10
        dan = masu % 10
        return SquareModel(sq=(suji-1) * 9 + (dan - 1))


    def __init__(self, sq):
        self._sq = sq


    @property
    def sq(self):
        return self._sq


    @property
    def file(self):
        return self._sq // 9


    @property
    def rank(self):
        return self._sq % 9


    def to_north_or_none(self):
        """北。
        """
        if self.rank == 0:
            return None
        return SquareModel(sq=self._sq - 1)


    def to_south_or_none(self):
        """南。
        """
        if self.rank == 8:
            return None
        return SquareModel(sq=self._sq + 1)