# import cshogi

# from ..layer_o1o0 import constants, OutOfTerminationStateModel, Mars
# from ..layer_o1o0o1o0_japanese import JapaneseMoveModel


# class BackwardsPlotModel(): # TODO Rename PathFromLeaf
#     """読み筋モデル。
#     末端局面から開始局面に向かって後ろ向きに進み、格納します。（スタック構造）

#     TODO 廃止方針。PV に統合したい。

#     NOTE ［指す手］を Move、指さずにする［終端外］を OutOfTermination と呼び分けるものとします。［指す手］と［終端外］を合わせて Play ［遊び］と呼ぶことにします。
#     ［終端外］には、［投了］、［入玉宣言勝ち］の２つがあります。［終端外］をした後に［指す手］が続くことはありません。
#     """


#     def __init__(self):
#         """初期化。
#         """
#         pass


#     # def is_mars_at_peek(self, out_of_termination_is_mars_arg):
#     #     if len(self._move_list) % 2 == 0:
#     #         return out_of_termination_is_mars_arg
#     #     return not out_of_termination_is_mars_arg


#     # @property
#     # def is_gote_at_peek(self, out_of_termination_is_gote_arg):
#     #     if len(self._move_list) % 2 == 0:
#     #         return out_of_termination_is_gote_arg
#     #     return not out_of_termination_is_gote_arg


#     # def move_list_length(self):
#     #     return len(self._move_list)


#     # def is_empty_moves(self):
#     #     # ASSERT
#     #     len_move_list = len(self._move_list)
#     #     len_cap_list = len(self._cap_list)
#     #     if not (len_move_list == len_cap_list):
#     #         raise ValueError(f"配列の長さの整合性が取れていません。 {len_move_list=} {len_cap_list=}")
        
#     #     return len(self._move_list) < 1


#     # def append_move_from_back(self, move, capture_piece_type, best_value, list_of_accumulate_exchange_value_on_earth_arg):
#     #     """
#     #     Parameters
#     #     ----------
#     #     move : int
#     #         シーショーギの指し手。
#     #     capture_piece_type : int
#     #         取った駒の種類。
#     #     best_value : int
#     #         ベスト点。
#     #     """

#     #     ##########
#     #     # １手追加
#     #     ##########
#     #     self._move_list.append(move)
#     #     self._cap_list.append(capture_piece_type)

#     #     ############
#     #     # １手追加後
#     #     ############

#     #     if capture_piece_type is None:
#     #         raise ValueError(f"capture_piece_type をナンにしてはいけません。cshogi.NONE を使ってください。 {capture_piece_type=}")

#     #     # if len(self._list_of_accumulate_exchange_value_on_earth) == 0:
#     #     #     accumulate_value_on_earth = self._get_out_of_termination_to_value_on_earth(   # ［終端外］の点数。
#     #     #             out_of_termination_state  = self._out_of_termination_state,
#     #     #             is_mars             = self._is_mars_at_out_of_termination)
#     #     # else:
#     #     #     accumulate_value_on_earth = self._list_of_accumulate_exchange_value_on_earth[-1]

#     #     # piece_exchange_value_on_earth = 2 * PieceValuesModel.by_piece_type(pt=capture_piece_type)      # 交換値に変換。正の数とする。
#     #     # if self.is_mars_at_peek:                    # 火星なら。
#     #     #     piece_exchange_value_on_earth *= -1     # 正負の符号を反転する。

#     #     # # ＜📚原則１＞地球と火星のペアが完成したら、駒得点を逓減。
#     #     # # # かつ、火星の［終端外］で終わるとき　＝　地球の［指し手］で読み終わるとき
#     #     # # if (
#     #     # #         self._out_of_termination_state == constants.out_of_termination_state.HORIZON     # ［終端外］が［読みの深さの最大］。
#     #     # #     and len(self._list_of_accumulate_exchange_value_on_earth) == 1                      # ［読みの深さの最大］のときの末端の指し手のとき。
#     #     # #     and not self.is_mars_at_peek                                                        # ［地球］の手番。
#     #     # #     ):
#     #     # #     piece_exchange_value_on_earth = 0   # 駒得点をノーカウントにする。（［地球の手］を１回多くカウントするのは数えすぎだから）

#     #     # # （完全に読み切るわけではないので）深くの手ほど価値を減らします。ただしあまり深くの駒を弱く調整すると、浅い銀と深い角が同じ価値になるなど不具合が生じます。
#     #     # # 累計します。
#     #     # piece_exchange_value_on_earth = (piece_exchange_value_on_earth + accumulate_value_on_earth)     # * 3 / 4     # * 9 / 10

#     #     # self._list_of_accumulate_exchange_value_on_earth.append(piece_exchange_value_on_earth)

#     #     list_of_accumulate_exchange_value_on_earth_arg.append(best_value)


#     # def stringify_bpm(self, out_of_termination_is_mars_arg, out_of_termination_state_arg):
#     #     """読み筋を１行で文字列化。
#     #     """
#     #     tokens = []
#     #     is_mars = self.is_mars_at_peek(out_of_termination_is_mars=out_of_termination_is_mars_arg)   # 逆順なので、ピークから。
#     #     is_gote = self.is_gote_at_peek   # 逆順なので、ピークから。

#     #     len_of_move_list = len(self._move_list)
#     #     for layer_no in reversed(range(0, len_of_move_list)):  # 逆順。
#     #         piece_exchange_value_on_earth   = self._list_of_accumulate_exchange_value_on_earth[layer_no]

#     #         # １手目は読み筋から省く。（別項目として表示されるから）
#     #         if layer_no == len_of_move_list - 1:
#     #             tokens.append(f"({len_of_move_list - layer_no})[{piece_exchange_value_on_earth}]")

#     #         else:
#     #             move        = self._move_list[layer_no]
#     #             cap_pt      = self._cap_list[layer_no]

#     #             if not isinstance(move, int):   # FIXME バグがあるよう
#     #                 raise ValueError(f"move は int 型である必要があります。 {layer_no=} {type(move)=} {move=} {self._move_list=}")

#     #             # 指し手のUSI表記を独自形式に変更。
#     #             move_jp_str = JapaneseMoveModel.from_move(
#     #                     move    = move,
#     #                     cap_pt  = cap_pt,
#     #                     is_mars = is_mars,
#     #                     is_gote = is_gote).stringify()

#     #             tokens.append(f"({len_of_move_list - layer_no}){move_jp_str}[{piece_exchange_value_on_earth}]")

#     #         # 手番交代
#     #         is_mars = not is_mars
#     #         is_gote = not is_gote

#     #     tokens.append(f"(終端外){Mars.japanese(is_mars)}の{OutOfTerminationStateModel.japanese(self.out_of_termination_state_arg)}")   # ［終端外］

#     #     return ' '.join(tokens)


#     # def stringify_dump(self):
#     #     return f"{self._move_list=} {self._cap_list=}"


#     # def stringify_debug_1(self):
#     #     return f"{len(self._move_list)=} {len(self._cap_list)=}"


#     # def copy_bpm(self):
#     #     return BackwardsPlotModel(
#     #             move_list                                   = list(self._move_list),
#     #             cap_list                                    = list(self._cap_list))
