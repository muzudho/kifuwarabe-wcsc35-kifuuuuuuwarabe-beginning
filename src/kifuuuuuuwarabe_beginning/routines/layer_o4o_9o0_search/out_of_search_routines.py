from ...models.layer_o1o0 import constants


class OutOfSearchRoutines:
    """探索ルーチンの外側
    """


    def filtering_next_pv_list(terminated_pv_list_1, terminated_pv_list_2, live_pv_list):
        """次のPV一覧を残す。
        """
        next_pv_list = []

        for terminated_pv in terminated_pv_list_1:
            if constants.value.MAYBE_EARTH_WIN_VALUE <= terminated_pv.leafer_value_in_frontward_pv:
                next_pv_list.append(terminated_pv)

        if len(next_pv_list) == 0:
            for terminated_pv in terminated_pv_list_2:
                if constants.value.MAYBE_EARTH_WIN_VALUE <= terminated_pv.leafer_value_in_frontward_pv:
                    next_pv_list.append(terminated_pv)

        if len(next_pv_list) == 0:
            for live_pv in next_pv_list:
                if constants.value.MAYBE_EARTH_WIN_VALUE <= live_pv.leafer_value_in_frontward_pv:
                    next_pv_list.append(live_pv)

        return next_pv_list
