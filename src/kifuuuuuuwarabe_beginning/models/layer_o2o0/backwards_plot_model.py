import cshogi

from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import constants, DeclarationModel, PieceTypeModel


class CutoffReason():
    """カットオフした理由。
    """


    _label = [
        '',                 # [0]
        '詰み形',           # [1]
        '一手詰め',         # [2]
        '入玉宣言勝ち',     # [3]
        '応手無し',         # [4] 末端局面で合法手の中から指したい手無し
        '探索深さ最大',     # [5]
    ]


    @classmethod
    def japanese(clazz, number):
        return clazz._label[number]


    @property
    def GAME_OVER(self):
        """投了。詰み形。
        """
        return 1
    

    @property
    def MATE_MOVE_IN_1_PLY(self):
        """一手詰め。
        """
        return 2


    @property
    def NYUGYOKU_WIN(self):
        """入玉宣言勝ち。
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


class BackwardsPlotModel():
    """読み筋モデル。
    末端局面から開始局面に向かって後ろ向きに進み、格納します。（スタック構造）

    NOTE ［指す手］を Move、指さずにする［宣言］を Declaration と呼び分けるものとします。［指す手］と［宣言］を合わせて Play ［遊び］と呼ぶことにします。
    ［宣言］には、［投了］、［入玉宣言勝ち］の２つがあります。［宣言］をした後に［指す手］が続くことはありません。
    """


    @staticmethod
    def _declaration_to_value_on_earth(declaration, is_mars):
        if declaration == constants.declaration.RESIGN:
            previous = constants.value.GAME_OVER
        elif declaration == constants.declaration.NYUGYOKU_WIN:
            previous = constants.value.NYUGYOKU_WIN
        elif declaration == constants.declaration.MAX_DEPTH_BY_THINK:
            previous = constants.value.ZERO
        elif declaration == constants.declaration.NO_CANDIDATES:
            previous = constants.value.ZERO
        elif declaration == constants.declaration.NONE:    # 末端の手。
            previous = constants.value.ZERO
        else:
            raise ValueError(f"想定外の［宣言］。{declaration=}")

        # 対戦相手なら正負を逆転。
        if is_mars:
            previous *= -1

        return previous


    def __init__(self, is_mars_at_end_position, declaration, is_mate_in_1_move, cutoff_reason, hint):
        """初期化。

        Parameters
        ----------
        is_mars_at_end_position : bool
            末端局面で対戦相手か。
        declaration : int
            ［宣言］
        is_mate_in_1_move : bool
            ［末端局面で１手詰めか？］
        cutoff_reason : int
            カットオフの理由
        hint : str
            デバッグ用文字列
        """
        self._is_mars_at_end_position = is_mars_at_end_position
        self._declaration = declaration
        self._is_mate_in_1_move = is_mate_in_1_move
        self._mars_list = []
        self._move_list = []
        self._cap_list = []
        self._piece_exchange_value_list_on_earth = []
        self._cutoff_reason = cutoff_reason
        self._hint_list = [hint]


    @property
    def is_mars_at_end_position(self):
        """末端局面で対戦相手か。
        """
        return self._is_mars_at_end_position


    @property
    def is_mars_at_peek(self):
        if self._move_list % 2 == 0:
            return self._is_mars_at_end_position
        return not self._is_mars_at_end_position


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
    def mars_list(self):
        return self._mars_list


    @property
    def move_list(self):
        return self._move_list


    @property
    def cap_list(self):
        return self._cap_list


    @property
    def peek_move(self):
        if len(self._move_list) < 1:
            raise ValueError('指し手のリストが０件です。')
        return self._move_list[-1]


    @property
    def is_capture_at_last(self):
        if len(self._cap_list) < 1:
            raise ValueError('取った駒のリストが０件です。')
        return self._cap_list[-1] != cshogi.NONE


    @property
    def peek_piece_exchange_value_on_earth(self):   # TODO is_mars
        """
        """
        # if self.is_declaration():
        #     if self._declaration == constants.declaration.RESIGN:
        #         value = constants.value.GAME_OVER
        #         if self._is_mars_at_end_position:
        #             return -value
        #         return value

        #     if self._declaration == constants.declaration.NYUGYOKU_WIN:
        #         value = constants.value.NYUGYOKU_WIN
        #         if self._is_mars_at_end_position:
        #             return -value
        #         return value


        # TODO ［宣言］でも、疑似的な［交換値］を付けていいのでは？ _declaration_to_value_on_earth() を使う？
        if len(self._piece_exchange_value_list_on_earth) < 1:
            # ［指し手］が無ければ、［宣言］の点数を返します。［宣言］を行っていない場合は、点数を付けれません。
            return self._declaration_to_value_on_earth(
                    declaration = self._declaration,
                    is_mars     = self.is_mars_at_peek)
            # #return constants.value.ZERO     # TODO ［指したい手がない］というのを何点と見るか？
            # raise ValueError(f"取った駒の交換値のリストが０件です。 {self.stringify_debug_1()} {DeclarationModel.japanese(self._declaration)=} {self._is_mars_at_end_position=} {self._is_mate_in_1_move=} {self._cutoff_reason=} {CutoffReason.japanese(self._cutoff_reason)=}")
            # # previous_on_earth = BackwardsPlotModel._declaration_to_value_on_earth(
            # #         declaration             = self.declaration,
            # #         is_mars    = not is_mars) # １つ前の値だから手番は反転

        return self._piece_exchange_value_list_on_earth[-1]


    @property
    def cutoff_reason(self):
        return self._cutoff_reason


    @property
    def hint_list(self):
        return self._hint_list


    def is_declaration(self):
        return self._declaration != constants.declaration.NONE


    def move_list_length(self):
        return len(self._move_list)


    def is_empty_moves(self):
        # ASSERT
        len_mars_list = len(self._mars_list)
        len_move_list = len(self._move_list)
        len_cap_list = len(self._cap_list)
        len_pev_list = len(self._piece_exchange_value_list_on_earth)
        if not (len_mars_list == len_move_list and len_move_list == len_cap_list and len_cap_list == len_pev_list):
            raise ValueError(f"配列の長さの整合性が取れていません。 {len_move_list=} {len_cap_list=} {len_pev_list=}")
        
        return len(self._move_list) < 1


    def append_move(self, is_mars, move, capture_piece_type, hint):
        """
        Parameters
        ----------
        is_mars : bool
            対戦相手か。
        hint : str
            デバッグ用文字列。
        """

        if capture_piece_type is None:
            raise ValueError(f"capture_piece_type をナンにしてはいけません。cshogi.NONE を使ってください。 {capture_piece_type=}")
        
        # ひとつ前の値
        if len(self._piece_exchange_value_list_on_earth) == 0:
            previous_on_earth = BackwardsPlotModel._declaration_to_value_on_earth(
                    declaration             = self.declaration,
                    is_mars    = not is_mars) # １つ前の値だから手番は反転

        else:
            previous_on_earth = self._piece_exchange_value_list_on_earth[-1]

        ##########
        # １手追加
        ##########
        self._mars_list.append(is_mars)
        self._move_list.append(move)
        self._cap_list.append(capture_piece_type)
        self._hint_list.append(hint)

        piece_exchange_value_on_earth = 2 * PieceValuesModel.by_piece_type(pt=capture_piece_type)      # 交換値に変換。正の数とする。

        # 一手詰めなら、点は最大。
        if len(self._move_list) == 1 and self._is_mate_in_1_move:
            piece_exchange_value_on_earth += constants.value.CHECKMATE

        # 対戦相手なら正負を逆転。
        if is_mars:
            piece_exchange_value_on_earth *= -1

        # 累計していく。
        self._piece_exchange_value_list_on_earth.append(previous_on_earth + piece_exchange_value_on_earth)


    def stringify(self):
        """読み筋を１行で文字列化。
        """


        def _planet(is_mars):
            if is_mars:
                return '火'     # Mars
            return '地'         # Earth


        def _cap(cap):
            return f"x{PieceTypeModel.kanji(cap)}"
        

        tokens = []
        for layer in reversed(range(0, len(self._move_list))):  # 逆順。
            move = self._move_list[layer]

            if not isinstance(move, int):   # FIXME バグがあるよう
                raise ValueError(f"move は int 型である必要があります。 {layer=} {type(move)=} {move=} {self._move_list=}")

            move_as_usi                     = cshogi.move_to_usi(move)
            is_mars            = self._mars_list[layer]
            cap                             = self._cap_list[layer]
            piece_exchange_value_on_earth   = self._piece_exchange_value_list_on_earth[layer]
            tokens.append(f"{layer+1}.{_planet(is_mars)}{move_as_usi}{_cap(cap)}({piece_exchange_value_on_earth})")

        if self._declaration != constants.declaration.NONE:
            tokens.append(DeclarationModel.japanese(self.declaration))

        # カットオフ理由
        tokens.append(CutoffReason.japanese(self._cutoff_reason))

        # ヒント・リスト
        tokens.append(' '.join(self._hint_list))

        return ' '.join(tokens)


    def stringify_2(self):
        def _cap_str():
            if self.is_capture_at_last:
                return 'cap'
            return ''

        return f"{self.peek_piece_exchange_value_on_earth:4} {_cap_str():3}"


    def stringify_dump(self):
        return f"{self._is_mars_at_end_position=} {self._declaration=} {self._is_mate_in_1_move=} {self._move_list=} {self._cap_list=} {self._piece_exchange_value_list_on_earth=} {self._cutoff_reason=} {' '.join(self._hint_list)=}"


    def stringify_debug_1(self):
        return f"{len(self._move_list)=} {len(self._cap_list)=} {len(self._piece_exchange_value_list_on_earth)=}"