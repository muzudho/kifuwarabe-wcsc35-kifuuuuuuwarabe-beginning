class Masu():
    """［マス］

    Square のラッパーです。
    """


    def __init__(self, masu):
        self._masu = masu


    def to_masu(self):
        return self._masu


    def to_sq(self):
        return (self.to_suji() - 1) * 9 + (self.to_dan() - 1)


    def to_suji(self):
        return self._masu // 10


    def to_dan(self):
        return self._masu % 10
