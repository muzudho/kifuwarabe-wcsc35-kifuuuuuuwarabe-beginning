import cshogi


class MoveOnScrambleModel():
    """駒を取る手、駒を取らない手のSEE探索で使います。
    """


    @staticmethod
    def legal_moves_to_list(legal_moves):
        move_ex_list = []
        for move in list(legal_moves):
            move_ex_list.append(MoveOnScrambleModel(
                    move        = move,
                    piece_exchange_value = 0))
        return move_ex_list


    def __init__(self, move:int, piece_exchange_value:int, is_capture:bool):
        self._move                  = move
        self._piece_exchange_value  = piece_exchange_value  # FIXME 交換値だけではなく、その内訳も知りたい。取った駒リスト。
        self._is_capture            = is_capture
    

    @property
    def move(self):
        return self._move
    

    @property
    def piece_exchange_value(self):
        """駒の交換値。
        """
        return self._piece_exchange_value
    

    @property
    def is_capture(self):
        return self._is_capture


    def stringify(self):
        return f"{cshogi.move_to_usi(self._move):5} {self.stringify_2()}"


    def stringify_2(self):
        def _cap_str():
            if self._is_capture:
                return 'cap'
            return ''

        return f"{self._piece_exchange_value:4} {_cap_str():3}"
