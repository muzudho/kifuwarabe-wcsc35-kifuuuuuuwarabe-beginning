from ..models import Piece


class TableView():
    """盤表示
    """


    _turns = [
        'black',
        'white'
    ]


    def __init__(self, table):
        self._table = table


    @property
    def turn(self):
        """現在の手番を `black` か `white` で出力
        """
        return TableView._turns[self._table.turn]


    def count_repetition(self):
        """TODO 現局面が何回出現したかを数えます
        """

        # 指定局面（現局面）の SFEN を取得（棋譜は付いていない）
        designated_sfen = self._table.sfen()
        print(f"{designated_sfen=}")

        # 盤を複製
        copied_table = self._table.copy_table_with_0_moves()

    #     # 指し手をポップしていく
    #     print(f"{copied_table.move_number=}")
    #     moves_list = []
    #     moves_list.append(copied_table.pop_usi())
    #     print(f"{copied_table.move_number=}")
    #     while 1 < copied_table.move_number:
    #         # copied_table.undo_move_o1o1x() を使うと強制終了する？
    #         moves_list.append(copied_table.undo_move_o1o1x())
    #         print(f"{copied_table.move_number=}")
        
    #     # print(f"{len(moves_list)=}")
    #     # print(f"{moves_list=}")

    #     # # 指していく
    #     # repetition = 0
    #     # for i in reversed(range(0, len(moves_list))):
    #     #     m = moves_list[i]
    #     #     copied_table.do_move_o1o1x(m)

    #     #     # 指定局面の出現回数をカウント
    #     #     if board.sfen() == designated_sfen:
    #     #         repetition += 1

    #     # return repetition


    def stringify(self):

        # 先手、後手の持ち駒の数のリスト
        b = self._table.pieces_in_hand[0]
        w = self._table.pieces_in_hand[1]

        repetition = 0      # self.count_repetition()

        blocks = []
        blocks.append(f"""\
[ next {self._table.move_number} move(s) | {self.turn} | repetition - ]
""")
        blocks.append(f"""\

飛 角 金 銀 桂 香 歩
 {w[6]}  {w[5]}  {w[4]}  {w[3]}  {w[2]}  {w[1]} {w[0]:2}
 -  -  -  -  -  - --

""")

        p = [0] * 81
        for sq in range(0,81):
            p[sq] = Piece.on_board(self._table.piece(sq))

        blocks.append("""\
  9   8   7   6   5   4   3   2   1
+---+---+---+---+---+---+---+---+---+
""")

        blocks.append(f"""\
|{p[72]}|{p[63]}|{p[54]}|{p[45]}|{p[36]}|{p[27]}|{p[18]}|{p[ 9]}|{p[ 0]}| 一
+---+---+---+---+---+---+---+---+---+
|{p[73]}|{p[64]}|{p[55]}|{p[46]}|{p[37]}|{p[28]}|{p[19]}|{p[10]}|{p[ 1]}| 二
+---+---+---+---+---+---+---+---+---+
|{p[74]}|{p[65]}|{p[56]}|{p[47]}|{p[38]}|{p[29]}|{p[20]}|{p[11]}|{p[ 2]}| 三
+---+---+---+---+---+---+---+---+---+
|{p[75]}|{p[66]}|{p[57]}|{p[48]}|{p[39]}|{p[30]}|{p[21]}|{p[12]}|{p[ 3]}| 四
+---+---+---+---+---+---+---+---+---+
|{p[76]}|{p[67]}|{p[58]}|{p[49]}|{p[40]}|{p[31]}|{p[22]}|{p[13]}|{p[ 4]}| 五
+---+---+---+---+---+---+---+---+---+
|{p[77]}|{p[68]}|{p[59]}|{p[50]}|{p[41]}|{p[32]}|{p[23]}|{p[14]}|{p[ 5]}| 六
+---+---+---+---+---+---+---+---+---+
|{p[78]}|{p[69]}|{p[60]}|{p[51]}|{p[42]}|{p[33]}|{p[24]}|{p[15]}|{p[ 6]}| 七
+---+---+---+---+---+---+---+---+---+
|{p[79]}|{p[70]}|{p[61]}|{p[52]}|{p[43]}|{p[34]}|{p[25]}|{p[16]}|{p[ 7]}| 八
+---+---+---+---+---+---+---+---+---+
|{p[80]}|{p[71]}|{p[62]}|{p[53]}|{p[44]}|{p[35]}|{p[26]}|{p[17]}|{p[ 8]}| 九
+---+---+---+---+---+---+---+---+---+

""")

        blocks.append(f"""\
                 飛 角 金 銀 桂 香 歩
                  {b[6]}  {b[5]}  {b[4]}  {b[3]}  {b[2]}  {b[1]} {b[0]:2}
                  -  -  -  -  -  - -- 

""")

        return ''.join(blocks)
