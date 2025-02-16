import cshogi
import sys

from .. import Mind
from ..sente_perspective import Ban, Helper, Ji


class WillNotToBeCut88Bishop():
    """［８八の角を素抜かれない意志］
    """


    @staticmethod
    def have_will_after_moving_on_board(board):
        """指した後に意志があるか？

        NOTE 指した後は相手の番になっていることに注意
        """
        ban = Ban(board, after_moving=True)
        ji = Ji(board, after_moving=True)

        # ８八に自角がいるケースだけ対称
        if board.piece(ban.masu(88)) != ji.pc(cshogi.BISHOP):
            return Mind.NOT_IN_THIS_CASE

        # ７八に自金が残れば意志あり
        pc = board.piece(ban.masu(78))
        if pc in [ji.pc(cshogi.GOLD)]:
            return Mind.WILL

        # ７九に自金、自銀が残れば意志あり
        pc = board.piece(ban.masu(79))
        if pc in [ji.pc(cshogi.GOLD), ji.pc(cshogi.SILVER)]:
            return Mind.WILL

        # ８段目を７筋から１筋を順に見に行って、最初に見つかった駒が自飛なら意志あり
        for suji in range(1, 8)[::-1]:
            pc = board.piece(ban.masu(suji * 10 + 8))
            if pc == cshogi.NONE:
                continue
            elif pc == ji.pc(cshogi.ROOK):
                return Mind.WILL

        # 意志なし
        return Mind.WILL_NOT
