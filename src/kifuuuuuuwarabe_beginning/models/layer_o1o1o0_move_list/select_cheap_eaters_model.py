class SelectCheapEatersModel():


    def __init__(self, move_group_by_dst_sq, cheapest_eat_move_list):
        self._move_group_by_dst_sq      = move_group_by_dst_sq
        self._cheapest_eat_move_list    = cheapest_eat_move_list


    @property
    def move_group_by_dst_sq(self):
        return self._move_group_by_dst_sq


    @property
    def cheapest_eat_move_list(self):
        return self._cheapest_eat_move_list
