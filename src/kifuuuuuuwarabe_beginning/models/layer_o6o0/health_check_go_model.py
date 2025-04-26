import cshogi


class HealthCheckGoModel():
    """go コマンドの健康診断。
    """


    def __init__(self, gymnasium):
        """初期化。
        """
        self._gymnasium = gymnasium
        self._document = {}


    def on_go_started(self):
        pass
    

    def on_go_finished(self):
        pass


    def append_health(self, move, name, value):
        if move not in self._document:
            self._document[move] = {}
        
        self._document[move][name] = value


    def stringify(self):

        # インデックス・アクセスしたいので、リストに変換。
        # キーを int 型から str の USI 形式に変換（非破壊的）してから、ソート。
        health_list = sorted(self._document.items(), key=lambda entry:cshogi.move_to_usi(entry[0]))


        def fn_move(i):
            move = health_list[i][0]
            return f"{cshogi.move_to_usi(move)}"


        def fn_legal(i):
            move_prop = health_list[i][1]
            if 'legal' in move_prop:
                return 'legal'
            return ''
        

        def fn_eater(i):
            move_prop = health_list[i][1]
            if 'SQ_eater' in move_prop:
                return f"{move_prop['SQ_eater']}"
            return ''


        # def fn_qs_cheapest(i):
        #     move_prop = health_list[i][1]
        #     if 'QS_cheapest' in move_prop:
        #         return 'QS_cheapest'
        #     return ''


        def fn_qs_eliminate171(i):
            move_prop = health_list[i][1]
            if 'QS_eliminate171' in move_prop:
                return f"{move_prop['QS_eliminate171']}"
            return ''


        def fn_qs_select(i):
            move_prop = health_list[i][1]
            if 'QS_select' in move_prop:
                return f"{move_prop['QS_select']}"
            return ''


        def fn_negative_rule(i, rule_id):
            move_prop = health_list[i][1]
            prop_name = f"NR[{rule_id}]"
            if prop_name in move_prop:
                return f"{move_prop[prop_name]}"
            return ''


        def fn_pr_nr_remaining(i):
            move_prop = health_list[i][1]

            if 'PR_remaining' in move_prop:
                return f"{move_prop['PR_remaining']}"

            if 'NR_remaining' in move_prop:
                return f"{move_prop['NR_remaining']}"

            return ''
        

        def fn_bm_bestmove(i):
            move_prop = health_list[i][1]
            if 'BM_bestmove' in move_prop:
                return 'BM_bestmove'
            return ''


        def fn_qs_plot(i):
            move_prop = health_list[i][1]
            if 'QS_backwards_plot_model' in move_prop:
                return f"{move_prop['QS_backwards_plot_model'].stringify()}"
            return ''


        lines = []

        lines.append(f"* {self._gymnasium.config_doc['search']['capture_depth']} 手読み")
        lines.append('')
        lines.append('HEALTH CHECK GO WORKSHEET')
        lines.append('-------------------------')

        header_list = []
        header_list.append('move')
        header_list.append('legal')
        header_list.append('eater')
        # header_list.append('QS_cheapest')
        header_list.append('qs_plot')
        header_list.append('qs_eliminate171')
        header_list.append('qs_select')

        # 号令リスト
        for negative_rule in self._gymnasium.gourei_collection_model.negative_rule_list_of_active:
            header_list.append(f"NR[{negative_rule.label}]")    # 日本語表示

        header_list.append('PR_NR_remaining')
        header_list.append('bm_bestmove')
        lines.append(', '.join(header_list))
        

        for i in range(0, len(health_list)):
            body_list = []
            body_list.append(fn_move(i))                # USI書式の指し手
            body_list.append(fn_legal(i))               # リーガル・ムーブ
            body_list.append(fn_eater(i))
            # body_list.append(fn_qs_cheapest(i))         # 一番安い駒を選ぶ。
            body_list.append(fn_qs_plot(i))             # 静止探索の読み筋の詳細
            body_list.append(fn_qs_eliminate171(i))     # 静止探索で選ばれた手をエリミネートした手
            body_list.append(fn_qs_select(i))           # 静止探索で選ばれた手

            # 号令リスト
            for negative_rule in self._gymnasium.gourei_collection_model.negative_rule_list_of_active:
                body_list.append(fn_negative_rule(i, negative_rule.id))

            body_list.append(fn_pr_nr_remaining(i))        # ネガティブ・ルールで選別して残った手
            body_list.append(fn_bm_bestmove(i))         # ベストムーブ
            lines.append(', '.join(body_list))

        return '\n'.join(lines)
