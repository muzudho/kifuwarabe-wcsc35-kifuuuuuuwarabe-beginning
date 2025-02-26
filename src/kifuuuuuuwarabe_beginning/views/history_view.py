class HistoryView():
    """棋譜の表示
    """


    def __init__(self, table):
        self._table = table


    def stringify(self):
        piece_moved_list = self._table.copy_piece_moved_list()

        accumulated_list = ["""\
HISTORY
-------"""]
        for piece_moved in piece_moved_list:
            accumulated_list.append(f"{piece_moved.move_as_usi:<5} {piece_moved.sfen_with_0_moves}")

        return '\n'.join(accumulated_list)
