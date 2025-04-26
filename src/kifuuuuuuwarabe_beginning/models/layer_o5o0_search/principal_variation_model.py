class PrincipalVariationModel:
    """読み筋モデル"""


    def __init__(self, value_pv, backwards_plot_model):
        """
        Parameters
        ----------
        value_pv : int
            評価値。
        backwards_plot_model : BackwardsPlotModel
            後ろ向き探索の読み筋。
        """
        self._value_pv = value_pv
        self._backwards_plot_model = backwards_plot_model


    @property
    def value_pv(self):
        """評価値。
        """
        return self._value_pv


    @property
    def backwards_plot_model(self):
        """後ろ向き探索の読み筋。
        """
        return self._backwards_plot_model
