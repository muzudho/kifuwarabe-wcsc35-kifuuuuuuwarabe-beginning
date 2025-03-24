class SquareModel():


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
