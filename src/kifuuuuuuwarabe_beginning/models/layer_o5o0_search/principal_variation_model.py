class PrincipalVariationModel:
    """読み筋モデル"""


    def __init__(self, backwards_plot_model):
        self._backwards_plot_model = backwards_plot_model


    @property
    def backwards_plot_model(self):
        return self._backwards_plot_model
