import cshogi
import random

from ..logics import MovesReductionFilterLogics


class GoLogic():


    @staticmethod
    def Go(gymnasium):
        """思考開始～最善手返却

        Returns
        -------
        best_move_as_usi : str
            ［指す手］
        """
        if gymnasium.table.is_game_over():
            """投了局面時"""

            # 投了
            print(f'bestmove resign', flush=True)
            return

        if gymnasium.table.is_nyugyoku():
            """入玉宣言局面時"""

            # 勝利宣言
            print(f'bestmove win', flush=True)
            return

        # 一手詰めを詰める
        if not gymnasium.table.is_check():
            """自玉に王手がかかっていない時で"""

            if (matemove := gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""

                best_move = cshogi.move_to_usi(matemove)
                print('info score mate 1 pv {}'.format(best_move), flush=True)
                print(f'bestmove {best_move}', flush=True)
                return

        # 合法手から、１手を選び出します。
        # ［指前］
        remaining_moves = MovesReductionFilterLogics.before_move_o1(
                remaining_moves = list(gymnasium.table.legal_moves),
                gymnasium       = gymnasium)

        # 指し手が全部消えてしまった場合、何でも指すようにします
        if len(remaining_moves) < 1:
            remaining_moves = list(gymnasium.table.legal_moves)

        # １手指す（投了のケースは対応済みなので、ここで対応しなくていい）
        best_move = random.choice(remaining_moves)
        best_move_as_usi = cshogi.move_to_usi(best_move)

        # ［指後］
        MovesReductionFilterLogics.after_best_moving(
                move        = best_move,
                gymnasium   = gymnasium)

        return best_move_as_usi
