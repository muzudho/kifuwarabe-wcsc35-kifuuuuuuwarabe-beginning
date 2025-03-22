import cshogi


class MoveOnScramble():
    """駒を取る手、駒を取らない手のSEE探索で使います。
    """


    @staticmethod
    def legal_moves_to_list(legal_moves):
        move_ex_list = []
        for move in list(legal_moves):
            move_ex_list.append(MoveOnScramble(
                    move        = move,
                    piece_value = 0))
        return move_ex_list


    def __init__(self, move:int, piece_value:int, is_capture:bool):
        self._move          = move
        self._piece_value   = piece_value
        self._is_capture    = is_capture
    

    @property
    def move(self):
        return self._move
    

    @property
    def piece_value(self):
        return self._piece_value
    

    @property
    def is_capture(self):
        return self._is_capture


    def stringify(self):
        def _cap_str():
            if self._is_capture:
                return 'cap'
            return ''

        return f"{cshogi.move_to_usi(self._move)} {self._piece_value} {_cap_str()}"
