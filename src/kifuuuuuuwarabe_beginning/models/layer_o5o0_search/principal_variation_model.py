import cshogi

from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import constants, Mars, SquareModel
from ..layer_o2o0 import BackwardsPlotModel
from .termination_model import TerminationModel


class PrincipalVariationModel:
    """読み筋モデル。

    TODO HistoryNode へ移行したい。
    """


    @staticmethod
    def create_zeroth_pv(
            out_of_termination_is_gote_arg,
            search_context_model):
        """TODO ０手の［読み筋］。
        Parameters
        ----------
        out_of_termination_is_gote_arg : bool
            ［終端外］は後手か？
        search_context_model : _
            TODO 廃止方針。
        """

        termination_model = TerminationModel(
                is_mars_arg = False,
                is_gote_arg = out_of_termination_is_gote_arg,
                state_arg   = constants.out_of_termination_state_const.HORIZON,
                comment_arg = '')

        obj_1 = PrincipalVariationModel(
                frontward_vertical_list_of_move_arg         = [],
                frontward_vertical_list_of_cap_pt_arg       = [],
                frontward_vertical_list_of_value_arg        = [],
                frontward_vertical_list_of_comment_arg      = [],
                backward_vertical_list_of_move_arg          = [],
                backward_vertical_list_of_cap_pt_arg        = [],
                backward_vertical_list_of_value_arg         = [],
                backward_vertical_list_of_comment_arg       = [],
                out_of_termination_is_mars_arg              = termination_model.is_mars_tm,
                out_of_termination_is_gote_arg              = termination_model.is_gote_tm,
                out_of_termination_state_arg                = termination_model.state_tm,
                out_of_termination_comment_arg              = termination_model.comment_tm,
                search_is_over_arg                          = False,
                # TODO 廃止方針。
                # 終端外が有る分、他のリストより要素１個多い。＜水平線＞がデフォルト値。
                vertical_list_of_backwards_plot_model_arg   = [])

        obj_1.setup_to_horizon(search_context_model=search_context_model)

        return obj_1


    def __init__(
            self,
            frontward_vertical_list_of_move_arg,
            frontward_vertical_list_of_cap_pt_arg,
            frontward_vertical_list_of_value_arg,
            frontward_vertical_list_of_comment_arg,
            backward_vertical_list_of_move_arg,
            backward_vertical_list_of_cap_pt_arg,
            backward_vertical_list_of_value_arg,
            backward_vertical_list_of_comment_arg,
            out_of_termination_is_mars_arg,
            out_of_termination_is_gote_arg,
            out_of_termination_state_arg,
            out_of_termination_comment_arg,
            search_is_over_arg,
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
        backward_vertical_list_of_move_arg : list<int>
            ［後ろ向き探索］中に確定しながら追加していく［シーショーギの指し手］の履歴。
        backward_vertical_list_of_cap_pt_arg : list<int>
            ［後ろ向き探索］中に確定しながら追加していく［取った駒の種類］の履歴。
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
        vertical_list_of_backwards_plot_model_arg : list<B ackwardsPlotModel>
            ［後ろ向き探索］中に追加していく［読み筋］の履歴。
            ０番目の要素に［終端外］を含む分、他のリストより要素１個多い。
            TODO 廃止方針。
        search_is_over_arg : bool
            ［読み筋］が終わっているか。
        """

        # ［前向き探索］しながら追加していく要素。
        self._frontward_vertical_list_of_move_pv        = frontward_vertical_list_of_move_arg
        self._frontward_vertical_list_of_cap_pt_pv      = frontward_vertical_list_of_cap_pt_arg
        self._frontward_vertical_list_of_value_pv       = frontward_vertical_list_of_value_arg
        self._frontward_vertical_list_of_comment_pv     = frontward_vertical_list_of_comment_arg

        # ［後ろ向き探索］しながら追加していく要素。
        self._backward_vertical_list_of_move_pv         = backward_vertical_list_of_move_arg
        self._backward_vertical_list_of_cap_pt_pv       = backward_vertical_list_of_cap_pt_arg
        self._backward_vertical_list_of_value_pv        = backward_vertical_list_of_value_arg
        self._backward_vertical_list_of_comment_pv      = backward_vertical_list_of_comment_arg

        # ［終端外］で設定する要素。
        # TODO ［終端外］オブジェクトというまとまりにするか？
        self._out_of_termination_is_mars_pv             = out_of_termination_is_mars_arg
        self._out_of_termination_is_gote_pv             = out_of_termination_is_gote_arg
        self._out_of_termination_state_pv               = out_of_termination_state_arg
        self._out_of_termination_comment                = out_of_termination_comment_arg
        self._search_is_over_pv                         = search_is_over_arg

        # TODO 廃止方針の要素。
        self._deprecated_vertical_list_of_backwards_plot_model_pv   = vertical_list_of_backwards_plot_model_arg
        self._list_of_accumulate_exchange_value_on_earth_pv         = []


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
    def backward_vertical_list_of_move_pv(self):
        """［指し手］の履歴。
        """
        return self._backward_vertical_list_of_move_pv


    @property
    def backward_vertical_list_of_cap_pt_pv(self):
        """［取った駒の種類］の履歴。
        """
        return self._backward_vertical_list_of_cap_pt_pv

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


    @staticmethod
    def _get_out_of_termination_to_value_on_earth(out_of_termination_state_arg, is_mars_arg):
        """［終端外］の駒の価値。
        """
        if out_of_termination_state_arg == constants.out_of_termination_state_const.RESIGN:
            value = constants.value.GAME_OVER
        elif out_of_termination_state_arg == constants.out_of_termination_state_const.NYUGYOKU_WIN:
            value = constants.value.NYUGYOKU_WIN
        elif out_of_termination_state_arg == constants.out_of_termination_state_const.HORIZON:
            value = constants.value.ZERO
        elif out_of_termination_state_arg == constants.out_of_termination_state_const.NO_CANDIDATES:
            value = constants.value.ZERO
        elif out_of_termination_state_arg == constants.out_of_termination_state_const.QUIESCENCE:
            value = constants.value.ZERO
        else:
            raise ValueError(f"想定外の［終端外］。{out_of_termination_state_arg=}")

        # 対戦相手なら正負を逆転。
        if is_mars_arg:
            value *= -1

        return value


    def get_root_value_in_backward_pv(self, out_of_termination_is_mars_arg, out_of_termination_state_arg, list_of_accumulate_exchange_value_on_earth_arg):
        """TODO ［後ろ向き探索］の方の、初手の［局面評価値］。地球視点。
        """

        # TODO 取った駒を、葉要素から点数付けして累計する。
        # 先手、後手を正確に把握していれば、前から順に累計しても同じ。
        #
        # 旧方式
        if len(list_of_accumulate_exchange_value_on_earth_arg) == 0:
            return PrincipalVariationModel._get_out_of_termination_to_value_on_earth(   # ［終端外］の点数。
                    out_of_termination_state_arg    = out_of_termination_state_arg,
                    is_mars_arg                     = out_of_termination_is_mars_arg)

        return list_of_accumulate_exchange_value_on_earth_arg[-1]


    ##############
    # MARK: 終端外
    ##############

    def out_of_termination_is_mars_pv(self):
        """［終端外］は火星か？
        """
        return self._out_of_termination_is_mars_pv


    def out_of_termination_is_gote(self):
        """［終端外］は後手か？
        """
        return self._out_of_termination_is_gote_pv


    def out_of_termination_state_pv(self):
        """［終端外］の状態。
        """
        return self._out_of_termination_state_pv


    def out_of_termination_comment(self):
        """［終端外］の［指し手のコメント］。
        """
        return self._out_of_termination_comment


    def setup_to_nyugyoku_win(self, search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜入玉宣言勝ち＞')
        self._out_of_termination_is_mars_pv                 = search_context_model.gymnasium.is_mars
        self._out_of_termination_is_gote_pv                 = search_context_model.gymnasium.table.is_gote
        self._out_of_termination_state_pv                   = constants.out_of_termination_state_const.NYUGYOKU_WIN
        self._list_of_accumulate_exchange_value_on_earth_pv = []
        self._backward_vertical_list_of_move_pv             = []
        self._backward_vertical_list_of_cap_pv              = []
        self._backward_vertical_list_of_comment_pv          = []
        obj_1 = BackwardsPlotModel()
        self.set_deprecated_rooter_backwards_plot_model_in_backward_pv(obj_1)
        self.set_search_is_over_pv(True)


    def setup_to_no_candidates(self, info_depth, search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜候補手無し[深={info_depth}]＞")
        self._out_of_termination_is_mars_pv                 = search_context_model.gymnasium.is_mars
        self._out_of_termination_is_gote_pv                 = search_context_model.gymnasium.table.is_gote
        self._out_of_termination_state_pv                   = constants.out_of_termination_state_const.NO_CANDIDATES
        self._list_of_accumulate_exchange_value_on_earth_pv = []
        self._backward_vertical_list_of_move_pv             = []
        self._backward_vertical_list_of_cap_pv              = []
        self._backward_vertical_list_of_comment_pv          = []
        obj_1 = BackwardsPlotModel()
        self.set_deprecated_rooter_backwards_plot_model_in_backward_pv(obj_1)
        self.set_search_is_over_pv(True)


    def setup_to_quiescence(self, info_depth, search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜静止[深={info_depth}]＞")
        self._out_of_termination_is_mars_pv                 = search_context_model.gymnasium.is_mars
        self._out_of_termination_is_gote_pv                 = search_context_model.gymnasium.table.is_gote
        self._out_of_termination_state_pv                   = constants.out_of_termination_state_const.QUIESCENCE
        self._list_of_accumulate_exchange_value_on_earth_pv = []
        self._backward_vertical_list_of_move_pv             = []
        self._backward_vertical_list_of_cap_pv              = []
        self._backward_vertical_list_of_comment_pv          = []
        obj_1 = BackwardsPlotModel()
        self.set_deprecated_rooter_backwards_plot_model_in_backward_pv(obj_1)
        self.set_search_is_over_pv(True)


    def setup_to_game_over(self, search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')
        self._out_of_termination_is_mars_pv                 = search_context_model.gymnasium.is_mars
        self._out_of_termination_is_gote_pv                 = search_context_model.gymnasium.table.is_gote
        self._out_of_termination_state_pv                   = constants.out_of_termination_state_const.RESIGN
        self._list_of_accumulate_exchange_value_on_earth_pv = []
        self._backward_vertical_list_of_move_pv             = []
        self._backward_vertical_list_of_cap_pv              = []
        self._backward_vertical_list_of_comment_pv          = []
        obj_1 = BackwardsPlotModel()
        self.set_deprecated_rooter_backwards_plot_model_in_backward_pv(obj_1)
        self.set_search_is_over_pv(True)


    def setup_to_mate_move_in_1_ply(self, info_depth, mate_move, search_context_model):
        """一手詰まされ。
        """
        dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
        cap_pt = search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
        piece_exchange_value_on_earth = PieceValuesModel.get_piece_exchange_value_on_earth(
                pt          = cap_pt,
                is_mars     = search_context_model.gymnasium.is_mars)
        
        search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=mate_move, cap_pt=cap_pt, value=piece_exchange_value_on_earth, comment='＜一手詰め＞')
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')

        is_mars_at_out_of_termination = not search_context_model.gymnasium.is_mars    # ［詰む］のは、もう１手先だから not する。

        self._out_of_termination_is_mars_pv                 = search_context_model.gymnasium.is_mars
        self._out_of_termination_is_gote_pv                 = search_context_model.gymnasium.table.is_gote
        self._out_of_termination_state_pv                   = constants.out_of_termination_state_const.RESIGN
        self._list_of_accumulate_exchange_value_on_earth_pv = []
        self._backward_vertical_list_of_move_pv             = []
        self._backward_vertical_list_of_cap_pv              = []
        self._backward_vertical_list_of_comment_pv          = []
        best_plot_model = BackwardsPlotModel()
    
        # 今回の手を付け加える。
        if is_mars_at_out_of_termination:
            best_value = constants.value.BIG_VALUE        # 火星の負け
        else:
            best_value = constants.value.SMALL_VALUE      # 地球の負け

        best_plot_model.append_move_from_back(
                move                = mate_move,
                capture_piece_type  = cap_pt,
                best_value          = best_value,
                #hint                = f"{info_depth}階で{Mars.japanese(is_mars_at_out_of_termination)}は一手詰まされ",
                list_of_accumulate_exchange_value_on_earth_arg  = self._list_of_accumulate_exchange_value_on_earth_pv)
        self.set_deprecated_rooter_backwards_plot_model_in_backward_pv(best_plot_model)
        self.set_search_is_over_pv(True)


    def setup_to_horizon(self, search_context_model):
        """読みの水平線。
        水平線はデフォルトの状態なので、深さは設定しません。
        """
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜水平線＞")
        self._out_of_termination_is_mars_pv                 = search_context_model.gymnasium.is_mars
        self._out_of_termination_is_gote_pv                 = search_context_model.gymnasium.table.is_gote
        self._out_of_termination_state_pv                   = constants.out_of_termination_state_const.HORIZON
        self._list_of_accumulate_exchange_value_on_earth_pv = []
        self._backward_vertical_list_of_move_pv             = []
        self._backward_vertical_list_of_cap_pv              = []
        self._backward_vertical_list_of_comment_pv          = []
        obj_1 = BackwardsPlotModel()
        self.set_deprecated_rooter_backwards_plot_model_in_backward_pv(obj_1)
        self.set_search_is_over_pv(True)


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
            replace_search_is_over_arg):
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

        termination_model = TerminationModel(
                is_mars_arg = self._out_of_termination_is_mars_pv,
                is_gote_arg = self._out_of_termination_is_gote,
                state_arg   = self._out_of_termination_state,
                comment_arg = '')

        # NOTE リストはコピー渡し。
        return PrincipalVariationModel(
                frontward_vertical_list_of_move_arg         = copied_frontward_vertical_list_of_move_pv,
                frontward_vertical_list_of_cap_pt_arg       = copied_frontward_vertical_list_of_cap_pt_pv,
                frontward_vertical_list_of_value_arg        = copied_frontward_vertical_list_of_value_pv,
                frontward_vertical_list_of_comment_arg      = copied_frontward_vertical_list_of_comment_pv,
                backward_vertical_list_of_move_arg          = self._backward_vertical_list_of_move_pv,
                backward_vertical_list_of_cap_pt_arg        = self._backward_vertical_list_of_cap_pt_pv,
                backward_vertical_list_of_value_arg         = self._backward_vertical_list_of_value_pv,
                backward_vertical_list_of_comment_arg       = self._backward_vertical_list_of_comment_pv,
                out_of_termination_is_mars_arg              = termination_model.is_mars_tm,
                out_of_termination_is_gote_arg              = termination_model.is_gote_tm,
                out_of_termination_state_arg                = termination_model.state_tm,
                out_of_termination_comment_arg              = termination_model.comment_tm,
                search_is_over_arg                          = replace_search_is_over_arg,
                vertical_list_of_backwards_plot_model_arg   = copied_vertical_list_of_backwards_plot_model_pv)


    ###################
    # MARK: 後ろ向き探索
    ###################

    def append_move_in_backward_pv(self, move, capture_piece_type, best_value, list_of_accumulate_exchange_value_on_earth_arg):
        """［後ろ向き探索］中に要素追加。
        """
        self.deprecated_rooter_backwards_plot_model_in_backward_pv.append_move_from_back(
                move                                            = move,
                capture_piece_type                              = capture_piece_type,
                best_value                                      = best_value,
                list_of_accumulate_exchange_value_on_earth_arg  = list_of_accumulate_exchange_value_on_earth_arg)


    #####################
    # MARK: その他いろいろ
    #####################

    @property
    def search_is_over_pv(self):
        """探索は終端です。
        TODO ［終端外］オブジェクトの有無に変更したい。
        """
        return self._search_is_over_pv


    def set_search_is_over_pv(self, value):
        """［終端外］設定。
        * ［指し手一覧のクリーニング］後とか。
        TODO だったら、フラグではなく、［終端外］オブジェクトを設定したい。
        """
        self._search_is_over_pv = value


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

        termination_model = TerminationModel(
                is_mars_arg = self._out_of_termination_is_mars_pv,
                is_gote_arg = self._out_of_termination_is_gote,
                state_arg   = self._out_of_termination_state,
                comment_arg = self._out_of_termination_comment_arg)

        # NOTE リストはコピー渡し。
        return PrincipalVariationModel(
                frontward_vertical_list_of_move_arg         = list(self._frontward_vertical_list_of_move_pv),
                frontward_vertical_list_of_cap_pt_arg       = list(self._frontward_vertical_list_of_cap_pt_pv),
                frontward_vertical_list_of_value_arg        = list(self._frontward_vertical_list_of_value_pv),
                frontward_vertical_list_of_comment_arg      = list(self._frontward_vertical_list_of_comment_pv),
                backward_vertical_list_of_move_arg          = list(self._backward_vertical_list_of_move_pv),
                backward_vertical_list_of_cap_pt_arg        = list(self._backward_vertical_list_of_cap_pt_pv),
                backward_vertical_list_of_value_arg         = list(self._backward_vertical_list_of_value_pv),
                backward_vertical_list_of_comment_arg       = list(self._backward_vertical_list_of_comment_pv),
                out_of_termination_is_mars_arg              = termination_model.is_mars_tm,
                out_of_termination_is_gote_arg              = termination_model.is_gote_tm,
                out_of_termination_state_arg                = termination_model.state_tm,
                out_of_termination_comment_arg              = termination_model.comment_tm,
                search_is_over_arg                          = self._search_is_over_pv,
                vertical_list_of_backwards_plot_model_arg   = self._create_copied_bpm_list())


    def stringify_2(self):
        return self.deprecated_rooter_backwards_plot_model_in_backward_pv.stringify_2()


    @property
    def peek_move_pv(self):
        return self.deprecated_rooter_backwards_plot_model_in_backward_pv.peek_move_bpm


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


    def get_len_of_deprecated_vertical_list_of_backwards_plot_model_pv(self):
        return len(self._deprecated_vertical_list_of_backwards_plot_model_pv)

    @property
    def deprecated_rooter_backwards_plot_model_in_backward_pv(self):
        """［後ろ向き探索］の方の、１手目に近い方の［読み筋モデル］。
        TODO 廃止方針。
        """
        return self._deprecated_vertical_list_of_backwards_plot_model_pv[-1]


    def set_deprecated_rooter_backwards_plot_model_in_backward_pv(self, value):
        """TODO 廃止方針。
        """
        if len(self._deprecated_vertical_list_of_backwards_plot_model_pv)==0:
            self._deprecated_vertical_list_of_backwards_plot_model_pv.append(value)
        else:
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
