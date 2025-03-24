import cshogi


class HealthCheckModel():
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

        # キーを int 型から str の USI 形式に変換（非破壊的）してから、ソート。
        ordered_document = sorted(self._document.items(), key=lambda entry:cshogi.move_to_usi(entry[0]))


        def _legal(move_prop):
            if 'legal' in move_prop:
                return 'legal '
            return '      '


        def _quiescence_search(move_prop):
            if 'quiescence_search' in move_prop:
                return 'quiescence_search '
            return '                  '


        def _eliminate171(move_prop):
            if 'eliminate171' in move_prop:
                return f"{move_prop['eliminate171']:20}"
            return f"{'':20}"


        def _select(move_prop):
            if 'select' in move_prop:
                return 'select '
            return '       '


        def _reselect(move_prop):
            if 'reselect' in move_prop:
                return 'reselect '
            return '         '


        lines = []

        for move, move_prop in ordered_document:
            # （１）リーガル・ムーブ
            # （２）静止探索で選ばれた手
            # （３）静止探索で選ばれた手をエリミネートした手
            # （４）ネガティブ・ルールで選別した手
            # （５）ロールバックした手
            lines.append(f"{cshogi.move_to_usi(move):5} {_legal(move_prop)} | {_quiescence_search(move_prop)} | {_eliminate171(move_prop)} | {_select(move_prop)} | {_reselect(move_prop)} |")

        return '\n'.join(lines)
