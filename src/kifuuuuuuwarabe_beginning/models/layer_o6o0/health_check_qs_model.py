class HealthCheckQsItemModel:


    def __init__(self, nodes=[]):
        self._nodes = nodes


    def append_node(self, text):
        self._nodes.append(text)
    

    def pop_node(self):
        self._nodes.pop()


    def copy(self):
        return HealthCheckQsItemModel(
                nodes=list(self._nodes))


    def stringify(self):
        tokens = []

        for node in self._nodes:
            tokens.append(node)
        
        return ', '.join(tokens)


class HealthCheckQsModel:
    """健康診断モデル。静止探索用。

    木構造をどうログに取るか？
    """


    def __init__(self, gymnasium):
        """初期化。
        """
        self._gymnasium = gymnasium
        self._enabled = False


    @property
    def enabled(self):
        return self._enabled


    def start_monitor(self):
        self._current_item = HealthCheckQsItemModel()
        self._item_list = []
        self._enabled = True


    def end_monitor(self):
        self._current_item = None
        self._item_list = None
        self._enabled = False


    def append_node(self, text):
        if not self._enabled:
            return
        
        self._current_item.append_node(text)
        self._item_list.append(self._current_item.copy())   # 単調増加していく。


    def pop_node(self):
        if not self._enabled:
            return

        self._current_item.pop_node()


    def stringify(self):
        if not self._enabled:
            return ''

        lines = []
        lines.append('HEALTH CHECK QS WORKSHEET')
        lines.append('-------------------------')

        for item in self._item_list:
            lines.append(item.stringify())

        return '\n'.join(lines)
