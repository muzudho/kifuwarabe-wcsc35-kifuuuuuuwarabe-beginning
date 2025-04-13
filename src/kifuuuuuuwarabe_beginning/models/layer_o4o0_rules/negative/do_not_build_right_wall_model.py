import cshogi

from ....logics.layer_o1o0.helper import Helper
from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotBuildRightWallModel(NegativeRuleModel):
    """号令［右壁を作るな］
    ［右壁を作らない］意志

    NOTE 飛車も玉も、［右壁］の構成物になるので注意。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_build_right_wall',
                label       = '右壁を作るな',
                basketball_court_model  = basketball_court_model)


    def _before_move_nrm(self, move, table):
        """指す前に。

        定義：　移動前の玉の以右の全ての筋について、８段目、９段目の両方に駒がある状態を［右壁］とする。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))
        #print(f'D: {cshogi.move_to_usi(move)=} {Helper.sq_to_masu(src_sq_obj.sq)=} {Helper.sq_to_masu(dst_sq_obj.sq)=}')

        # ライオンの指し手なら対象外
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            #print(f'★ ライオンの指し手は対象外')
            return constants.mind.NOT_IN_THIS_CASE

        k_sq_obj = SquareModel(table.king_square(table.turn))     # 移動前の自玉の位置
        #print(f'★ {k_sq_obj.file=} {np.suji(1)=}')

        # ライオンが１筋にいるなら対象外
        if k_sq_obj.file == np.suji(1):
            #print(f'★ ライオンが１筋にいるなら対象外')
            return constants.mind.NOT_IN_THIS_CASE

        # ライオンより左に移動する手なら対象外
        e1 = np.swap(k_sq_obj.file, dst_sq_obj.file)
        #print(f'★ {k_sq_obj.file=} {dst_sq_obj.file=} {e1[0]=} {e1[1]}')
        if e1[0] < e1[1]:
            #print(f'★ ライオンより左に移動する手なら対象外')
            return constants.mind.NOT_IN_THIS_CASE

        # ８段目、９段目以外に移動する手なら対象外
        dan8 = np.dan(8)
        dan9 = np.dan(9)
        #print(f'D: {dst_sq_obj.rank=} {np.dan(8)=} {np.dan(9)}')
        if dst_sq_obj.rank not in [dan8, dan9]:
            #print(f'★ {dst_sq_obj.rank=}段目 は、 {dan8}段目、{dan9}段目以外に移動する手だから対象外')
            return constants.mind.NOT_IN_THIS_CASE


        # 玉の元位置より右の全ての筋で起こる移動について
        right_side_of_k = []

        # 八段目、九段目
        for rank in [np.dan(8), np.dan(9)]:
            sq = Helper.file_rank_to_sq(dst_sq_obj.file, rank)
            #print(f'D: {rank=} {sq=}')
            right_side_of_k.append(sq)

            # 道を塞ぐ動きなら
            if dst_sq_obj.sq in right_side_of_k:
                # 道を消す
                #print(f'D: 道を消す')
                right_side_of_k.remove(dst_sq_obj.sq)

        # 道が空いているか？
        is_empty = False
        for sq in right_side_of_k:
            if (table.piece(sq) == cshogi.NONE
                    # 👇 香車が９段目から８段目に上がるのを右壁と誤認するのを防ぐ
                    or sq == src_sq_obj.sq):
                #print(f'D: 道が空いている')
                is_empty = True

        if not is_empty:
            # 道が開いていなければ、意志なし
            #print(f'★ 道が開いていなければ、意志なし')
            return constants.mind.WILL_NOT


        # 道は空いていたから、意志あり
        #print(f'★ 道は空いていたから、意志あり')
        return constants.mind.WILL
