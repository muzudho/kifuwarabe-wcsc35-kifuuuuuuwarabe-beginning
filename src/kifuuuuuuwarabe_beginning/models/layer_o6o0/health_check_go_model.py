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


    def append(self, move, name, value):
        if move not in self._document:
            self._document[move] = {}
        
        self._document[move][name] = value


    def stringify(self):

        # インデックス・アクセスしたいので、リストに変換。
        # キーを int 型から str の USI 形式に変換（非破壊的）してから、ソート。
        health_list = sorted(self._document.items(), key=lambda entry:cshogi.move_to_usi(entry[0]))


        def fn_move(i):
            move = health_list[i][0]
            return f"{cshogi.move_to_usi(move):5}"


        def fn_legal(i):
            move_prop = health_list[i][1]
            if 'legal' in move_prop:
                return f"{'legal':5}"
            return f"{'':5}"
        

        def fn_eater(i):
            move_prop = health_list[i][1]
            if 'SQ_eater' in move_prop:
                return f"{move_prop['SQ_eater']:12}"
            return f"{'':12}"


        def fn_cheapest(i):
            move_prop = health_list[i][1]
            if 'cheapest' in move_prop:
                return f"{move_prop['cheapest']:12}"
            return f"{'':12}"


        def fn_qs_eliminate171(i):
            move_prop = health_list[i][1]
            if 'eliminate171' in move_prop:
                return f"{move_prop['eliminate171']:30}"
            return f"{'':30}"


        def fn_qs_select(i):
            move_prop = health_list[i][1]
            if 'QS_select' in move_prop:
                return f"{move_prop['QS_select']:9}"
            return f"{'':9}"


        def fn_negative_rule(i, rule_id):
            move_prop = health_list[i][1]
            prop_name = f"NR[{rule_id}]"
            if prop_name in move_prop:
                return f"{move_prop[prop_name]}"
            return ''


        def fn_nr_remaining(i):
            move_prop = health_list[i][1]
            if 'NR_remaining' in move_prop:
                return f"{move_prop['NR_remaining']:12}"
            return f"{'':12}"
        

        def fn_bm_bestmove(i):
            move_prop = health_list[i][1]
            if 'BM_bestmove' in move_prop:
                return f"{'BM_bestmove':11}"
            return f"{'':11}"


        def fn_qs_plot(i):
            move_prop = health_list[i][1]
            if 'QS_backwards_plot_model' in move_prop:
                return move_prop['QS_backwards_plot_model'].stringify()
            return ''


        lines = []

        lines.append(f"* {self._gymnasium.config_doc['search']['capture_depth']} 手読み")
        lines.append('')
        lines.append('HEALTH CHECK GO WORKSHEET')
        lines.append('-------------------------')

        header_list = []
        header_list.append(f"{'move':5}")
        header_list.append(f"{'legal':5}")
        header_list.append(f"{'eater':12}")
        header_list.append(f"{'cheapest':12}")
        header_list.append(f"{'qs_eliminate171':30}")
        header_list.append(f"{'qs_select':9}")

        # 号令リスト
        for negative_rule in self._gymnasium.gourei_collection_model.negative_rule_list_of_active:
            header_list.append(f"NR[{negative_rule.label}]")    # 日本語表示

        header_list.append(f"{'nr_remaining':12}")
        header_list.append(f"{'bm_bestmove':11}")
        header_list.append('qs_plot')
        lines.append(', '.join(header_list))
        

        for i in range(0, len(health_list)):
            body_list = []
            body_list.append(fn_move(i))                # USI書式の指し手
            body_list.append(fn_legal(i))               # リーガル・ムーブ
            body_list.append(fn_eater(i))
            body_list.append(fn_cheapest(i))
            body_list.append(fn_qs_eliminate171(i))     # 静止探索で選ばれた手をエリミネートした手
            body_list.append(fn_qs_select(i))           # 静止探索で選ばれた手

            # 号令リスト
            for negative_rule in self._gymnasium.gourei_collection_model.negative_rule_list_of_active:
                body_list.append(fn_negative_rule(i, negative_rule.id))

            body_list.append(fn_nr_remaining(i))        # ネガティブ・ルールで選別して残った手
            body_list.append(fn_bm_bestmove(i))         # ベストムーブ
            body_list.append(fn_qs_plot(i))             # 静止探索の読み筋の詳細
            lines.append(', '.join(body_list))

        return '\n'.join(lines)
