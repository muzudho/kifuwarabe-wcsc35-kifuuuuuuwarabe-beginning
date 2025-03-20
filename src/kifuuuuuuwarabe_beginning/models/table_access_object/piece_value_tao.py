import cshogi

from ...models import constants, PieceValues


class PieceValueTAO():
    """駒得の評価値を調べます。
    """


    def __init__(self, table):
        self._table = table


    def scan_table(self):
        print(f'[PieceValueTAO#scan_table] start.')

        nine_rank_side_value = 0

        # 盤上の駒得を数える
        for sq in range(0, constants.BOARD_AREA):
            pc = self._table.piece(sq)
            nine_rank_side_value += PieceValues.by_piece(pc = pc)

        # 駒台の駒得を数える
        nine_rank_side_value += PieceValues.by_piece(cshogi.BPAWN     ) * self._table.pieces_in_hand[0][0]  # ▲歩
        nine_rank_side_value += PieceValues.by_piece(cshogi.BLANCE    ) * self._table.pieces_in_hand[0][1]  # ▲香
        nine_rank_side_value += PieceValues.by_piece(cshogi.BKNIGHT   ) * self._table.pieces_in_hand[0][2]  # ▲桂
        nine_rank_side_value += PieceValues.by_piece(cshogi.BSILVER   ) * self._table.pieces_in_hand[0][3]  # ▲銀
        nine_rank_side_value += PieceValues.by_piece(cshogi.BGOLD     ) * self._table.pieces_in_hand[0][4]  # ▲金
        nine_rank_side_value += PieceValues.by_piece(cshogi.BBISHOP   ) * self._table.pieces_in_hand[0][5]  # ▲角
        nine_rank_side_value += PieceValues.by_piece(cshogi.BROOK     ) * self._table.pieces_in_hand[0][6]  # ▲飛
        nine_rank_side_value += PieceValues.by_piece(cshogi.WPAWN     ) * self._table.pieces_in_hand[1][0]  # ▽歩
        nine_rank_side_value += PieceValues.by_piece(cshogi.WLANCE    ) * self._table.pieces_in_hand[1][1]  # ▽香
        nine_rank_side_value += PieceValues.by_piece(cshogi.WKNIGHT   ) * self._table.pieces_in_hand[1][2]  # ▽桂
        nine_rank_side_value += PieceValues.by_piece(cshogi.WSILVER   ) * self._table.pieces_in_hand[1][3]  # ▽銀
        nine_rank_side_value += PieceValues.by_piece(cshogi.WGOLD     ) * self._table.pieces_in_hand[1][4]  # ▽金
        nine_rank_side_value += PieceValues.by_piece(cshogi.WBISHOP   ) * self._table.pieces_in_hand[1][5]  # ▽角
        nine_rank_side_value += PieceValues.by_piece(cshogi.WROOK     ) * self._table.pieces_in_hand[1][6]  # ▽飛

        # 後手の駒台に歩が１つあれば、盤の上には先手の歩が１枚少ないので、-2 になる。（歩の交換値）
        print(f'[PieceValueTAO#scan_table] {nine_rank_side_value=}')

        return nine_rank_side_value


    def before_move(self, move):
        """相手の手番でしか呼び出されないので、１つ前の手が自分の手になる。

        Parameters
        ----------
        move : int
            ［指し手］
        """

        # 移動先にある駒を見る。
        dst_sq = cshogi.move_to(move)
        dst_pc = self._table.piece(dst_sq)
        nine_rank_side_value = 2 * - PieceValues.by_piece(dst_pc)  # 相手の駒を取るのでマイナスにします。交換値なので２倍します。

        return nine_rank_side_value




    def before_undo_move(self, move):
        """相手の手番でしか呼び出されないので、１つ前の手が自分の手になる。

        Parameters
        ----------
        move : int
            ［指し手］
        """

        # 取ったを見る。
        pc = cshogi.move_cap(move)
        nine_rank_side_value = 2 * - PieceValues.by_piece(pc)  # 相手の駒を取るのでマイナスにします。交換値なので２倍します。

        return - nine_rank_side_value   # アンドゥなのでマイナス
