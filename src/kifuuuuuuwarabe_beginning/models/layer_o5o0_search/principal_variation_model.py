class PrincipalVariationModel:
    """読み筋モデル"""


    def __init__(self, move_pv, value_pv, backwards_plot_model):
        """
        Parameters
        ----------
        move_pv : int
            シーショーギの指し手。
        value_pv : int
            評価値。
        backwards_plot_model : BackwardsPlotModel
            後ろ向き探索の読み筋。
        """
        self._move_pv = move_pv
        self._value_pv = value_pv
        self._backwards_plot_model = backwards_plot_model


    @property
    def move_pv(self):
        """指し手。
        """
        return self._move_pv


    @property
    def value_pv(self):
        """評価値。
        """
        return self._value_pv


    @value_pv.setter
    def value_pv(self, value):
        self._value_pv = value


    @property
    def backwards_plot_model(self):
        """後ろ向き探索の読み筋。
        """
        return self._backwards_plot_model


    @backwards_plot_model.setter
    def backwards_plot_model(self, value):
        """後ろ向き探索の読み筋。
        """
        self._backwards_plot_model = value
