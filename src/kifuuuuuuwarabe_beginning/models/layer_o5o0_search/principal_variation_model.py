from ..layer_o1o0 import constants


class PrincipalVariationModel:
    """読み筋モデル。
    """


    def __init__(
            self,
            frontward_vertical_list_of_move_pv,
            frontward_vertical_list_of_cap_pt_pv,
            frontward_vertical_list_of_value_pv,
            frontward_vertical_list_of_comment_pv,
            vertical_list_of_backwards_plot_model_pv,
            backward_vertical_list_of_comment_pv,
            out_of_termination_is_mars,
            out_of_termination_is_gote,
            out_of_termination_state,
            is_terminate=False):
        """
        Parameters
        ----------
        frontward_vertical_list_of_move_pv : list<int>
            ［前向き探索］中に確定しながら追加していく［シーショーギの指し手］の履歴。
        frontward_vertical_list_of_cap_pt_pv : list<int>
            ［前向き探索］中に確定しながら追加していく［取った駒の種類］の履歴。
        frontward_vertical_list_of_value_pv : list<int>
            ［前向き探索］中に確定しながら追加していく［取った駒の点数］の履歴。地球視点。
        frontward_vertical_list_of_comment_pv : list<string>
            ［前向き探索］中に確定しながら追加していく［コメント］の履歴。地球視点。
        vertical_list_of_backwards_plot_model_pv : list<BackwardsPlotModel>
            ［後ろ向き探索］中に追加していく［読み筋］の履歴。
            ０番目の要素に［終端外］を含む分、他のリストより要素１個多い。
            TODO 廃止方針。
        backward_vertical_list_of_comment_pv : list<string>
            ［後ろ向き探索］中に追加していく［指し手のコメント］の履歴。
            ０番目の要素に［終端外］を含む分、他のリストより要素１個多い。
        out_of_termination_is_mars : bool
            ［終端外］は火星か。（後ろ向きに設定します）
        out_of_termination_is_gote : bool
            ［終端外］は後手か。（後ろ向きに設定します）
        out_of_termination_state : int
            ［終端外］は何か。
        """
        self._frontward_vertical_list_of_move_pv = frontward_vertical_list_of_move_pv
        self._frontward_vertical_list_of_cap_pt_pv = frontward_vertical_list_of_cap_pt_pv
        self._frontward_vertical_list_of_value_pv = frontward_vertical_list_of_value_pv
        self._frontward_vertical_list_of_comment_pv = frontward_vertical_list_of_comment_pv
        self._vertical_list_of_backwards_plot_model_pv = vertical_list_of_backwards_plot_model_pv
        self._backwards_plot_model_pv = vertical_list_of_backwards_plot_model_pv[-1]   # TODO 廃止方針
        self._backward_vertical_list_of_comment_pv = backward_vertical_list_of_comment_pv
        self._out_of_termination_is_mars = out_of_termination_is_mars
        self._out_of_termination_is_gote = out_of_termination_is_gote
        self._out_of_termination_state = out_of_termination_state
        self._is_terminate = is_terminate


    #######################
    # MARK: 縦の指し手リスト
    #######################

    @property
    def frontward_vertical_list_of_move_pv(self):
        """［指し手］の履歴。
        """
        return self._frontward_vertical_list_of_move_pv


    @property
    def frontward_vertical_list_of_cap_pt_pv(self):
        """［取った駒の種類］の履歴。
        """
        return self._frontward_vertical_list_of_cap_pt_pv


    @property
    def frontward_vertical_list_of_value_pv(self):
        """［局面評価値］の履歴。
        """
        return self._frontward_vertical_list_of_value_pv


    @property
    def frontward_vertical_list_of_comment_pv(self):
        """［後ろ向き探索の指し手のコメント］の履歴。
        ０番目の要素に［終端外］を含む分、他のリストより要素１個多い。
        """
        return self._frontward_vertical_list_of_comment_pv


    @property
    def vertical_list_of_backwards_plot_model_pv(self):
        """［後ろ向き探索の読み筋モデル］の履歴。
        ０番目の要素に［終端外］を含む分、他のリストより要素１個多い。
        """
        return self._vertical_list_of_backwards_plot_model_pv


    @property
    def backward_vertical_list_of_comment_pv(self):
        """［後ろ向き探索の指し手のコメント］の履歴。
        ０番目の要素に［終端外］を含む分、他のリストより要素１個多い。
        """
        return self._backward_vertical_list_of_comment_pv


    #######################
    # MARK: 末端手目に近い方
    #######################

    @property
    def leafer_move_pv(self):
        """末端手目に近い方の［指し手］。
        """
        return self._frontward_vertical_list_of_move_pv[-1]


    @property
    def leafer_cap_pt_pv(self):
        """末端手目に近い方の［最後に取った駒］。
        """
        return self._frontward_vertical_list_of_cap_pt_pv[-1]


    @property
    def leafer_value_pv(self):
        """末端手目に近い方の［局面評価値］。
        """
        if len(self._frontward_vertical_list_of_value_pv) == 0:
            return constants.value.ZERO
        return self._frontward_vertical_list_of_value_pv[-1]


    #####################
    # MARK: １手目に近い方
    #####################

    @property
    def rooter_backwards_plot_model_pv(self):
        """１手目に近い方の［後ろ向き探索の読み筋モデル］。
        """
        return self._vertical_list_of_backwards_plot_model_pv[-1]


    @property
    def rooter_comment_pv(self):
        """１手目に近い方の［後ろ向き探索の指し手のコメント］。
        """
        return self._vertical_list_of_comment_pv[-1]


    @rooter_backwards_plot_model_pv.setter
    def rooter_backwards_plot_model_pv(self, value):
        self._vertical_list_of_backwards_plot_model_pv[-1] = value


    ##############
    # MARK: 終端外
    ##############

    def out_of_termination_is_mars(self):
        return self._out_of_termination_is_mars


    def out_of_termination_is_gote(self):
        return self._out_of_termination_is_gote


    def out_of_termination_state(self):
        return self._out_of_termination_state


    ##############
    # MARK: その他
    ##############

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
                frontward_vertical_list_of_move_pv          = list(self._frontward_vertical_list_of_move_pv),
                frontward_vertical_list_of_cap_pt_pv        = list(self._frontward_vertical_list_of_cap_pt_pv),
                frontward_vertical_list_of_value_pv         = list(self._frontward_vertical_list_of_value_pv),
                frontward_vertical_list_of_comment_pv       = list(self._frontward_vertical_list_of_comment_pv),
                vertical_list_of_backwards_plot_model_pv    = self._create_copied_bpm_list(),
                backward_vertical_list_of_comment_pv        = list(self._backward_vertical_list_of_comment_pv),
                out_of_termination_is_mars                  = self._out_of_termination_is_mars,
                out_of_termination_is_gote                  = self._out_of_termination_is_gote,
                out_of_termination_state                    = self._out_of_termination_state,
                is_terminate                                = self._is_terminate)


    def new_and_append_pv(
            self,
            move_pv,
            cap_pt_pv,
            value_pv,
            backwards_plot_model_pv,
            frontward_comment_pv,
            backward_comment_pv,
            replace_is_terminate):
        copied_frontward_vertical_list_of_move_pv = list(self._frontward_vertical_list_of_move_pv)
        copied_frontward_vertical_list_of_move_pv.append(move_pv)
        copied_frontward_vertical_list_of_cap_pt_pv = list(self._frontward_vertical_list_of_cap_pt_pv)
        copied_frontward_vertical_list_of_cap_pt_pv.append(cap_pt_pv)
        copied_frontward_vertical_list_of_value_pv = list(self._frontward_vertical_list_of_value_pv)
        copied_frontward_vertical_list_of_value_pv.append(value_pv)
        copied_vertical_list_of_backwards_plot_model_pv = self._create_copied_bpm_list()    # TODO 廃止方針。
        copied_vertical_list_of_backwards_plot_model_pv.append(backwards_plot_model_pv)
        copied_frontward_vertical_list_of_comment_pv = list(self._frontward_vertical_list_of_comment_pv)
        copied_frontward_vertical_list_of_comment_pv.append(frontward_comment_pv)
        copied_backward_vertical_list_of_comment_pv = list(self._backward_vertical_list_of_comment_pv)
        copied_backward_vertical_list_of_comment_pv.append(backward_comment_pv)

        # NOTE リストはコピー渡し。
        return PrincipalVariationModel(
                frontward_vertical_list_of_move_pv          = copied_frontward_vertical_list_of_move_pv,
                frontward_vertical_list_of_cap_pt_pv        = copied_frontward_vertical_list_of_cap_pt_pv,
                frontward_vertical_list_of_value_pv         = copied_frontward_vertical_list_of_value_pv,
                vertical_list_of_backwards_plot_model_pv    = copied_vertical_list_of_backwards_plot_model_pv,
                frontward_vertical_list_of_comment_pv       = copied_frontward_vertical_list_of_comment_pv,
                backward_vertical_list_of_comment_pv        = copied_backward_vertical_list_of_comment_pv,
                out_of_termination_is_mars                  = self._out_of_termination_is_mars,
                out_of_termination_is_gote                  = self._out_of_termination_is_gote,
                out_of_termination_state                    = self._out_of_termination_state,
                is_terminate                                = replace_is_terminate)


    # @property
    # def is_mars_at_peek(self):
    #     """最後の要素は火星か？
    #     """
    #     if len(self._frontward_vertical_list_of_move_pv) % 2 == 0:
    #         return False
    #     return True


    # @property
    # def is_gote_at_peek(self):
    #     """最後の要素は後手か？
    #     """
    #     if len(self._frontward_vertical_list_of_move_pv) % 2 == 0:
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
