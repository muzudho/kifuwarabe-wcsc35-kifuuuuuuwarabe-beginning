class RuleModel:


    def __init__(self, id, label, basketball_court_model):
        """初期化。

        Parameters
        ----------
        id : str
            識別子。設定ファイルなどで利用する名前。
        label : str
            名前。人に読めるテキスト。
        """
        self._id = id
        self._label = label
        self._basketball_court_model = basketball_court_model

        self._is_activate = False
        self._is_removed = False


    @property
    def id(self):
        """識別子。
        設定ファイルなどで利用する名前。
        """
        return self._id


    @property
    def label(self):
        """名前。
        人に読めるテキスト。
        """
        return self._label


    @property
    def is_enabled(self):
        """設定ファイルで使用が許可されているか。
        記述が無ければ偽扱い。
        """
        if self._id not in self._basketball_court_model.config_doc['gourei_commands']:
            return False
        return self._basketball_court_model.config_doc['gourei_commands'][self._id]


    @property
    def is_activate(self):
        """［アイドリング］状態にある［号令］が、
        ［オンゴーイング］状態に遷移するためのフラグです。
        """
        return self._is_activate


    @property
    def is_removed(self):
        """このルールを消すか。
        """
        return self._is_removed
