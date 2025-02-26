class HistoryView():
    """棋譜の表示
    """


    def __init__(self, table):
        self._table = table


    def stringify(self):
        move_list_as_usi = self._table.copy_move_list_as_usi()

        accumulated_list = []
        for move_as_usi in move_list_as_usi:
            accumulated_list.append(move_as_usi)

        return '\n'.join(accumulated_list)
