import cshogi

from ..logics_o1x import Helper
from ..models_o1x import constants, MoveWithProfit, PieceValues, PieceType, Square, Turn


class QuiescenceSearchForScramble():
    """駒の取り合いのための静止探索。
    駒の取り合いが終わるまで、駒の取り合いを探索します。
    """


    def __init__(self, max_depth, gymnasium):
        """
        Parameters
        ----------
        gymnasium : Gymnasium
            体育館。        
        """
        self._max_depth = max_depth
        self._gymnasium = gymnasium


    def search_alice(self, depth, alice_s_remaining_moves):
        """
        TODO 静止探索はせず、［スクランブル・サーチ］というのを考える。静止探索は王手が絡むと複雑だ。
        リーガル・ムーブのうち、
          手番の１手目なら：
              ［取られそうになっている駒を逃げる手］∪［駒を取る手］∪［利きに飛び込む手］に絞り込む。（１度調べた手は２度目は調べない）
              ［放置したとき］も調べる。
          相手番の１手目なら：
              ［動いた駒を取る手］に絞り込む。（１番安い駒から動かす）
          手番の２手目なら：
              ［動いた駒を取る手］に絞り込む。（１番安い駒から動かす）
          最後の評価値が、１手目の評価値。

        Parameters
        ----------
        depth : int
            残りの探索深さ。
        alice_s_remaining_moves : list<int>
            アリスの指し手のリスト。

        Returns
        -------
        alice_s_best_value : int
            アリスの点数。
        alice_s_best_move_list : list
            アリスの最善手のリスト。０～複数件の指し手。
        alice_s_move_wp_list : dist
            アリスの全ての指し手と得のペアのリスト。
            投了時は空っぽのリスト。
            FIXME 入玉宣言勝ちは空リスト。
        """

        if depth < 1:
            raise ValueError(f'depth が 1 未満のときにこのメソッドを呼び出してはいけません。 {depth=}')

        ########################
        # MARK: 指す前にやること
        ########################

        if self._gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            return constants.value.GAME_OVER, [], {} # 負けだから

        if self._gymnasium.table.is_nyugyoku():
            """手番の入玉宣言局面時。
            """
            return constants.value.NYUGYOKU_WIN, [], {}  # 勝ちだから  FIXME 入玉宣言勝ちをどうやって返す？

        # 一手詰めを詰める
        if not self._gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return constants.value.CHECKMATE, matemove, {matemove: constants.value.CHECKMATE}  # 勝ちだから

        alice_s_best_value = constants.value.NOTHING_CAPTURE_MOVE  # （指し手のリストが空でなければ）どんな手でも更新される。
        alice_s_best_move_list          = []
        alice_s_move_wp_list            = []

        ##############################
        # MARK: アリスの合法手スキャン
        ##############################

        # 手番（アリス）が［駒を取る手］を全部調べる。
        for index, alice_s_move in enumerate(alice_s_remaining_moves):

            ##########################
            # MARK: アリスが一手指す前
            ##########################

            dst_sq_obj = Square(cshogi.move_to(alice_s_move))           # 移動先マス
            cap_pt = self._gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            piece_value = PieceValues.by_piece_type(pt=cap_pt)

            # １回呼出時。
            if self._max_depth == depth:
                pass    # 何も無視しない。
            else:
                # 駒を取る手でなければ無視。
                if cap_pt == cshogi.NONE:
                    continue

            ########################
            # MARK: アリスが一手指す
            ########################

            self._gymnasium.do_move_o1x(move = alice_s_move)
            depth -= 1

            ############################
            # MARK: アリスが一手指した後
            ############################

            #print(f"(next {self._gymnasium.table.move_number} teme) ({index}) alice's move={cshogi.move_to_usi(alice_s_move)}({Helper.sq_to_masu(dst_sq_obj.sq)}) pt({PieceType.alphabet(piece_type=cap_pt)}) {alice_s_profit_after_move=} {piece_profit=}")

            # これ以上深く読まない場合。
            if depth - 1 < 1:
                alice_s_value = piece_value     # 駒を取ったことによる得。

            # まだ深く読む場合。
            else:
                #raise ValueError(f"depth error: {depth=}") # FIXME
                #print(f"まだ深く読む {depth=}")

                (
                    bob_s_value,
                    bob_s_best_move_list,   # FIXME 入玉宣言勝ちは空リストが返ってくる。
                    bob_s_move_wp_list
                ) = self.search_alice(
                    depth                           = depth,
                    alice_s_remaining_moves         = list(self._gymnasium.table.legal_moves))

                alice_s_value = piece_value - bob_s_value   # 今取った駒の価値から、末端の枝の積み重ね（bob_s_value）を引く。

            # TODO アリスとしては、損が一番小さな分岐へ進みたい。
            # 手番は、一番得する手を指したい。
            if alice_s_best_value < alice_s_value:
                alice_s_best_value = alice_s_value
                alice_s_best_move_list = [alice_s_move]
            elif alice_s_best_value == alice_s_value:
                alice_s_best_move_list.append(alice_s_move)

            # 指し手と、その得を紐づけます。
            alice_s_move_wp_list.append(
                    MoveWithProfit(
                            move    = alice_s_move,
                            profit  = alice_s_value))

            ########################
            # MARK: アリスが一手戻す
            ########################

            self._gymnasium.undo_move_o1x()

            ############################
            # MARK: アリスが一手戻した後
            ############################

            depth += 1

        ########################
        # MARK: 合法手スキャン後
        ########################
        return alice_s_best_value, alice_s_best_move_list, alice_s_move_wp_list
