import cshogi
import sys

from ..models import constants
from ..sente_perspective import Ban, Helper, Ji
from .match_operation import MatchOperation


class WillNotToBeCut88Bishop(MatchOperation):
    """［８八の角を素抜かれない］意志
    """


    def __init__(self):
        super().__init__()
        self._id = 'will_not_to_be_cut_88_bishop'
        self._label = '８八の角を素抜かれない'


    def do_anything(self, will_play_moves, table, config_doc):
        # １手指してから判定
        for i in range(len(will_play_moves))[::-1]:     # `[::-1]` - 逆順
            m = will_play_moves[i]
            table.push(m)   # １手指す

            # ［８八の角を素抜かれない］意志
            if config_doc['march_operations'][self._id]:
                mind = self.have_will_after_moving_on_board(table)
                if mind == constants.mind.WILL_NOT:
                    del will_play_moves[i]

            table.pop() # １手戻す

        return will_play_moves


    def have_will_after_moving_on_board(self, table):
        """指した後に意志があるか？        
        """
        # NOTE 指した後は相手の番になっていることに注意
        ban = Ban(table, after_moving=True)
        ji = Ji(table, after_moving=True)

        # ８八に自角がいるケースだけ対称
        if table.piece(ban.masu(88)) != ji.pc(cshogi.BISHOP):
            return constants.mind.NOT_IN_THIS_CASE

        # ７八に自金が残れば意志あり
        pc = table.piece(ban.masu(78))
        if pc in [ji.pc(cshogi.GOLD)]:
            return constants.mind.WILL

        # ７九に自金、自銀が残れば意志あり
        pc = table.piece(ban.masu(79))
        if pc in [ji.pc(cshogi.GOLD), ji.pc(cshogi.SILVER)]:
            return constants.mind.WILL

        # ８段目を７筋から１筋を順に見に行って、最初に見つかった駒が自飛なら意志あり
        for file in ban.suji_range(1, 8)[::-1]:
            pc = table.piece(Helper.file_rank_to_sq(file, ban.dan(8)))
            if pc == cshogi.NONE:
                continue
            elif pc == ji.pc(cshogi.ROOK):
                return constants.mind.WILL

        # 意志なし
        return constants.mind.WILL_NOT
