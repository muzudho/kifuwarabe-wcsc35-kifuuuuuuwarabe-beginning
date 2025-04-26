import cshogi

from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0o_9o0_table_helper import TableHelper
from ..layer_o1o0 import constants, OutOfTerminationModel, Mars, PieceTypeModel, PlanetPieceTypeModel, SquareModel
from ..layer_o1o0o1o0_japanese import JapaneseMoveModel


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
        '静止',             # [6] 駒の取り合いが無くなった。
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


    @property
    def QUIESCENCE(self):
        """静止。駒の取り合いがなくなった。
        """
        return 6


cutoff_reason = CutoffReason()


class BackwardsPlotModel(): # TODO Rename PathFromLeaf
    """読み筋モデル。
    末端局面から開始局面に向かって後ろ向きに進み、格納します。（スタック構造）

    NOTE ［指す手］を Move、指さずにする［終端外］を OutOfTermination と呼び分けるものとします。［指す手］と［終端外］を合わせて Play ［遊び］と呼ぶことにします。
    ［終端外］には、［投了］、［入玉宣言勝ち］の２つがあります。［終端外］をした後に［指す手］が続くことはありません。
    """


    @staticmethod
    def _out_of_termination_to_value_on_earth(out_of_termination, is_mars):
        if out_of_termination == constants.out_of_termination.RESIGN:
            previous = constants.value.GAME_OVER
        elif out_of_termination == constants.out_of_termination.NYUGYOKU_WIN:
            previous = constants.value.NYUGYOKU_WIN
        elif out_of_termination == constants.out_of_termination.MAX_DEPTH_BY_THINK:
            previous = constants.value.ZERO
        elif out_of_termination == constants.out_of_termination.NO_CANDIDATES:
            previous = constants.value.ZERO
        elif out_of_termination == constants.out_of_termination.QUIESCENCE:
            previous = constants.value.ZERO
        else:
            raise ValueError(f"想定外の［終端外］。{out_of_termination=}")

        # 対戦相手なら正負を逆転。
        if is_mars:
            previous *= -1

        return previous


    def __init__(self, is_mars_at_out_of_termination, is_gote_at_out_of_termination, out_of_termination, cutoff_reason, hint):
        """初期化。

        Parameters
        ----------
        is_mars_at_out_of_termination : bool
            ［葉局面］＝［終端外］手番は対戦相手か。
        is_gote_at_out_of_termination : bool
            ［葉局面］＝［終端外］手番は後手か。
        out_of_termination : int
            ［終端外］
        cutoff_reason : int
            カットオフの理由
        hint : str
            デバッグ用文字列
        """
        self._is_mars_at_out_of_termination = is_mars_at_out_of_termination
        self._is_gote_at_out_of_termination = is_gote_at_out_of_termination
        self._out_of_termination = out_of_termination
        self._move_list = []
        self._cap_list = []
        self._list_of_accumulate_exchange_value_on_earth = []   # 地球から見た、取った駒の交換値。
        self._cutoff_reason = cutoff_reason
        self._hint_list = [hint]


    @property
    def is_mars_at_out_of_termination(self):
        """木構造の葉ノードの次で対戦相手か。
        """
        return self._is_mars_at_out_of_termination


    @property
    def is_gote_at_out_of_termination(self):
        """木構造の葉ノードの次で後手か。
        """
        return self._is_gote_at_out_of_termination


    @property
    def is_mars_at_peek(self):
        if len(self._move_list) % 2 == 0:
            return self._is_mars_at_out_of_termination
        return not self._is_mars_at_out_of_termination


    @property
    def is_gote_at_peek(self):
        if len(self._move_list) % 2 == 0:
            return self._is_gote_at_out_of_termination
        return not self._is_gote_at_out_of_termination


    @property
    def out_of_termination(self):
        """［終端外］
        """
        return self._out_of_termination


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


    def get_exchange_value_on_earth(self):
        """駒得の交換値。
        """


        if len(self._list_of_accumulate_exchange_value_on_earth) == 0:
            return self._out_of_termination_to_value_on_earth(   # ［終端外］の点数。
                    out_of_termination = self._out_of_termination,
                    is_mars     = self._is_mars_at_out_of_termination)

        return self._list_of_accumulate_exchange_value_on_earth[-1]


    @property
    def cutoff_reason(self):
        return self._cutoff_reason


    @property
    def hint_list(self):
        return self._hint_list


    def move_list_length(self):
        return len(self._move_list)


    def is_empty_moves(self):
        # ASSERT
        len_move_list = len(self._move_list)
        len_cap_list = len(self._cap_list)
        len_ev_list = len(self._list_of_accumulate_exchange_value_on_earth)
        if not (len_move_list == len_cap_list and len_cap_list == len_ev_list):
            raise ValueError(f"配列の長さの整合性が取れていません。 {len_move_list=} {len_cap_list=} {len_ev_list=}")
        
        return len(self._move_list) < 1


    def append_move(self, move, capture_piece_type, hint):
        """
        Parameters
        ----------
        capture_piece_type : int
            取った駒の種類。
        hint : str
            デバッグ用文字列。
        """

        ##########
        # １手追加
        ##########
        self._move_list.append(move)
        self._cap_list.append(capture_piece_type)
        self._hint_list.append(hint)

        ############
        # １手追加後
        ############

        if capture_piece_type is None:
            raise ValueError(f"capture_piece_type をナンにしてはいけません。cshogi.NONE を使ってください。 {capture_piece_type=}")

        if len(self._list_of_accumulate_exchange_value_on_earth) == 0:
            accumulate_value_on_earth = self._out_of_termination_to_value_on_earth(   # ［終端外］の点数。
                    out_of_termination = self._out_of_termination,
                    is_mars     = self._is_mars_at_out_of_termination)
        else:
            accumulate_value_on_earth = self._list_of_accumulate_exchange_value_on_earth[-1]

        piece_exchange_value_on_earth = 2 * PieceValuesModel.by_piece_type(pt=capture_piece_type)      # 交換値に変換。正の数とする。
        if self.is_mars_at_peek:                    # 火星なら。
            piece_exchange_value_on_earth *= -1     # 正負の符号を反転する。

        # かつ、火星の［終端外］で終わるとき　＝　地球の［指し手］で読み終わるとき
        if (
                self._out_of_termination == constants.out_of_termination.MAX_DEPTH_BY_THINK   # ［終端外］が［読みの深さの最大］。
            and len(self._list_of_accumulate_exchange_value_on_earth) == 1      # ［読みの深さの最大］のときの末端の指し手のとき。
            and not self.is_mars_at_peek                                        # ［地球］の手番。
            ):
            piece_exchange_value_on_earth = 0   # 駒得点をノーカウントにする。（［地球の手］を１回多くカウントするのは数えすぎだから）

        # ＜📚原則１＞地球と火星のペアが完成したら、駒得点を逓減。
        # （完全に読み切るわけではないので）深くの手ほど価値を減らします。ただしあまり深くの駒を弱く調整すると、浅い銀と深い角が同じ価値になるなど不具合が生じます。
        piece_exchange_value_on_earth = (piece_exchange_value_on_earth + accumulate_value_on_earth)     # * 3 / 4     # * 9 / 10

        # 累計します。
        self._list_of_accumulate_exchange_value_on_earth.append(piece_exchange_value_on_earth)


    def stringify(self):
        """読み筋を１行で文字列化。
        """
        tokens = []
        is_mars = self.is_mars_at_peek   # 逆順なので、ピークから。
        is_gote = self.is_gote_at_peek   # 逆順なので、ピークから。

        len_of_move_list = len(self._move_list)
        for layer_no in reversed(range(0, len_of_move_list)):  # 逆順。
            move        = self._move_list[layer_no]
            moving_pt   = TableHelper.get_moving_pt_from_move(move=move)  # 動かした駒の種類。盤上の移動元の駒か、打った駒。
            cap_pt      = self._cap_list[layer_no]

            if not isinstance(move, int):   # FIXME バグがあるよう
                raise ValueError(f"move は int 型である必要があります。 {layer_no=} {type(move)=} {move=} {self._move_list=}")

            # 指し手のUSI表記を独自形式に変更。
            move_str = JapaneseMoveModel.from_move(move=move, moving_pt=moving_pt, cap_pt=cap_pt, is_mars=is_mars, is_gote=is_gote).stringify()

            piece_exchange_value_on_earth   = self._list_of_accumulate_exchange_value_on_earth[layer_no]
            tokens.append(f"({len_of_move_list - layer_no}){move_str}[{piece_exchange_value_on_earth}]")

            # 手番交代
            is_mars = not is_mars
            is_gote = not is_gote

        tokens.append(f"{Mars.japanese(is_mars)}の{OutOfTerminationModel.japanese(self.out_of_termination)}")   # ［終端外］

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

        return f"{self.get_exchange_value_on_earth():4} {_cap_str():3}"


    def stringify_dump(self):
        return f"{self._is_mars_at_out_of_termination=} {self._out_of_termination=} {self._move_list=} {self._cap_list=} {self._list_of_accumulate_exchange_value_on_earth=} {self._cutoff_reason=} {' '.join(self._hint_list)=}"


    def stringify_debug_1(self):
        return f"{len(self._move_list)=} {len(self._cap_list)=} {len(self._list_of_accumulate_exchange_value_on_earth)=}"
