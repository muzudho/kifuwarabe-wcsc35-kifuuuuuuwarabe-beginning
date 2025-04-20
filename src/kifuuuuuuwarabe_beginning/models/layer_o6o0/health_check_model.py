import cshogi


class HealthCheckModel():
    """健康診断。
    """


    def __init__(self, config_doc):
        """初期化。
        """
        self._config_doc = config_doc
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


        def _eater(move_prop):
            if 'SQ_eater' in move_prop:
                return move_prop['SQ_eater']
            return ''


        def _cheapest(move_prop):
            if 'cheapest' in move_prop:
                return move_prop['cheapest']
            return ''


        def _qs_eliminate171(move_prop):
            if 'eliminate171' in move_prop:
                return move_prop['eliminate171']
            return ''


        def _qs_select(move_prop):
            if 'QS_select' in move_prop:
                return move_prop['QS_select']
            return ''


        def _nr_remaining(move_prop):
            if 'NR_remaining' in move_prop:
                return move_prop['NR_remaining']
            return ''


        def _bm_bestmove(move_prop):
            if 'BM_bestmove' in move_prop:
                return 'BM_bestmove'
            return ''


        def _qs_plot(move_prop):
            if 'QS_backwards_plot_model' in move_prop:
                return move_prop['QS_backwards_plot_model'].stringify()
            return ''


        lines = []

        lines.append(f"* {self._config_doc['search']['capture_depth']} 手読み")
        lines.append('')
        lines.append('HEALTH CHECK WORKSHEET')
        lines.append('----------------------')

        header_list = []
        header_list.append(f"{'move':5}")
        header_list.append(f"{'legal':5}")
        header_list.append(f"{'eater':12}")
        header_list.append(f"{'cheapest':12}")
        header_list.append(f"{'qs_eliminate171':30}")
        header_list.append(f"{'qs_select':9}")
        header_list.append(f"{'nr_remaining':12}")
        header_list.append(f"{'bm_bestmove':11}")
        header_list.append('qs_plot')
        lines.append(', '.join(header_list))

        for move, move_prop in ordered_document:
            # （１）リーガル・ムーブ
            # （２）静止探索で選ばれた手
            # （３）静止探索で選ばれた手をエリミネートした手
            # （４）ネガティブ・ルールで選別した手
            # （５）ロールバックした手
            body_list = []
            body_list.append(f"{cshogi.move_to_usi(move):5}")
            body_list.append(f"{_legal(move_prop):5}")
            body_list.append(f"{_eater(move_prop):12}")
            body_list.append(f"{_cheapest(move_prop):12}")
            body_list.append(f"{_qs_eliminate171(move_prop):30}")
            body_list.append(f"{_qs_select(move_prop):9}")
            body_list.append(f"{_nr_remaining(move_prop):12}")
            body_list.append(f"{_bm_bestmove(move_prop):11}")
            body_list.append(f"{_qs_plot(move_prop)}")
            lines.append(', '.join(body_list))

        return '\n'.join(lines)
