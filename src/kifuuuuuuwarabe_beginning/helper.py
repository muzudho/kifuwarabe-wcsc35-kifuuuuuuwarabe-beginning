class Helper():
    
    
    @staticmethod
    def sq_to_masu(sq):
        file = sq // 9 + 1
        rank = sq % 9 + 1
        return file * 10 + rank
