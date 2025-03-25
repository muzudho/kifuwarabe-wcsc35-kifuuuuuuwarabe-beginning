import cshogi

from ..models_o1x import constants, PieceValuesModel


class PlotModel():
    """読み筋モデル。
    """


    def __init__(self):
        """初期化。
        """
        self._search_result_state_model_list = []
        self._move_list = []
        self._cap_list = []
        self._last_piece_exchange_value = constants.value.ZERO


    @property
    def search_result_state_model_list(self):
        return self._search_result_state_model_list


    @property
    def move_list(self):
        return self._move_list


    @property
    def cap_list(self):
        return self._cap_list


    @property
    def last_move(self):
        return self._move_list[-1]


    @property
    def last_piece_exchange_value(self):
        return self._last_piece_exchange_value


    @property
    def is_capture_at_last(self):
        return self._cap_list[-1] != cshogi.NONE


    def append_capture(self, search_result_state_model, move, piece_type):
        self._search_result_state_model_list.append(search_result_state_model)
        self._move_list.append(move)

        piece_exchange_value = 2 * PieceValuesModel.by_piece_type(pt=piece_type)      # 交換値に変換。
        self._cap_list.append(piece_type)
        self._last_piece_exchange_value = piece_exchange_value - self._last_piece_exchange_value


    def stringify_2(self):
        def _cap_str():
            if self.is_capture_at_last:
                return 'cap'
            return ''

        return f"{self.last_piece_exchange_value:4} {_cap_str():3}"
