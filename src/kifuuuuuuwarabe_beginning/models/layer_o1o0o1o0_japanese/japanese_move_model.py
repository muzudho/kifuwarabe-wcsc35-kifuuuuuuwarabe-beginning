import cshogi

from ..layer_o1o_8o0_str import StringResourcesModel
from ..layer_o1o0o_9o0_table_helper import TableHelper
from ..layer_o1o0 import PlanetPieceTypeModel, SquareModel


class JapaneseMoveModel:
    """日本人が読みやすい書式の指し手。
    """


    @staticmethod
    def from_move(move, cap_pt, is_mars, is_gote):
        """
        Parameters
        ----------
        move : int
            シーショーギの指し手。
        cap_pt : int
            取った駒種類。
        is_mars : bool
            火星か。
        is_gote : bool
            後手か。
        """
        src_sq_obj  = SquareModel(cshogi.move_from(move))       # ［移動元マス］
        dst_sq_obj  = SquareModel(cshogi.move_to(move))         # ［移動先マス］
        is_prom     = cshogi.move_is_promotion(move)            # ［成］
        is_drop     = cshogi.move_is_drop(move)                 # ［打］

        moving_pt = TableHelper.get_moving_pt_from_move(move)   # 駒種類。盤上の移動元の駒か、打った駒。

        moving_pt_str = PlanetPieceTypeModel.kanji_on_text(
                piece_type  = moving_pt,
                is_mars     = is_mars,
                is_gote     = is_gote)

        return JapaneseMoveModel(
                move            = move,
                cap_pt          = cap_pt,
                src_sq_obj      = src_sq_obj,
                dst_sq_obj      = dst_sq_obj,
                moving_pt_str   = moving_pt_str,
                is_prom         = is_prom,
                is_drop         = is_drop,
                is_mars         = is_mars)


    def __init__(self, move, cap_pt, src_sq_obj, dst_sq_obj, moving_pt_str, is_prom, is_drop, is_mars):
        self._move          = move
        self._cap_pt        = cap_pt
        self._src_sq_obj    = src_sq_obj
        self._dst_sq_obj    = dst_sq_obj
        self._moving_pt_str = moving_pt_str
        self._is_prom       = is_prom
        self._is_drop       = is_drop
        self._is_mars       = is_mars


    @property
    def src_sq_obj(self):
        return self._src_sq_obj


    @property
    def dst_sq_obj(self):
        return self._dst_sq_obj


    @property
    def moving_pt_str(self):
        return self._moving_pt_str


    @property
    def is_prom(self):
        return self._is_prom


    @property
    def is_drop(self):
        return self._is_drop


    def stringify(self):
        """文字列化。
        """

        try:
            if self._is_drop:
                # 打なら
                src_str = ''

            else:
                # 盤上なら
                # ［移動元マス］
                src_str = f"{StringResourcesModel.zenkaku_suji_list()[self._src_sq_obj.file + 1]}{StringResourcesModel.kan_suji_list()[self._src_sq_obj.rank + 1]}→"

            # ［移動先マス］
            dst_file_str = StringResourcesModel.zenkaku_suji_list()[self._dst_sq_obj.file + 1]
            dst_rank_str = StringResourcesModel.kan_suji_list()[self._dst_sq_obj.rank + 1]

        except IndexError as ex:
            print(f"human_presentable_move_model.py: {cshogi.move_to_usi(self._move)=} {self._src_sq_obj.file=} {self._src_sq_obj.rank=} {self._dst_sq_obj.file=} {self._dst_sq_obj.rank=} {ex=}")
            raise
        

        def _prom():
            if self._is_prom:
                return '成'
            return ''


        def _drop_kanji():
            if self._is_drop:
                return StringResourcesModel.drop_kanji()
            return ''
        

        def _cap(cap_pt, is_mars):
            if cap_pt == cshogi.NONE:
                return ''
            
            if is_mars:
              return f"-{PlanetPieceTypeModel.earth_kanji(piece_type=cap_pt)}"    # 火星側が取ったのは地球側の駒
            return f"+{PlanetPieceTypeModel.mars_kanji(piece_type=cap_pt)}"     # 地球側が取ったのは火星側の駒


        return f"{src_str}{dst_file_str}{dst_rank_str}{self.moving_pt_str}{_prom()}{_drop_kanji()}{_cap(cap_pt=self._cap_pt,is_mars=self._is_mars)}"
