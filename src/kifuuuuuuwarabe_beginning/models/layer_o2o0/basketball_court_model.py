class BasketballCourtModel():
    """バスケットボール・コート。
    
    - 体育館の中にある。
    - ネガティブ・ルールから参照される。
    """


    def __init__(self, config_doc):
        """初期化。
        """
        self._config_doc = config_doc


    @property
    def config_doc(self):
        """［設定］
        """
        return self._config_doc
