import cshogi


class HealthCheckQsItemModel:
    """健康診断モデル。
    """


    def __init__(self, vertical_edges_move=[], vertical_edges_comment=[]):
        self._vertical_edges_move = vertical_edges_move     # 指し手
        self._vertical_edges_comment = vertical_edges_comment     # 指し手へのコメント


    def append_edge(self, move, comment):
        self._vertical_edges_move.append(move)
        self._vertical_edges_comment.append(comment)
    

    def pop_node(self):
        self._vertical_edges_move.pop()
        self._vertical_edges_comment.pop()


    def copy(self):
        return HealthCheckQsItemModel(
                vertical_edges_move=list(self._vertical_edges_move),
                vertical_edges_comment=list(self._vertical_edges_comment))


    def stringify(self):
        tokens = []

        for i in range(0, len(self._vertical_edges_move)):
            move = self._vertical_edges_move[i]
            comment = self._vertical_edges_comment[i]


            def _move():
                if move:
                    return cshogi.move_to_usi(move)
                return ''


            def _comment():
                if comment != '':
                    return f" {comment}"
                return ''


            tokens.append(f"{_move()}{_comment()}")
        
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


    def append_edge_qs(self, move, comment):
        if not self._enabled:
            return
        
        self._current_item.append_edge(move=move, comment=comment)


    def on_out_of_termination(self, text):
        """探索の［終端外］時。
        """
        if not self._enabled:
            return

        self._current_item.append_edge(move=None, comment=text)
        self._item_list.append(self._current_item.copy())   # 単調増加していく。
        self._current_item.pop_node()


    def pop_node_qs(self):
        if not self._enabled:
            return

        self._current_item.pop_node()


    def stringify(self):
        if not self._enabled:
            return ''

        lines = []
        lines.append('HEALTH CHECK QS WORKSHEET')
        lines.append('-------------------------')

        for i in range(0, len(self._item_list)):
            item = self._item_list[i]
            lines.append(f"({i}) {item.stringify()}")

        return '\n'.join(lines)
