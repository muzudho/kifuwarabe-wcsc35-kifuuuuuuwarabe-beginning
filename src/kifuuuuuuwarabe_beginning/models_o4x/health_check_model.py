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
                return 'legal'
            return ''


        def _quiescence_search(move_prop):
            if 'quiescence_search' in move_prop:
                return 'quiescence_search'
            return ''


        def _qs_eliminate171(move_prop):
            if 'eliminate171' in move_prop:
                return move_prop['eliminate171']
            return ''


        def _nr_select(move_prop):
            if 'NR_select' in move_prop:
                return 'NR_select'
            return ''


        def _nr_reselect(move_prop):
            if 'NR_reselect' in move_prop:
                return 'NR_reselect'
            return ''


        lines = []

        for move, move_prop in ordered_document:
            # （１）リーガル・ムーブ
            # （２）静止探索で選ばれた手
            # （３）静止探索で選ばれた手をエリミネートした手
            # （４）ネガティブ・ルールで選別した手
            # （５）ロールバックした手
            lines.append(f"{cshogi.move_to_usi(move):5} {_legal(move_prop):6} | {_quiescence_search(move_prop):18} | {_qs_eliminate171(move_prop):30} | {_nr_select(move_prop):10} | {_nr_reselect(move_prop):12} |")

        return '\n'.join(lines)
