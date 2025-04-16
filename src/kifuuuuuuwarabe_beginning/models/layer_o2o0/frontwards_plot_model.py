import cshogi


class FrontwardsPlotModel(): # TODO Rename PathFromRoot


    def __init__(self):
        self._move_list = []


    def append_move(self, move):
        self._move_list.append(move)


    def pop_move(self):
        self._move_list.pop()


    def equals_move_usi_list(self, move_usi_list):
        usi_list = []
        for move in self._move_list:
            usi_list.append(cshogi.move_to_usi(move))

        return usi_list == move_usi_list


    def stringify(self):
        tokens = []
        for move in self._move_list:
            tokens.append(cshogi.move_to_usi(move))
        
        return ','.join(tokens)
