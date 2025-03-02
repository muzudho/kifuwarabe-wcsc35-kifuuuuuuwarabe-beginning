class HistoryView():
    """棋譜の表示
    """


    def __init__(self, table):
        self._table = table


    def stringify(self):
        piece_moved_list = self._table.copy_piece_moved_list()

        accumulated_list = [f"""\
HISTORY
-------
      Re:0 {self._table.designated_sfen}"""]

        for piece_moved in piece_moved_list:
            # 指し手
            # TODO 同形反復回数
            # SFEN
            accumulated_list.append(f"{piece_moved.move_as_usi:<5} Re:{piece_moved.number_of_repetition} {piece_moved.sfen_with_0_moves}")

        return '\n'.join(accumulated_list)
