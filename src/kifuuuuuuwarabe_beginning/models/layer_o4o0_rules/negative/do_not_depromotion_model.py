class DoNotDepromotionModel:
    """号令［成らないということをするな］

    TODO 枝前処理で、成る手の一覧を作る。
    TODO 成る手に対応する［成らない手］の一覧を作る。
    TODO ［成らない手］なら除外する。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_depromotion_model',
                label       = '成らないということをするな',
                basketball_court_model  = basketball_court_model)


    def _before_branches_nrm(self, table):
        """枝前に。
        """
        pass
