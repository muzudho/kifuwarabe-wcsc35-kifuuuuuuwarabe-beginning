import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o1o0o_9o0_table_helper import TableHelper
from ..negative_rule_model import NegativeRuleModel


class DoNotBackModel(NegativeRuleModel):
    """号令［戻るな］
    ［手待ちをしない］意志

    FIXME 駒が取られそうなときは、戻りたい。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_back',
                label       = '戻るな',
                basketball_court_model  = basketball_court_model)

        #print(f'★ ＤoNotBack: back_board 生成')
        # 元の位置。該当がなければナンです。
        # NOTE 自分が指し手を送信した手しか記憶していません。
        self._back_board = [None] * constants.BOARD_AREA


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """

        is_drop = cshogi.move_is_drop(move)
        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        if is_drop: # 打のとき
            back_sq = constants.PIECE_STAND_SQ
        
        else:
            # 動かす駒は、現在のマスに移動する前はどこに居たか調べます。
            try:
                back_sq = self._back_board[src_sq_obj.sq]
            except:
                # NOTE 角打だと 89 が返ってくる？
                print(f'ERROR {src_sq_obj.sq=}')
                #print(f'ERROR {src_sq_obj.sq=}', file=sys.stderr)
                raise

        if back_sq in [None, constants.PIECE_STAND_SQ]:
            # 動いていない、または、駒台にあったなら、対象外
            return constants.mind.NOT_IN_THIS_CASE

        #print(f'★ ＤoNotBack: {Helper.sq_to_masu(src_sq_obj.sq)=} の前位置は {Helper.sq_to_masu(back_sq)=}。')

        if dst_sq_obj.sq != back_sq:        # 元居た位置に戻る手でなければ。
            return constants.mind.WILL      # 意志有り。

        # FIXME 駒が取られそうなときは、戻りたい。

        # それ以外なら、意志無し。
        return constants.mind.WILL_NOT


    def _after_best_moving_negative(self, move, table):
        """指す手の確定時。
        """

        if not self.is_enabled:
            return

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))
        is_drop = cshogi.move_is_drop(move)

        # FIXME 暫定で玉は対象外。玉は右へ進みたいから、号令［相手が手を戻したら自分も戻せ］で戻したときは、戻り直してもよいようにしたい。
        if TableHelper.get_moving_pt_from_move(move) == cshogi.KING:
            return
        
        # 戻れない駒は対象外。
        if TableHelper.get_moving_pt_from_move(move) in [cshogi.KNIGHT, cshogi.LANCE, cshogi.PAWN]:
            return

        # 移動元のマス番号
        if is_drop: # 打のとき。                
            src_sq = constants.PIECE_STAND_SQ
        else:
            src_sq = src_sq_obj.sq

        # 記憶
        self._back_board[dst_sq_obj.sq] = src_sq

        if not is_drop:
            self._back_board[src_sq] = None

        #print(f'★ ＤoNotBack: {Helper.sq_to_masu(dst_sq_obj.sq)=} に前位置 {Helper.sq_to_masu(src_sq)=} を記憶。')
