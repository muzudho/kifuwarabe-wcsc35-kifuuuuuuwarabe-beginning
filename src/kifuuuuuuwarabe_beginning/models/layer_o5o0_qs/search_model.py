from ..layer_o2o0 import FrontwardsPlotModel


class SearchModel():


    def __init__(self, max_depth, gymnasium):
        """
        Parameters
        ----------
        max_depth : int
            最大深さ。
        gymnasium : GymnasiumModel
            体育館。        
        """
        self._max_depth = max_depth
        self._gymnasium = gymnasium

        self._number_of_visited_nodes = 0
        self._start_time = None
        self._restart_time = None
        self._end_time = None
        self._move_list_for_debug = FrontwardsPlotModel()  # デバッグ用に手を記憶。


    @property
    def max_depth(self):
        return self._max_depth


    @property
    def gymnasium(self):
        return self._gymnasium


    @property
    def number_of_visited_nodes(self):
        return self._number_of_visited_nodes


    @number_of_visited_nodes.setter
    def number_of_visited_nodes(self, value):
        self._number_of_visited_nodes = value


    @property
    def start_time(self):
        return self._start_time
    

    @start_time.setter
    def start_time(self, value):
        self._start_time = value


    @property
    def restart_time(self):
        return self._restart_time
    

    @restart_time.setter
    def restart_time(self, value):
        self._restart_time = value


    @property
    def end_time(self):
        return self._end_time
    

    @end_time.setter
    def end_time(self, value):
        self._end_time = value


    @property
    def move_list_for_debug(self):
        return self._move_list_for_debug
    

    @move_list_for_debug.setter
    def move_list_for_debug(self, value):
        self._move_list_for_debug = value
