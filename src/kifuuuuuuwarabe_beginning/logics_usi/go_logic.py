import cshogi
import random

from ..logics import MovesReductionFilterLogics


class GoLogicResultState():


    @staticmethod
    def RESIGN():
        """投了。
        """
        return 1


    @staticmethod
    def NYUGYOKU_WIN():
        """入玉宣言局面時。
        """
        return 2


    def MATE_IN_1_MOVE():
        """１手詰め時。
        """
        return 3


    def BEST_MOVE():
        """通常時の次の１手。
        """
        return 4


class GoLogic():


    @staticmethod
    def Go(gymnasium):
        """盤面が与えられるので、次の１手を返します。

        Returns
        -------
        best_move_as_usi : str
            ［指す手］
        """

        if gymnasium.table.is_game_over():
            """投了局面時。
            """
            return GoLogicResultState.RESIGN, None

        if gymnasium.table.is_nyugyoku():
            """入玉宣言局面時。
            """
            return GoLogicResultState.NYUGYOKU_WIN, None

        # 一手詰めを詰める
        if not gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                best_move_as_usi = cshogi.move_to_usi(matemove)
                return GoLogicResultState.MATE_IN_1_MOVE, best_move_as_usi

        # 合法手から、１手を選び出します。
        # （必ず、投了ではない手が存在します）
        #
        # ［指前］
        #       制約：
        #           指し手は必ず１つ以上残っています。
        remaining_moves = MovesReductionFilterLogics.before_move_o1x(
                remaining_moves = list(gymnasium.table.legal_moves),
                gymnasium       = gymnasium)

        if gymnasium.config_doc['debug_mode']['search_do_undo']:
            print('in debug')
            dump_1 = gymnasium.dump()

        # 残った手一覧
        for move in remaining_moves:

            # 一手指す
            gymnasium.do_move_o1x(move = move)
            #print(f'move: {cshogi.move_to_usi(move)}')

            # 一手戻す
            gymnasium.undo_move_o1x()

            if gymnasium.config_doc['debug_mode']['search_do_undo']:
                dump_2 = gymnasium.dump()
                if dump_1 != dump_2:
                    raise(f"""探索でずれが発生しました。
dump_1:
{dump_1}
dump_2:
{dump_2}
""")


        # １手に絞り込む
        best_move = random.choice(remaining_moves)
        best_move_as_usi = cshogi.move_to_usi(best_move)

        # ［指後］
        MovesReductionFilterLogics.after_best_moving(
                move        = best_move,
                gymnasium   = gymnasium)

        return GoLogicResultState.BEST_MOVE, best_move_as_usi
