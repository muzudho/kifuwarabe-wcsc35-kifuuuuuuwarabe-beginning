class SearchContextModel():


    def __init__(self, max_depth_qs, gymnasium):
        """
        Parameters
        ----------
        max_depth_qs : int
            最大深さ。
        gymnasium : GymnasiumModel
            体育館。        
        """
        self._max_depth_qs     = max_depth_qs
        self._gymnasium     = gymnasium
        self._number_of_visited_nodes = 0
        self._start_time    = None
        self._restart_time  = None
        self._end_time      = None
        self.clear_root_searched_control_map()


    @property
    def max_depth_qs(self):
        return self._max_depth_qs


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


    def clear_root_searched_control_map(self):
        """利きの早見表をクリアー。
        """
        self._root_searched_control_map = [False] * 81


    def set_root_searched_control_map(self, sq, value):
        self._root_searched_control_map[sq] = value


    def get_root_searched_control_map(self, sq):
        return self._root_searched_control_map[sq]
