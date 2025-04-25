class SearchAlgorithmModel:
    """検索アルゴリズム。
    """


    def __init__(self, search_context_model):
        """
        Parameters
        ----------
        search_context_model : SearchContextModel
            探索モデル。
        """
        self._search_context_model = search_context_model
