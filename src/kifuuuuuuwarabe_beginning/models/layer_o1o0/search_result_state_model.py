class SearchResultStateModel():


    @staticmethod
    def NONE():
        """特に何もなし。
        """
        return 0


    @staticmethod
    def GAME_OVER():
        """投了局面。
        """
        return 1


    @staticmethod
    def NYUGYOKU_WIN():
        """入玉宣言勝ち局面時。
        """
        return 2


    def MATE_IN_1_MOVE():
        """１手詰め時。
        """
        return 3


    def BEST_MOVE():
        """通常時の次の１手。
        """
        return 4
