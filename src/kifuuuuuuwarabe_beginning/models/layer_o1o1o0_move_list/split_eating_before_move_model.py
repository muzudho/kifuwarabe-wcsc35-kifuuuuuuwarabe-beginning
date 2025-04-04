class SplitEatingBeforeMoveModel():


    def __init__(self, move_not_eat_list, move_eat_list, cap_list):
        self._move_not_eat_list = move_not_eat_list
        self._move_eat_list = move_eat_list
        self._cap_list = cap_list


    @property
    def move_not_eat_list(self):
        """駒を取らない手リスト
        """
        return self._move_not_eat_list


    @property
    def move_eat_list(self):
        """駒を取る手リスト
        """
        return self._move_eat_list


    @property
    def cap_list(self):
        """取った駒リスト
        """
        return self._cap_list
