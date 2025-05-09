from ...models.layer_o1o0 import constants


class EndOfSearchRoutines:


    def eliminate_qs_171(pv_list, gymnasium):
        """次の１つの手は、候補に挙げる必要がないので除去します。
        （１）駒を取らない手で非正の手（最高点のケースを除く）。このとき、［零点の手］があるかどうか調べます。
        次の手は、候補に挙げる必要がないので除去します。
        （２）最高点でない手。
        （３）［零点の手」が存在し、かつ、負の手。（リスクヘッジの手でもないから）
        それ以外の手は選択します。

        Returns
        -------
        alice_s_move_list : list(int)
            指し手のリスト。
        """
        alice_s_move_list = []
        exists_zero_value_move = False

        # まず、水平枝の中の最高点を調べます。
        best_exchange_value = constants.value.NOTHING_CAPTURE_MOVE
        for pv in pv_list:
            value_on_earth = pv.leafer_value_in_frontward_pv
            if best_exchange_value < value_on_earth:
                best_exchange_value = value_on_earth

        # 最高点が 0 点のケース。 FIXME 千日手とかを何点に設定しているか？
        if best_exchange_value == 0:
            exists_zero_value_move = True

        for pv in pv_list:

            if pv._leaf_node is None:
                continue

            # ［後ろ向き探索］中の［根に近い方の指し手］
            gymnasium.health_check_go_model.append_health(
                    move    = pv.peek_move_pv,
                    name    = 'QS_principal_variation',
                    value   = pv)

            # （１）駒を取らない手で非正の手（最高点のケースを除く）。
            value_on_earth = pv.leafer_value_in_frontward_pv
            if not pv.is_capture_at_last and value_on_earth < 1 and value_on_earth != best_exchange_value:
                if value_on_earth == 0:
                    exists_zero_value_move = True
                
                gymnasium.health_check_go_model.append_health(
                        move    = pv.peek_move_pv,
                        name    = 'QS_eliminate171',
                        value   = f"{pv.stringify_2():10} not_cap_not_posite")

            # （２）最高点でない手。
            elif value_on_earth < best_exchange_value:
                gymnasium.health_check_go_model.append_health(
                        move    = pv.peek_move_pv,
                        name    = 'QS_eliminate171',
                        value   = f"{pv.stringify_2():10} not_best")

            # （３）リスクヘッジにならない手
            elif exists_zero_value_move and value_on_earth < 0:
                gymnasium.health_check_go_model.append_health(
                        move    = pv.peek_move_pv,
                        name    = 'QS_eliminate171',
                        value   = f"{pv.stringify_2():10} not_risk_hedge")

            # それ以外の手は選択します。
            else:
                alice_s_move_list.append(pv.peek_move_pv)
                gymnasium.health_check_go_model.append_health(
                        move    = pv.peek_move_pv,
                        name    = 'QS_eliminate171',
                        value   = f"{pv.stringify_2():10} ok")

        return alice_s_move_list
