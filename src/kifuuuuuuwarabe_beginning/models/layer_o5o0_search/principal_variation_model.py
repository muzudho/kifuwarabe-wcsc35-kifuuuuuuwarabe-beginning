from ..layer_o1o0 import constants


class PrincipalVariationModel:
    """読み筋モデル。
    """


    @staticmethod
    def create_zeroth_pv(
            out_of_termination_is_gote_arg,
            vertical_list_of_backwards_plot_model_arg   # TODO 廃止方針。
    ):
        """TODO ０手の［読み筋］。
        Parameters
        ----------
        out_of_termination_is_gote_arg : bool
            ［終端外］は後手か？
        vertical_list_of_backwards_plot_model_arg : _
            TODO 廃止方針。
        """
        return PrincipalVariationModel(
                frontward_vertical_list_of_move_arg         = [],
                frontward_vertical_list_of_cap_pt_arg       = [],
                frontward_vertical_list_of_value_arg        = [],
                frontward_vertical_list_of_comment_arg      = [],
                backward_vertical_list_of_value_arg         = [],
                backward_vertical_list_of_comment_arg       = [],
                out_of_termination_is_mars_arg              = False,
                out_of_termination_is_gote_arg              = out_of_termination_is_gote_arg,
                out_of_termination_state_arg                = constants.out_of_termination_state.HORIZON,
                out_of_termination_comment_arg              = '',
                is_terminate_arg                            = False,
                # TODO 廃止方針。
                # 終端外が有る分、他のリストより要素１個多い。＜水平線＞がデフォルト値。
                vertical_list_of_backwards_plot_model_arg   = vertical_list_of_backwards_plot_model_arg)


    def __init__(
            self,
            frontward_vertical_list_of_move_arg,
            frontward_vertical_list_of_cap_pt_arg,
            frontward_vertical_list_of_value_arg,
            frontward_vertical_list_of_comment_arg,
            backward_vertical_list_of_value_arg,
            backward_vertical_list_of_comment_arg,
            out_of_termination_is_mars_arg,
            out_of_termination_is_gote_arg,
            out_of_termination_state_arg,
            out_of_termination_comment_arg,
            is_terminate_arg,
            vertical_list_of_backwards_plot_model_arg):  # TODO 廃止方針。
        """
        Parameters
        ----------
        frontward_vertical_list_of_move_arg : list<int>
            ［前向き探索］中に確定しながら追加していく［シーショーギの指し手］の履歴。
        frontward_vertical_list_of_cap_pt_arg : list<int>
            ［前向き探索］中に確定しながら追加していく［取った駒の種類］の履歴。
        frontward_vertical_list_of_value_arg : list<int>
            ［前向き探索］中に確定しながら追加していく［取った駒の点数］の履歴。地球視点。
        frontward_vertical_list_of_comment_arg : list<str>
            ［前向き探索］中に確定しながら追加していく［コメント］の履歴。地球視点。
        backward_vertical_list_of_value_arg : list<int>
            ［後ろ向き探索］中に追加していく［局面評価値］の履歴。
        backward_vertical_list_of_comment_arg : list<str>
            ［後ろ向き探索］中に追加していく［指し手のコメント］の履歴。
        out_of_termination_is_mars_arg : bool
            ［終端外］は火星か。（後ろ向きに設定します）
        out_of_termination_is_gote_arg : bool
            ［終端外］は後手か。（後ろ向きに設定します）
        out_of_termination_state_arg : int
            ［終端外］は何か。
        out_of_termination_comment_arg : str
            ［終端外］へのコメント。
        vertical_list_of_backwards_plot_model_arg : list<BackwardsPlotModel>
            ［後ろ向き探索］中に追加していく［読み筋］の履歴。
            ０番目の要素に［終端外］を含む分、他のリストより要素１個多い。
            TODO 廃止方針。
        is_terminate_arg : bool
            ［読み筋］が終わっているか。
        """

        # ［前向き探索］しながら追加していく要素。
        self._frontward_vertical_list_of_move_pv        = frontward_vertical_list_of_move_arg
        self._frontward_vertical_list_of_cap_pt_pv      = frontward_vertical_list_of_cap_pt_arg
        self._frontward_vertical_list_of_value_pv       = frontward_vertical_list_of_value_arg
        self._frontward_vertical_list_of_comment_pv     = frontward_vertical_list_of_comment_arg

        # ［後ろ向き探索］しながら追加していく要素。
        self._backward_vertical_list_of_value_pv        = backward_vertical_list_of_value_arg
        self._backward_vertical_list_of_comment_pv      = backward_vertical_list_of_comment_arg

        # ［終端外］で設定する要素。
        # TODO ［終端外］オブジェクトというまとまりにするか？
        self._out_of_termination_is_mars                = out_of_termination_is_mars_arg
        self._out_of_termination_is_gote                = out_of_termination_is_gote_arg
        self._out_of_termination_state                  = out_of_termination_state_arg
        self._out_of_termination_comment                = out_of_termination_comment_arg
        self._is_terminate_pv                              = is_terminate_arg

        # TODO 廃止方針の要素。
        self._deprecated_vertical_list_of_backwards_plot_model_pv  = vertical_list_of_backwards_plot_model_arg


    ############################################
    # MARK: 前向き探索しながら伸ばす縦の指し手リスト
    ############################################

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


    ##############################################
    # MARK: 後ろ向き探索しながら伸ばす縦の指し手リスト
    ##############################################

    @property
    def backward_vertical_list_of_value_pv(self):
        """［後ろ向き探索］しながら追加していく［局面評価値］の履歴。
        """
        return self._backward_vertical_list_of_value_pv


    @property
    def backward_vertical_list_of_comment_pv(self):
        """［後ろ向き探索］しながら追加していく［指し手のコメント］の履歴。
        """
        return self._backward_vertical_list_of_comment_pv


    ###########################################
    # MARK: ［前向き探索］の方の、末端手目に近い方
    ###########################################

    @property
    def leafer_move_in_frontward_pv(self):
        """［前向き探索］の方の、末端手目に近い方の［指し手］。
        """
        return self._frontward_vertical_list_of_move_pv[-1]


    @property
    def leafer_cap_pt_in_frontward_pv(self):
        """［前向き探索］の方の、末端手目に近い方の［最後に取った駒］。
        """
        return self._frontward_vertical_list_of_cap_pt_pv[-1]


    @property
    def leafer_value_in_frontward_pv(self):
        """［前向き探索］の方の、末端手目に近い方の［局面評価値］。
        """
        if len(self._frontward_vertical_list_of_value_pv) == 0:
            return constants.value.ZERO
        return self._frontward_vertical_list_of_value_pv[-1]


    ###########################################
    # MARK: ［後ろ向き探索］の方の、１手目に近い方
    ###########################################

    @property
    def rooter_value_in_backward_pv(self):
        """［後ろ向き探索］の方の、１手目に近い方の［局面評価値］。
        """
        return self._backward_vertical_list_of_value_pv[-1]


    @property
    def rooter_comment_in_backward_pv(self):
        """［後ろ向き探索］の方の、１手目に近い方の［指し手のコメント］。
        """
        return self._backward_vertical_list_of_comment_pv[-1]


    def get_root_value_in_backward_pv(self):
        """TODO ［後ろ向き探索］の方の、初手の［局面評価値］。地球視点。
        旧名: get_exchange_value_on_earth
        """

        # TODO 取った駒を、葉要素から点数付けして累計する。
        # 先手、後手を正確に把握していれば、前から順に累計しても同じ。
        #
        # 旧方式
        return self.deprecated_rooter_backwards_plot_model_in_backward_pv.get_exchange_value_on_earth()

    ##############
    # MARK: 終端外
    ##############

    def out_of_termination_is_mars(self):
        """［終端外］は火星か？
        """
        return self._out_of_termination_is_mars


    def out_of_termination_is_gote(self):
        """［終端外］は後手か？
        """
        return self._out_of_termination_is_gote


    def out_of_termination_state(self):
        """［終端外］の状態。
        """
        return self._out_of_termination_state


    def out_of_termination_comment(self):
        """［終端外］の［指し手のコメント］。
        """
        return self._out_of_termination_comment


    ##################
    # MARK: 前向き探索
    ##################

    def new_and_append_in_frontward_pv(
            self,
            move_arg,
            cap_pt_arg,
            value_arg,
            backwards_plot_model_arg,
            frontward_comment_arg,
            replace_is_terminate_arg):
        """［前向き探索］中に要素追加。
        """
        copied_frontward_vertical_list_of_move_pv = list(self._frontward_vertical_list_of_move_pv)
        copied_frontward_vertical_list_of_move_pv.append(move_arg)
        copied_frontward_vertical_list_of_cap_pt_pv = list(self._frontward_vertical_list_of_cap_pt_pv)
        copied_frontward_vertical_list_of_cap_pt_pv.append(cap_pt_arg)
        copied_frontward_vertical_list_of_value_pv = list(self._frontward_vertical_list_of_value_pv)
        copied_frontward_vertical_list_of_value_pv.append(value_arg)
        copied_vertical_list_of_backwards_plot_model_pv = self._create_copied_bpm_list()    # TODO 廃止方針。
        copied_vertical_list_of_backwards_plot_model_pv.append(backwards_plot_model_arg)
        copied_frontward_vertical_list_of_comment_pv = list(self._frontward_vertical_list_of_comment_pv)
        copied_frontward_vertical_list_of_comment_pv.append(frontward_comment_arg)

        # NOTE リストはコピー渡し。
        return PrincipalVariationModel(
                frontward_vertical_list_of_move_arg         = copied_frontward_vertical_list_of_move_pv,
                frontward_vertical_list_of_cap_pt_arg       = copied_frontward_vertical_list_of_cap_pt_pv,
                frontward_vertical_list_of_value_arg        = copied_frontward_vertical_list_of_value_pv,
                frontward_vertical_list_of_comment_arg      = copied_frontward_vertical_list_of_comment_pv,
                backward_vertical_list_of_value_arg         = self._backward_vertical_list_of_value_pv,
                backward_vertical_list_of_comment_arg       = self._backward_vertical_list_of_comment_pv,
                out_of_termination_is_mars_arg              = self._out_of_termination_is_mars,
                out_of_termination_is_gote_arg              = self._out_of_termination_is_gote,
                out_of_termination_state_arg                = self._out_of_termination_state,
                out_of_termination_comment_arg              = '',
                is_terminate_arg                            = replace_is_terminate_arg,
                vertical_list_of_backwards_plot_model_arg   = copied_vertical_list_of_backwards_plot_model_pv)


    ###################
    # MARK: 後ろ向き探索
    ###################

    def append_move_in_backward_pv(self, move, capture_piece_type, best_value, hint):
        """［後ろ向き探索］中に要素追加。
        """
        self.deprecated_rooter_backwards_plot_model_in_backward_pv.append_move_from_back(
                move                = move,
                capture_piece_type  = capture_piece_type,
                best_value          = best_value,
                hint                = hint)


    #####################
    # MARK: その他いろいろ
    #####################

    @property
    def is_terminate_pv(self):
        """探索は終端です。
        TODO ［終端外］オブジェクトの有無に変更したい。
        """
        return self._is_terminate_pv


    def set_is_terminate_pv(self, value):
        """［終端外］設定。
        * ［指し手一覧のクリーニング］後とか。
        TODO だったら、フラグではなく、［終端外］オブジェクトを設定したい。
        """
        self._is_terminate_pv = value


    def _create_copied_bpm_list(self):
        """［後ろ向き探索の評価値モデル］のリストを、要素１つずつコピー。
        """
        new_bpm_list = []
        for old_bpm in self._deprecated_vertical_list_of_backwards_plot_model_pv:
            new_bpm_list.append(old_bpm.copy_bpm())
        return new_bpm_list
    

    def copy_pv(self):
        """コピー。
        """

        # NOTE リストはコピー渡し。
        return PrincipalVariationModel(
                frontward_vertical_list_of_move_arg         = list(self._frontward_vertical_list_of_move_pv),
                frontward_vertical_list_of_cap_pt_arg       = list(self._frontward_vertical_list_of_cap_pt_pv),
                frontward_vertical_list_of_value_arg        = list(self._frontward_vertical_list_of_value_pv),
                frontward_vertical_list_of_comment_arg      = list(self._frontward_vertical_list_of_comment_pv),
                backward_vertical_list_of_value_arg         = list(self._backward_vertical_list_of_value_pv),
                backward_vertical_list_of_comment_arg       = list(self._backward_vertical_list_of_comment_pv),
                out_of_termination_is_mars_arg              = self._out_of_termination_is_mars,
                out_of_termination_is_gote_arg              = self._out_of_termination_is_gote,
                out_of_termination_state_arg                = self._out_of_termination_state,
                out_of_termination_comment_arg              = self._out_of_termination_comment_arg,
                is_terminate_arg                            = self._is_terminate_pv,
                vertical_list_of_backwards_plot_model_arg   = self._create_copied_bpm_list())


    def stringify_2(self):
        return self.deprecated_rooter_backwards_plot_model_in_backward_pv.stringify_2()


    @property
    def peek_move(self):
        return self.deprecated_rooter_backwards_plot_model_in_backward_pv.peek_move


    @property
    def is_capture_at_last(self):
        return self.deprecated_rooter_backwards_plot_model_in_backward_pv.is_capture_at_last


    ###############
    # MARK: 廃止方針
    ###############

    # @property
    # def vertical_list_of_backwards_plot_model_pv(self):
    #     """［後ろ向き探索の読み筋モデル］の履歴。
    #     ０番目の要素に［終端外］を含む分、他のリストより要素１個多い。
    #     TODO 廃止方針。
    #     """
    #     return self._deprecated_vertical_list_of_backwards_plot_model_pv


    @property
    def deprecated_rooter_backwards_plot_model_in_backward_pv(self):
        """［後ろ向き探索］の方の、１手目に近い方の［読み筋モデル］。
        TODO 廃止方針。
        """
        return self._deprecated_vertical_list_of_backwards_plot_model_pv[-1]


    def set_deprecated_rooter_backwards_plot_model_in_backward_pv(self, value):
        """TODO 廃止方針。
        """
        self._deprecated_vertical_list_of_backwards_plot_model_pv[-1] = value


    ##############
    # MARK: その他
    ##############

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
