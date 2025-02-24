class BoardWrapper():
    """cshogi の Board に付いていない機能を付加するラッパー
    """


    def __init__(self, board):
        self._board = board


    @property
    def raw_b(self):
        return self._board


    #########
    # MARK: I
    #########

    def is_check(self):
        return self._board.is_check()


    def is_game_over(self):
        return self._board.is_game_over()


    def is_nyugyoku(self):
        return self._board.is_nyugyoku()


    #########
    # MARK: L
    #########

    @property
    def legal_moves(self):
        return self._board.legal_moves


    #########
    # MARK: M
    #########

    def mate_move_in_1ply(self):
        return self._board.mate_move_in_1ply()


    #########
    # MARK: P
    #########

    def piece(self, sq):
        return self._board.piece(sq)


    def pop(self, usi):
        return self._board.pop(usi)


    def push_usi(self, usi):
        return self._board.push_usi(usi)


    #########
    # MARK: R
    #########

    def reset(self):
        return self._board.reset()


    #########
    # MARK: S
    #########

    def set_sfen(self, sfen):
        self._board.set_sfen(sfen)
