class PrincipalVariationModel:
    """読み筋モデル"""


    def __init__(self, move_pv, cap_pt_pv, value_pv, backwards_plot_model):
        """
        Parameters
        ----------
        move_pv : int
            シーショーギの指し手。
        cap_pt_pv : int
            取った駒の種類。
        value_pv : int
            評価値。
        backwards_plot_model : BackwardsPlotModel
            後ろ向き探索の読み筋。
        """
        if move_pv:
            self._vertical_move_list_pv = [move_pv]
        else:
            self._vertical_move_list_pv = []

        self._cap_pt_pv = cap_pt_pv
        self._value_pv = value_pv
        self._backwards_plot_model = backwards_plot_model
        self._is_terminate = False


    @property
    def vertical_move_list_pv(self):
        """指し手の履歴。
        """
        return self._vertical_move_list_pv


    @property
    def last_child_move_pv(self):
        """最終の子の指し手。
        """
        return self._vertical_move_list_pv[-1]


    @property
    def value_pv(self):
        """評価値。
        """
        return self._value_pv


    @value_pv.setter
    def value_pv(self, value):
        self._value_pv = value


    @property
    def cap_pt_pv(self):
        """取った駒の種類。
        """
        return self._cap_pt_pv


    @cap_pt_pv.setter
    def cap_pt_pv(self, value):
        self._cap_pt_pv = value


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
