class SelectCheapEatersModel():


    def __init__(self, cheapest_eat_move_list):
        self._cheapest_eat_move_list = cheapest_eat_move_list


    @property
    def cheapest_eat_move_list(self):
        return self._cheapest_eat_move_list
