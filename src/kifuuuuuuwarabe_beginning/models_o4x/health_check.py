import cshogi


class HealthCheck():
    """健康診断。
    """


    def __init__(self):
        """初期化。
        """
        self._document = {}


    def on_go_started(self):
        pass
    

    def on_go_finished(self):
        pass


    def append(self, move, name, value):
        if move not in self._document:
            self._document[move] = {}
        
        self._document[move][name] = value


    def stringify(self):

        def _legal(move_prop):
            if 'legal' in move_prop:
                return 'legal '
            return '      '

        lines = []

        for move, move_prop in self._document.items():
            lines.append(f"{cshogi.move_to_usi(move):5} {_legal(move_prop)}")

        return '\n'.join(lines)