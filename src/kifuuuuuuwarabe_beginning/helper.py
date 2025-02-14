class Helper():
    """ヘルパー関数集
    """
    

    @staticmethod
    def sq_to_masu(sq):
        return Helper.sq_to_suji(sq) * 10 + Helper.sq_to_dan(sq)

    @staticmethod
    def sq_to_suji(sq):
        return sq // 9 + 1

    @staticmethod
    def sq_to_dan(sq):
        return sq % 9 + 1
