class PieceValueTAO():
    """駒得の評価値を調べます。
    """


    def __init__(self):
        pass


    def scan_table(self, table):
        print(f'[PieceValueTAO#scan_table] start.')
        pass


    def put_move_usi_before_move(self, move_as_usi, table):
        """相手の手番でしか呼び出されないので、１つ前の手が自分の手になる。

        Parameters
        ----------
        move_as_usi : str
            指し手。
        """
        print(f'[PieceValueTAO#put_move_usi] ({table.move_number}) {move_as_usi}')
