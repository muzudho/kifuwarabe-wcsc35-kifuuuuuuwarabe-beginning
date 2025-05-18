import cshogi
import openpyxl as xl

from openpyxl.styles import PatternFill, Font
from ...models.layer_o1o0o1o0_japanese import JapaneseMoveModel


class XlSearchModule:
    """Excel を用いた探索部。
    """


    _PATH_TO_XL_SEARCH_WORKSHEET = './temp/search_part_work.xlsx'


    def __init__(self, gymnasium):
        """［初期化］

        Parameters
        ----------
        gymnasium : GymnasiumModel
            ［体育館］
            記憶は全部この中に詰め込めます。
        """
        self._gymnasium = gymnasium

        # 色
        self._HEADER_BLACK = '404040'
        self._HEADER_WHITE = 'F2F2F2'

        # フォント
        self._HEADER_FONT = Font(size=12.0, color=self._HEADER_WHITE)


    def render_1st_move(self, move_list):
        """１手目を描画。
        """
        try:
            # ワークブックを新規生成
            wb = xl.Workbook()

            # ワークシート
            ws = wb['Sheet']

            cell = ws['A1']
            cell.value = '削除'
            cell.fill = PatternFill(patternType='solid', fgColor=self._HEADER_BLACK)
            cell.font = self._HEADER_FONT

            cell = ws['B1']
            cell.value = '1階合法手'
            cell.fill = PatternFill(patternType='solid', fgColor=self._HEADER_BLACK)
            cell.font = self._HEADER_FONT

            cell = ws['C1']
            cell.value = '1階終端'
            cell.fill = PatternFill(patternType='solid', fgColor=self._HEADER_BLACK)
            cell.font = self._HEADER_FONT

            row_th = 2

            # 指す前
            ws[f"B{row_th}"].value = '(指す前)'

            if self._gymnasium.table.is_game_over():
                """投了局面時。
                """
                ws[f"C{row_th}"].value = 'GAME_OVER'
                return

            if self._gymnasium.table.is_nyugyoku():
                """入玉宣言勝ち局面時。
                """
                ws[f"C{row_th}"].value = 'NYUGYOKU_WIN'
                return

            # 一手詰めを詰める
            if not self._gymnasium.table.is_check():
                """自玉に王手がかかっていない時で"""

                if (matemove := self._gymnasium.table.mate_move_in_1ply()):
                    """一手詰めの指し手があれば、それを取得"""
                    ws[f"C{row_th}"].value = 'MATE_IN_1_MOVE'
                    return

            row_th += 1

            # 指し手
            for index, move in enumerate(move_list):

                # 指し手のUSI表記に、独自形式を併記。
                ws[f"B{row_th}"].value = JapaneseMoveModel.from_move(
                        move    = move,
                        cap_pt  = self._gymnasium.table.piece_type(sq=cshogi.move_to(move)),
                        is_mars = False,
                        is_gote = self._gymnasium.table.is_gote).stringify()

                row_th += 1

            wb.save(filename=XlSearchModule._PATH_TO_XL_SEARCH_WORKSHEET)

        except Exception as ex:
            print(ex)
