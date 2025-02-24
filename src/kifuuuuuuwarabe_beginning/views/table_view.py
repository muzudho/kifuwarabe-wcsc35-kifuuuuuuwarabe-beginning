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


    # def count_repetition(self):
    #     """現局面が何回出現したかを数えます
    #     """

    #     # 指定局面（現局面）の SFEN を取得
    #     # sfen() は 棋譜が付いていない
    #     designated_sfen = self._table.sfen()
    #     print(f"{designated_sfen=}")

    #     # 盤を複製
    #     copied_board = self._table.copy()
    #     print(f"{copied_board=}")

    #     # 指し手をポップしていく
    #     print(f"{copied_board.move_number=}")
    #     moves_list = []
    #     moves_list.append(copied_board.pop_usi())
    #     print(f"{copied_board.move_number=}")
    #     while 1 < copied_board.move_number:
    #         # copied_board.pop() を使うと強制終了する？
    #         moves_list.append(copied_board.pop())
    #         print(f"{copied_board.move_number=}")
        
    #     # print(f"{len(moves_list)=}")
    #     # print(f"{moves_list=}")

    #     # # 指していく
    #     # repetition = 0
    #     # for i in reversed(range(0, len(moves_list))):
    #     #     m = moves_list[i]
    #     #     copied_board.push(m)

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
[ next {self._table.move_number} move(s) | {self.turn} | repetition {repetition} ]
""")
        blocks.append(f"""\

飛 角 金 銀 桂 香 歩
 {w[6]}  {w[5]}  {w[4]}  {w[3]}  {w[2]}  {w[1]} {w[0]:2}
 -  -  -  -  -  - --

""")
        blocks.append(f"""\
  9   8   7   6   5   4   3   2   1
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 一
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 二
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 三
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 四
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 五
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 六
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 七
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 八
+---+---+---+---+---+---+---+---+---+
|   |   |   |   |   |   |   |   |   | 九
+---+---+---+---+---+---+---+---+---+

""")
        blocks.append(f"""\
                 飛 角 金 銀 桂 香 歩
                  {b[6]}  {b[5]}  {b[4]}  {b[3]}  {b[2]}  {b[1]} {b[0]:2}
                  -  -  -  -  -  - -- 

""")
        return ''.join(blocks)
