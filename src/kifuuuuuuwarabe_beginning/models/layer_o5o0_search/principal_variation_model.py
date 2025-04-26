class PrincipalVariationModel:
    """読み筋モデル"""


    def __init__(self, vertical_list_of_move_pv, vertical_list_of_cap_pt_pv, value_pv, backwards_plot_model, is_terminate=False):
        """
        Parameters
        ----------
        vertical_list_of_move_pv : list<int>
            シーショーギの指し手のリスト。
        vertical_list_of_cap_pt_pv : list<int>
            取った駒の種類のリスト。
        value_pv : int
            評価値。
        backwards_plot_model : BackwardsPlotModel
            後ろ向き探索の読み筋。
        """
        self._vertical_list_of_move_pv = vertical_list_of_move_pv
        self._vertical_list_of_cap_pt_pv = vertical_list_of_cap_pt_pv
        self._value_pv = value_pv
        self._backwards_plot_model = backwards_plot_model
        self._is_terminate = is_terminate


    @property
    def vertical_list_of_move_pv(self):
        """指し手の履歴。
        """
        return self._vertical_list_of_move_pv


    @property
    def last_child_move_pv(self):
        """最終の子の指し手。
        """
        return self._vertical_list_of_move_pv[-1]


    @property
    def value_pv(self):
        """評価値。
        """
        return self._value_pv


    @value_pv.setter
    def value_pv(self, value):
        self._value_pv = value


    @property
    def vertical_list_of_cap_pt_pv(self):
        """取った駒の種類のリスト。
        """
        return self._vertical_list_of_cap_pt_pv


    @property
    def backwards_plot_model(self):
        """後ろ向き探索の読み筋。
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


    def pop_vertical_list_of_move_pv(self):
        """指し手の履歴をポップします。
        """
        work = list(self._vertical_list_of_move_pv)
        self._vertical_list_of_move_pv = []
        return work


    def copy_pv(self):
        return PrincipalVariationModel(
                vertical_list_of_move_pv    = self._vertical_list_of_move_pv,
                vertical_list_of_cap_pt_pv  = self._vertical_list_of_cap_pt_pv,
                value_pv                    = self._value_pv,
                backwards_plot_model        = self._backwards_plot_model,
                is_terminate                = self._is_terminate)


    def new_and_append(self, move_pv, cap_pt_pv, value_pv, replace_backwards_plot_model, replace_is_terminate):
        vertical_list_of_move_pv = list(self._vertical_list_of_cap_pt_pv)
        vertical_list_of_move_pv.append(move_pv)
        vertical_list_of_cap_pt_pv = list(self._vertical_list_of_cap_pt_pv)
        vertical_list_of_cap_pt_pv.append(cap_pt_pv)

        return PrincipalVariationModel(
                vertical_list_of_move_pv    = vertical_list_of_move_pv,
                vertical_list_of_cap_pt_pv  = vertical_list_of_cap_pt_pv,
                value_pv                    = self._value_pv + value_pv,
                backwards_plot_model        = replace_backwards_plot_model,
                is_terminate                = replace_is_terminate)
