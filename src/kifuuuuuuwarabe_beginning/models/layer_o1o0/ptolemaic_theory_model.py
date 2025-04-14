class PtolemaicTheoryModel():
    """［天動説］
    地球が中心。
    """


    def __init__(self, is_mars):
        self._is_mars = is_mars


    @property
    def is_mars(self):
        return self._is_mars


    @property
    def is_earth(self):
        return not self._is_mars


    ##############
    # MARK: 式関連
    ##############

    def swap(self, a, b):
        """［比較］
        """
        if self.is_mars:   # 対戦相手ならひっくり返す。
            return b, a
        
        return a, b
