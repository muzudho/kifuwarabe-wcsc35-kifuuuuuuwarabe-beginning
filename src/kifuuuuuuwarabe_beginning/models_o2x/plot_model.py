import cshogi

from ..models_o1x import constants, PieceTypeModel, PieceValuesModel


class PlotModel():
    """読み筋モデル。

    NOTE ［指す手］を Move、指さずにする［宣言］を Declaration と呼び分けるものとします。［指す手］と［宣言］を合わせて Play ［遊び］と呼ぶことにします。
    ［宣言］には、［投了］、［入玉宣言勝ち］の２つがあります。［宣言］をした後に［指す手］が続くことはありません。
    """


    def __init__(self, declaration):
        """初期化。

        Parameters
        ----------
        declaration : DeclarationModel
            ［宣言］
        """
        self._declaration = declaration
        self._move_list = []
        self._cap_list = []
        self._last_piece_exchange_value = constants.value.ZERO


    @property
    def declaration(self):
        """［宣言］
        """
        return self._declaration


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


    def append_move(self, move, piece_type):
        self._move_list.append(move)

        piece_exchange_value = 2 * PieceValuesModel.by_piece_type(pt=piece_type)      # 交換値に変換。
        self._cap_list.append(piece_type)
        self._last_piece_exchange_value = piece_exchange_value - self._last_piece_exchange_value


    def stringify(self):
        tokens = []
        for cap in reversed(self._cap_list):
            tokens.append(PieceTypeModel.kanji(cap))

        return ' '.join(tokens)


    def stringify_2(self):
        def _cap_str():
            if self.is_capture_at_last:
                return 'cap'
            return ''

        return f"{self.last_piece_exchange_value:4} {_cap_str():3}"
