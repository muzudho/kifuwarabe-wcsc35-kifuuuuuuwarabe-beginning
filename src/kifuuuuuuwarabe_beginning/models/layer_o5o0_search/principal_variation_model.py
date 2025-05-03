from ..layer_o1o0 import constants


class PrincipalVariationModel:
    """読み筋モデル。
    """


    def __init__(self, vertical_list_of_move_pv, vertical_list_of_cap_pt_pv, vertical_list_of_value_pv, vertical_list_of_backwards_plot_model_pv, is_terminate=False):
        """
        Parameters
        ----------
        vertical_list_of_move_pv : list<int>
            シーショーギの指し手のリスト。
        vertical_list_of_cap_pt_pv : list<int>
            取った駒の種類のリスト。
        vertical_list_of_value_pv : list<int>
            ［取った駒の点数］のリスト。地球視点。
        vertical_list_of_backwards_plot_model_pv : list<BackwardsPlotModel>
            ［後ろ向き探索の読み筋］のリスト。
            終端外が有る分、他のリストより要素１個多い。
        """
        self._vertical_list_of_move_pv = vertical_list_of_move_pv
        self._vertical_list_of_cap_pt_pv = vertical_list_of_cap_pt_pv
        self._vertical_list_of_value_pv = vertical_list_of_value_pv
        self._vertical_list_of_backwards_plot_model = vertical_list_of_backwards_plot_model_pv
        self._backwards_plot_model_pv = vertical_list_of_backwards_plot_model_pv[-1]   # TODO 廃止
        self._is_terminate = is_terminate


    ####################
    # MARK: 最後の指し手
    ####################

    @property
    def last_move_pv(self):
        """最終の子の指し手。
        """
        return self._vertical_list_of_move_pv[-1]


    @property
    def last_cap_pt_pv(self):
        """最後の取った駒。
        """
        return self._vertical_list_of_cap_pt_pv[-1]


    @property
    def last_value_pv(self):
        """評価値。
        """
        if len(self._vertical_list_of_value_pv) == 0:
            return constants.value.ZERO
        return self._vertical_list_of_value_pv[-1]


    @property
    def vertical_list_of_move_pv(self):
        """指し手の履歴。
        """
        return self._vertical_list_of_move_pv


    @property
    def vertical_list_of_cap_pt_pv(self):
        """取った駒の種類のリスト。
        """
        return self._vertical_list_of_cap_pt_pv


    @property
    def vertical_list_of_backwards_plot_model_pv(self):
        """［後ろ向き探索の読み筋モデル］のリスト。
        """
        return self._vertical_list_of_backwards_plot_model_pv


    @property
    def backwards_plot_model(self):
        """後ろ向き探索の読み筋。
        TODO 廃止
        """
        return self._backwards_plot_model


    @backwards_plot_model.setter
    def backwards_plot_model(self, value):
        self._backwards_plot_model = value


    @property
    def is_terminate(self):
        """探索は終端です。
        """
        return self._is_terminate

    
    @is_terminate.setter
    def is_terminate(self, value):
        self._is_terminate = value


    def _create_copied_bpm_list(self):
        """［後ろ向き探索の評価値モデル］のリストを、要素１つずつコピー。
        """
        new_bpm_list = []
        for old_bpm in self._vertical_list_of_backwards_plot_model_pv:
            new_bpm_list.append(old_bpm.copy_bpm())
        return new_bpm_list
    

    def copy_pv(self):
        """コピー。
        """

        # NOTE リストはコピー渡し。
        return PrincipalVariationModel(
                vertical_list_of_move_pv                    = list(self._vertical_list_of_move_pv),
                vertical_list_of_cap_pt_pv                  = list(self._vertical_list_of_cap_pt_pv),
                vertical_list_of_value_pv                   = list(self._vertical_list_of_value_pv),
                vertical_list_of_backwards_plot_model_pv    = self._create_copied_bpm_list(),
                is_terminate                                = self._is_terminate)


    def new_and_append_pv(self, move_pv, cap_pt_pv, value_pv, backwards_plot_model_pv, replace_is_terminate):
        copied_vertical_list_of_move_pv = list(self._vertical_list_of_move_pv)
        copied_vertical_list_of_move_pv.append(move_pv)
        copied_vertical_list_of_cap_pt_pv = list(self._vertical_list_of_cap_pt_pv)
        copied_vertical_list_of_cap_pt_pv.append(cap_pt_pv)
        copied_vertical_list_of_value_pv = list(self._vertical_list_of_value_pv)
        copied_vertical_list_of_value_pv.append(value_pv)
        copied_vertical_list_of_backwards_plot_model_pv = self._create_copied_bpm_list()
        copied_vertical_list_of_backwards_plot_model_pv.append(backwards_plot_model_pv)

        # NOTE リストはコピー渡し。
        return PrincipalVariationModel(
                vertical_list_of_move_pv                    = copied_vertical_list_of_move_pv,
                vertical_list_of_cap_pt_pv                  = copied_vertical_list_of_cap_pt_pv,
                vertical_list_of_value_pv                   = copied_vertical_list_of_value_pv,
                vertical_list_of_backwards_plot_model_pv    = copied_vertical_list_of_backwards_plot_model_pv,
                is_terminate                                = replace_is_terminate)


    # @property
    # def is_mars_at_peek(self):
    #     """最後の要素は火星か？
    #     """
    #     if len(self._vertical_list_of_move_pv) % 2 == 0:
    #         return False
    #     return True


    # @property
    # def is_gote_at_peek(self):
    #     """最後の要素は後手か？
    #     """
    #     if len(self._vertical_list_of_move_pv) % 2 == 0:
    #         return not self.is_gote_at_first
    #     return self.is_gote_at_first


    # def equals_move_usi_list(self, move_usi_list):
    #     """完全一致判定。
    #     """
    #     usi_list = []
    #     for move in self._move_list:
    #         usi_list.append(cshogi.move_to_usi(move))

    #     return usi_list == move_usi_list


    # def stringify(self):
    #     """文字列化。
    #     """
    #     tokens = []

    #     is_mars = self.is_mars_at_peek
    #     is_gote = self.is_gote_at_peek

    #     len_of_move_list = len(self._move_list)
    #     for layer_no in range(0, len_of_move_list):
    #         move = self._move_list[layer_no]
    #         cap_pt = self._cap_list[layer_no]

    #         # 指し手のUSI表記を独自形式に変更。
    #         move_jp_str = JapaneseMoveModel.from_move(
    #                 move    = move,
    #                 cap_pt  = cap_pt,
    #                 is_mars = is_mars,
    #                 is_gote = is_gote).stringify()

    #         tokens.append(move_jp_str)

    #         # 手番交代
    #         is_mars = not is_mars
    #         is_gote = not is_gote

    #     return ','.join(tokens)
