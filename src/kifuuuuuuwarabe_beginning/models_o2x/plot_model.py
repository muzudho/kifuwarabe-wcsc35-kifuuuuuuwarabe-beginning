import cshogi

from ..models_o1x import constants, DeclarationModel, PieceTypeModel, PieceValuesModel


class PlotModel():
    """読み筋モデル。

    NOTE ［指す手］を Move、指さずにする［宣言］を Declaration と呼び分けるものとします。［指す手］と［宣言］を合わせて Play ［遊び］と呼ぶことにします。
    ［宣言］には、［投了］、［入玉宣言勝ち］の２つがあります。［宣言］をした後に［指す手］が続くことはありません。
    """


    def __init__(self, declaration, is_mate_in_1_move):
        """初期化。

        Parameters
        ----------
        declaration : int
            ［宣言］
        is_mate_in_1_move : bool
            ［末端局面で１手詰めか？］
        """
        self._declaration = declaration
        self._is_mate_in_1_move = is_mate_in_1_move
        self._move_list = []
        self._cap_list = []
        self._piece_exchange_value_list = []


    @property
    def declaration(self):
        """［宣言］
        """
        return self._declaration


    @property
    def is_mate_in_1_move(self):
        """［末端局面で１手詰めか？］
        """
        return self._is_mate_in_1_move


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
    def is_capture_at_last(self):
        return self._cap_list[-1] != cshogi.NONE


    @property
    def last_piece_exchange_value(self):
        return self._piece_exchange_value_list[-1]


    def append_move(self, is_opponent, move, capture_piece_type):

        if capture_piece_type is None:
            raise ValueError(f"capture_piece_type をナンにしてはいけません。cshogi.NONE を使ってください。 {capture_piece_type=}")

        self._move_list.append(move)
        self._cap_list.append(capture_piece_type)

        piece_exchange_value = 2 * PieceValuesModel.by_piece_type(pt=capture_piece_type)      # 交換値に変換。正の数とする。

        # 一手詰め時
        if len(self._move_list) == 1 and self._is_mate_in_1_move:
            piece_exchange_value += constants.value.CHECKMATE

        if is_opponent:
            piece_exchange_value *= -1
        
        # ひとつ前の値
        previous = 0
        if 0 < len(self._piece_exchange_value_list):
            previous = self._piece_exchange_value_list[-1]

        # 累計していく。
        self._piece_exchange_value_list.append(previous + piece_exchange_value)


    def stringify(self):


        def _cap(cap):
            if cap != cshogi.NONE:
                return f"x{PieceTypeModel.kanji(cap)}"
            return ''


        def _pev(pev):
            if pev == 0:
                return ''
            return f"({pev})"
        

        tokens = []
        for index in reversed(range(0, len(self._move_list))):
            move_as_usi = cshogi.move_to_usi(self._move_list[index])
            cap = self._cap_list[index]
            piece_exchange_value = self._piece_exchange_value_list[index]
            tokens.append(f"{move_as_usi}{_cap(cap)}{_pev(piece_exchange_value)}")

        if self._declaration != DeclarationModel.NONE:
            tokens.append(DeclarationModel.japanese(self.declaration))

        return ' '.join(tokens)


    def stringify_2(self):
        def _cap_str():
            if self.is_capture_at_last:
                return 'cap'
            return ''

        return f"{self.last_piece_exchange_value:4} {_cap_str():3}"
