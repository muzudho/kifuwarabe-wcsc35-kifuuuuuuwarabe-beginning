class TerminationModel:
    """［終端外］オブジェクト。
    """

    def __init__(
            self,
            is_mars_arg,
            is_gote_arg,
            state_arg,
            comment_arg):
        self._is_mars_tm    = is_mars_arg
        self._is_gote_tm    = is_gote_arg
        self._state_tm      = state_arg
        self._comment_tm    = comment_arg


    @property
    def is_mars_tm(self):
        """［火星］。
        """
        return self._is_mars_tm


    @property
    def is_gote_tm(self):
        """［後手］。
        """
        return self._is_gote_tm


    @property
    def state_tm(self):
        """［状態］。
        """
        return self._state_tm


    @property
    def comment_tm(self):
        """［コメント］。
        """
        return self._comment_tm


    def copy_termination_model(self):
        """複製。
        """
        return TerminationModel(
                is_mars_arg = self._is_mars_tm,
                is_gote_arg = self._is_gote_tm,
                state_arg   = self._state_tm,
                comment_arg = self._comment_tm)
