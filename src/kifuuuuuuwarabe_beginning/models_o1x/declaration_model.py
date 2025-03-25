class DeclarationModel():
    """［宣言］。
    """


    @staticmethod
    def NONE():
        """宣言ではありません。
        """
        return 0


    @staticmethod
    def RESIGN():
        """投了。
        """
        return 1


    @staticmethod
    def NYUGYOKU_WIN():
        """入玉宣言局面時。
        """
        return 2
