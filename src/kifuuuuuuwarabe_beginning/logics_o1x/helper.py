

class Helper():
    """ヘルパー関数集
    """

    # D

    @staticmethod
    def dan_to_rank(dan):
        return dan - 1


    # F

    @staticmethod
    def file_rank_to_masu(file, rank):
        return (file + 1) * 10 + (rank + 1)

    @staticmethod
    def file_rank_to_sq(file, rank):
        return file * 9 + rank


    # M

    @staticmethod
    def masu_to_suji(masu):
        return masu // 10

    @staticmethod
    def masu_to_dan(masu):
        return masu % 10

    @staticmethod
    def masu_to_file(masu):
        return masu // 10 - 1


    @staticmethod
    def masu_to_rank(masu):
        return masu % 10 - 1


    # S

    @staticmethod
    def suji_to_file(suji):
        return suji - 1


    @staticmethod
    def suji_dan_to_masu(suji, dan):
        return suji * 10 + dan

    @staticmethod
    def sq_to_masu(sq):
        return Helper.sq_to_suji(sq) * 10 + Helper.sq_to_dan(sq)


    @staticmethod
    def sq_to_suji(sq):
        return sq // 9 + 1


    @staticmethod
    def sq_to_dan(sq):
        return sq % 9 + 1


    @staticmethod
    def sq_to_file(sq):
        return sq // 9


    @staticmethod
    def sq_to_rank(sq):
        return sq % 9


    # T

    @staticmethod
    def turn_name(turn):
        if turn == 0:
            return 'Black'
        elif turn == 1:
            return 'White'
        else:
            raise ValueError(f'{turn=}')
