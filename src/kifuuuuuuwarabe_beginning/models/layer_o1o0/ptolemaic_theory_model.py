class PtolemaicTheoryModel():
    """［天動説］
    地球が中心。
    """


    def __init__(self, gymnasium):
        self._gymnasium = gymnasium


    ##############
    # MARK: 式関連
    ##############

    def swap(self, a, b):
        """［比較］
        """
        if self._gymnasium.is_mars:   # 対戦相手ならひっくり返す。
            return b, a
        
        return a, b
