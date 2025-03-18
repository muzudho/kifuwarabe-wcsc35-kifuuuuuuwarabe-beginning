import cshogi

from ...models import constants, PieceValues


class PieceValueTAO():
    """駒得の評価値を調べます。
    """


    def __init__(self):
        self._nine_rank_side_value = 0


    def nine_rank_side_value(self):
        """９段目に近い方の対局者から見た駒得評価値。
        """
        return self._nine_rank_side_value


    def scan_table(self, table):
        print(f'[PieceValueTAO#scan_table] start.')

        self._nine_rank_side_value = 0

        # 盤上の駒得を数える
        for sq in range(0, constants.BOARD_AREA):
            pc = table.piece(sq)
            self._nine_rank_side_value += PieceValues.by_piece(pc = pc)

        # 駒台の駒得を数える
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.BPAWN     ) * table.pieces_in_hand[0][0]  # ▲歩
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.BLANCE    ) * table.pieces_in_hand[0][1]  # ▲香
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.BKNIGHT   ) * table.pieces_in_hand[0][2]  # ▲桂
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.BSILVER   ) * table.pieces_in_hand[0][3]  # ▲銀
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.BGOLD     ) * table.pieces_in_hand[0][4]  # ▲金
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.BBISHOP   ) * table.pieces_in_hand[0][5]  # ▲角
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.BROOK     ) * table.pieces_in_hand[0][6]  # ▲飛
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.WPAWN     ) * table.pieces_in_hand[1][0]  # ▽歩
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.WLANCE    ) * table.pieces_in_hand[1][1]  # ▽香
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.WKNIGHT   ) * table.pieces_in_hand[1][2]  # ▽桂
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.WSILVER   ) * table.pieces_in_hand[1][3]  # ▽銀
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.WGOLD     ) * table.pieces_in_hand[1][4]  # ▽金
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.WBISHOP   ) * table.pieces_in_hand[1][5]  # ▽角
        self._nine_rank_side_value += PieceValues.by_piece(cshogi.WROOK     ) * table.pieces_in_hand[1][6]  # ▽飛

        # 後手の駒台に歩が１つあれば、盤の上には先手の歩が１枚少ないので、-2 になる。（歩の交換値）
        print(f'[PieceValueTAO#scan_table] {self._nine_rank_side_value=}')


    def put_move_usi_before_move(self, move_as_usi, table):
        """相手の手番でしか呼び出されないので、１つ前の手が自分の手になる。

        Parameters
        ----------
        move_as_usi : str
            指し手。
        """
        print(f'[PieceValueTAO#put_move_usi] ({table.move_number}) {move_as_usi}')
