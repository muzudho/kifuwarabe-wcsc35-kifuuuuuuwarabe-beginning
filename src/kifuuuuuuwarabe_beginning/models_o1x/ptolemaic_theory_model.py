class PtolemaicTheoryModel():
    """［天動説］
    地球が中心。
    """


    def __init__(self, is_absolute_opponent):
        self._is_absolute_opponent = is_absolute_opponent


    @property
    def is_absolute_opponent(self):
        return self._is_absolute_opponent


    @property
    def is_earth(self):
        return not self._is_absolute_opponent


    ##############
    # MARK: 式関連
    ##############

    def swap(self, a, b):
        """［比較］
        """
        if self.is_absolute_opponent:   # 対戦相手ならひっくり返す。
            return b, a
        
        return a, b
