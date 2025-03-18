class PieceValueTAO():
    """駒得の評価値を調べます。
    """


    def __init__(self):
        pass


    def scan_table(self, table):
        print(f'[PieceValueTAO#scan_table] start.')
        pass


    def put_move_usi(self, previous_move_usi, last_move_usi, table):
        """相手の手番でしか呼び出されないので、１つ前の手が自分の手になる。

        Parameters
        ----------
        previous_move_usi : str
            自分の手。無ければナン。
        last_move_usi : str
            相手の手。
        """
        print(f'[PieceValueTAO#put_move_usi] ({table.move_number-2}) friend:{previous_move_usi} ({table.move_number-1}) opponent:{last_move_usi}')
