class SFEN():
    """
    例： `lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1`

    NOTE 同形反復をチェックするときは、盤面、手番、持ち駒を見ればいい。何手目かは不要。
    """


    @staticmethod
    def parse(sfen):
        """sfen をパースする。速いレスポンスが欲しいので、文字列を空白で分割するだけ。
        """
        tokens = sfen.split()

        return SFEN(
                board_str=tokens[0],
                turn_str=tokens[1],
                hand_str=tokens[2],
                number_of_moves=int(tokens[3]))


    def __init__(self, board_str, turn_str, hand_str, number_of_moves):
        self._board_str = board_str
        self._turn_str = turn_str
        self._hand_str = hand_str
        self._number_of_moves = number_of_moves


    @property
    def board_str(self):
        """
        例： `lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1`
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        """
        return self._board_str


    @property
    def turn_str(self):
        """
        例： `lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1`
                                                                        ^
        """
        return self._turn_str


    @property
    def hand_str(self):
        """
        例： `lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1`
                                                                          ^
        """
        return self._hand_str


    @property
    def number_of_moves(self):
        """
        例： `lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1`
                                                                            ^

        Returns
        -------
        number_of_moves : int
            何手目か
        """
        return self._number_of_moves


    def check_repetition(self, sfen_obj):
        """TODO 同形反復かチェックする
        """

        # 盤面、手番、持ち駒が等しければ同形反復
        return self._board_str == sfen_obj.board_str and self._turn_str == sfen_obj.turn_str and self._hand_str == sfen_obj.hand_str
