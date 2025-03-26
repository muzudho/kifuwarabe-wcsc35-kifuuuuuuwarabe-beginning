import cshogi

from ..models_o1x import constants, DeclarationModel, PieceTypeModel, PieceValuesModel


class CutoffReason():
    """カットオフした理由。
    """


    _label = [
        '',                                 # [0]
        '詰み形',                           # [1]
        '入玉宣言勝ち',                     # [2]
        '一手詰め',                         # [3]
        '合法手の中から指したい手無し',     # [4]
        '探索深さ最大',                     # [5]
    ]


    @classmethod
    def label(clazz, number):
        return clazz._label[number]


    @property
    def GAME_OVER(self):
        """投了。詰み形。
        """
        return 1


    @property
    def NYUGYOKU_WIN(self):
        """入玉宣言勝ち。
        """
        return 2
    

    @property
    def MATE_MOVE_IN_1_PLY(self):
        """一手詰め。
        """
        return 3


    @property
    def NO_MOVES(self):
        """（合法手の中から）指したい手無し。
        """
        return 4


    @property
    def MAX_DEPTH(self):
        """探索深さ最大。
        """
        return 5


cutoff_reason = CutoffReason()


class PlotModel():
    """読み筋モデル。

    NOTE ［指す手］を Move、指さずにする［宣言］を Declaration と呼び分けるものとします。［指す手］と［宣言］を合わせて Play ［遊び］と呼ぶことにします。
    ［宣言］には、［投了］、［入玉宣言勝ち］の２つがあります。［宣言］をした後に［指す手］が続くことはありません。
    """


    def __init__(self, declaration, is_mate_in_1_move, cutoff_reason):
        """初期化。

        Parameters
        ----------
        declaration : int
            ［宣言］
        is_mate_in_1_move : bool
            ［末端局面で１手詰めか？］
        cutoff_reason : int
            カットオフの理由
        """
        self._declaration = declaration
        self._is_mate_in_1_move = is_mate_in_1_move
        self._move_list = []
        self._cap_list = []
        self._piece_exchange_value_list = []
        self._cutoff_reason = cutoff_reason


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
        if len(self._move_list) < 1:
            return 0    # FIXME 投了
        return self._move_list[-1]


    @property
    def is_capture_at_last(self):
        if len(self._cap_list) < 1:
            return False    # FIXME 本当は None だが。
        return self._cap_list[-1] != cshogi.NONE


    @property
    def last_piece_exchange_value(self):
        if len(self._piece_exchange_value_list) < 1:
            return 0
        return self._piece_exchange_value_list[-1]


    @property
    def cutoff_reason(self):
        return self._cutoff_reason


    def append_move(self, is_absolute_opponent, move, capture_piece_type):
        """
        Parameters
        ----------
        is_absolute_opponent : bool
            対戦相手か。
        """

        if capture_piece_type is None:
            raise ValueError(f"capture_piece_type をナンにしてはいけません。cshogi.NONE を使ってください。 {capture_piece_type=}")

        self._move_list.append(move)
        self._cap_list.append(capture_piece_type)

        piece_exchange_value = 2 * PieceValuesModel.by_piece_type(pt=capture_piece_type)      # 交換値に変換。正の数とする。

        # 一手詰め時
        if len(self._move_list) == 1 and self._is_mate_in_1_move:
            piece_exchange_value += constants.value.CHECKMATE

        if is_absolute_opponent:
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
            move = self._move_list[index]

            if not isinstance(move, int):   # FIXME バグがあるよう
                raise ValueError(f"move は int 型である必要があります。 {index=} {type(move)=} {move=} {self._move_list=}")

            move_as_usi = cshogi.move_to_usi(move)
            cap = self._cap_list[index]
            piece_exchange_value = self._piece_exchange_value_list[index]
            tokens.append(f"{move_as_usi}{_cap(cap)}{_pev(piece_exchange_value)}")

        if self._declaration != DeclarationModel.NONE:
            tokens.append(DeclarationModel.japanese(self.declaration))

        # カットオフ理由
        tokens.append(CutoffReason.label(self._cutoff_reason))

        return ' '.join(tokens)


    def stringify_2(self):
        def _cap_str():
            if self.is_capture_at_last:
                return 'cap'
            return ''

        return f"{self.last_piece_exchange_value:4} {_cap_str():3}"
