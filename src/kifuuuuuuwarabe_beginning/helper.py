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
