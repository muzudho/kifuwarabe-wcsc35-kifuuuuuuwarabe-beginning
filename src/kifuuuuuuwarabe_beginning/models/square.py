class Square():


    def __init__(self, sq):
        self._sq = sq


    def sq(self):
        return self._sq


    def to_file(self):
        return self._sq // 9


    def to_rank(self):
        return self._sq % 9
