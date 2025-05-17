import openpyxl as xl
import pyxlart as xa
import re

from openpyxl.styles import PatternFill, Font
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.alignment import Alignment

from ....models.layer_o1o_8o0_str import StringResourcesModel
from ....models.layer_o1o0 import TurnModel


class XsBoardView():


    def __init__(self):
        # 色
        BLACK = '000000'
        BACKGROUND_COLOR = 'F2DCDB'
        BOARD_COLOR = 'DAEEF3'
        HEADER_1_COLOR = 'FCD5B4'
        HEADER_2_COLOR = 'FDE9D9'
        TITLE_COLOR = '4F81BD'

        # フォント
        self._LARGE_FONT = Font(size=20.0)
        self._NEXT_LABEL_FONT = Font(size=12.0, color='31869B')
        self._NEXT_VALUE_FONT = Font(size=12.0, bold=True, color='60497A')
        self._TITLE_FONT = Font(size=16.0, color=TITLE_COLOR)
        self._SMALL_TITLE_FONT = Font(size=6.0, color=TITLE_COLOR)

        # 罫線
        self._thin_black_side = Side(style='thin', color=BLACK)
        self._thick_black_side = Side(style='thick', color=BLACK)
        #self._board_top_border = Border(top=self._thick_black_side)
        self._board_cell_border = Border(left=self._thin_black_side, right=self._thin_black_side, top=self._thin_black_side, bottom=self._thin_black_side)
        self._board_top_left_border = Border(left=self._thick_black_side, top=self._thick_black_side)
        self._board_top_border = Border(top=self._thick_black_side)
        self._board_top_right_border = Border(right=self._thick_black_side, top=self._thick_black_side)
        self._board_left_border = Border(left=self._thick_black_side)
        self._board_right_border = Border(right=self._thick_black_side)
        self._board_bottom_left_border = Border(left=self._thick_black_side, bottom=self._thick_black_side)
        self._board_bottom_border = Border(bottom=self._thick_black_side)
        self._board_bottom_right_border = Border(right=self._thick_black_side, bottom=self._thick_black_side)

        # フィル
        self._background_fill = PatternFill(patternType='solid', fgColor=BACKGROUND_COLOR)
        self._board_fill = PatternFill(patternType='solid', fgColor=BOARD_COLOR)
        self._header_1_fill = PatternFill(patternType='solid', fgColor=HEADER_2_COLOR)
        self._header_2_fill = PatternFill(patternType='solid', fgColor=HEADER_1_COLOR)

        # 寄せ
        #   horizontal は 'distributed', 'fill', 'general', 'center', 'centerContinuous', 'justify', 'right', 'left' のいずれかから選ぶ
        #   vertical は 'center', 'top', 'bottom', 'justify', 'distributed' のいずれかから選ぶ
        self._left_top_alignment = Alignment(horizontal='left', vertical='top')
        self._left_center_alignment = Alignment(horizontal='left', vertical='center')
        self._center_center_alignment = Alignment(horizontal='center', vertical='center')
        self._right_center_alignment = Alignment(horizontal='right', vertical='center')


    def render(self, gymnasium):
        """描画。
        """

        # ワークブックを新規生成
        wb = xl.Workbook()

        # ワークシート
        ws = wb['Sheet']

        # 方眼紙を作成します。
        xa.GraphPaperRenderer.render(
                left_th = 1,
                top_th  = 1,
                width   = 100,
                height  = 100,
                ws      = ws)

        self._render_background(ws)                     # 背景を描画。
        self._render_next_label_1(ws)                   # 何手目ラベル１。
        self._render_next_value(ws, gymnasium)          # 何手目値。
        self._render_moves_label_2(ws)                  # 何手目ラベル２。
        self._render_color(ws, gymnasium)               # 手番の描画。
        self._render_repetition_label(ws)               # 局面反復回数ラベル。
        self._render_repetition_value(ws)               # 局面反復回数値。
        self._render_title(ws)                          # タイトルを描画。
        self._render_mars_hands(ws, gymnasium)          # 一段目側の持ち駒の描画。
        self._render_earth_hands(ws, gymnasium)         # 九段目側の持ち駒の描画。
        self._render_board_background_except_squares(ws, gymnasium)    # 盤の背景を描画。マスを除く。
        self._render_board_frame(ws, gymnasium)         # 盤の枠を描画。
       

        # a7 = ws[f'A7']
        # a7.value = 'v香'
        # a7.border = board_top_boarder
        # a7.fill = self._board_fill

        # b7 = ws[f'B7']
        # b7.value = 'v桂'
        # b7.border = board_top_boarder
        # a7.fill = self._board_fill

        # c7 = ws[f'C7']
        # c7.value = 'v銀'
        # c7.border = board_top_boarder
        # a7.fill = self._board_fill

        # d7 = ws[f'D7']
        # d7.value = 'v金'
        # d7.border = board_top_boarder
        # a7.fill = self._board_fill

        # e7 = ws[f'E7']
        # e7.value = 'v玉'

        # f7 = ws[f'F7']
        # f7.value = 'v金'

        # g7 = ws[f'G7']
        # g7.value = 'v銀'

        # h7 = ws[f'H7']
        # h7.value = 'v桂'

        # i7 = ws[f'I7']
        # i7.value = 'v香'

        # ws[f'B8'].value = 'v飛'
        # ws[f'H8'].value = 'v角'

        # ws[f'A9'].value = 'v歩'
        # ws[f'B9'].value = 'v歩'
        # ws[f'C9'].value = 'v歩'
        # ws[f'D9'].value = 'v歩'
        # ws[f'E9'].value = 'v歩'
        # ws[f'F9'].value = 'v歩'
        # ws[f'G9'].value = 'v歩'
        # ws[f'H9'].value = 'v歩'
        # ws[f'I9'].value = 'v歩'

        # ws[f'A13'].value = '歩'
        # ws[f'B13'].value = '歩'
        # ws[f'C13'].value = '歩'
        # ws[f'D13'].value = '歩'
        # ws[f'E13'].value = '歩'
        # ws[f'F13'].value = '歩'
        # ws[f'G13'].value = '歩'
        # ws[f'H13'].value = '歩'
        # ws[f'I13'].value = '歩'

        # ws[f'B14'].value = '飛'
        # ws[f'H14'].value = '角'

        # ws[f'A15'].value = '香'
        # ws[f'B15'].value = '桂'
        # ws[f'C15'].value = '銀'
        # ws[f'D15'].value = '金'
        # ws[f'E15'].value = '玉'
        # ws[f'F15'].value = '金'
        # ws[f'G15'].value = '銀'
        # ws[f'H15'].value = '桂'
        # ws[f'I15'].value = '香'

        # ワークブック保存
        gymnasium.exshell.save_workbook(wb=wb)

        # エクセル開く
        gymnasium.exshell.open_virtual_display()

        line = input('何か入力してください。例： y\n')
        print() # 空行

        # エクセル閉じる
        gymnasium.exshell.close_virtual_display()


    def _render_background(self, ws):
        """背景を描画。
        """
        start_row_th = 1
        end_row_th = 27
        for y_th in range(start_row_th, end_row_th + 1):
            for column_letter in xa.ColumnLetterRange(start='A', end='AK'):
                row_th = y_th
                cell = ws[f"{column_letter}{row_th}"]
                cell.fill = self._background_fill


    def _render_next_label_1(self, ws):
        """何手目ラベル１。
        """
        cell = ws['C2']
        cell.value = 'Next'
        cell.font = self._NEXT_LABEL_FONT
        cell.fill = self._header_2_fill
        cell.alignment = self._right_center_alignment
        ws.merge_cells('C2:D2')


    def _render_next_value(self, ws, gymnasium):
        """何手目値。
        """
        cell = ws['E2']
        cell.value = gymnasium.table.move_number
        cell.font = self._NEXT_VALUE_FONT
        cell.fill = self._header_1_fill
        cell.alignment = self._center_center_alignment
        ws.merge_cells('E2:F2')


    def _render_moves_label_2(self, ws):
        """何手目ラベル２。
        """
        cell = ws['G2']
        cell.value = 'move(s)'
        cell.font = self._NEXT_LABEL_FONT
        cell.fill = self._header_2_fill
        cell.alignment = self._left_center_alignment
        ws.merge_cells('G2:J2')


    def _render_color(self, ws, gymnasium):
        """手番の描画。
        """
        cell = ws['K2']
        cell.value = TurnModel.code(gymnasium.table.turn).capitalize()
        cell.font = self._NEXT_VALUE_FONT
        cell.fill = self._header_1_fill
        cell.alignment = self._center_center_alignment
        ws.merge_cells('K2:L2')


    def _render_repetition_label(self, ws):
        """局面反復回数ラベル。
        """
        cell = ws['M2']
        cell.value = 'Repetition'
        cell.font = self._NEXT_LABEL_FONT
        cell.fill = self._header_2_fill
        cell.alignment = self._right_center_alignment
        ws.merge_cells('M2:P2')


    def _render_repetition_value(self, ws):
        """局面反復回数値。
        """
        cell = ws['Q2']
        cell.value = '_'
        cell.font = self._NEXT_VALUE_FONT
        cell.fill = self._header_1_fill
        cell.alignment = self._left_center_alignment


    def _render_title(self, ws):
        """タイトルを描画。
        """
        cell = ws['S2']
        cell.value = 'B'
        cell.font = self._TITLE_FONT

        cell = ws['T2']
        cell.value = 'i'
        cell.font = self._TITLE_FONT

        cell = ws['U2']
        cell.value = 'g'
        cell.font = self._TITLE_FONT

        cell = ws['W2']
        cell.value = 'D'
        cell.font = self._TITLE_FONT

        cell = ws['X2']
        cell.value = 'o'
        cell.font = self._TITLE_FONT

        cell = ws['Y2']
        cell.value = 'b'
        cell.font = self._TITLE_FONT

        cell = ws['Z2']
        cell.value = 'u'
        cell.font = self._TITLE_FONT

        cell = ws['AA2']
        cell.value = 't'
        cell.font = self._TITLE_FONT

        cell = ws['AB2']
        cell.value = 's'
        cell.font = self._TITLE_FONT

        cell = ws['AC2']
        cell.value = 'u'
        cell.font = self._TITLE_FONT

        cell = ws['AE2']
        cell.value = 's'
        cell.font = self._TITLE_FONT

        cell = ws['AF2']
        cell.value = 'h'
        cell.font = self._TITLE_FONT

        cell = ws['AG2']
        cell.value = 'o'
        cell.font = self._TITLE_FONT

        cell = ws['AH2']
        cell.value = 'g'
        cell.font = self._TITLE_FONT

        cell = ws['AI2']
        cell.value = 'i'
        cell.font = self._TITLE_FONT

        cell = ws['S3']
        cell.value = 'Original 3x4 board was invented by Madoka Kitao. The original pieces were designed by Maiko Fujita.'
        cell.font = self._SMALL_TITLE_FONT
        cell.alignment = self._left_top_alignment


    def _render_mars_hands(self, ws, gymnasium):
        """一段目側の持ち駒の描画。
        """
        # 駒台を塗り潰し
        for row_th in range(5, 21):
            for column_letter in xa.ColumnLetterRange(start='C', end='G'):
                # セル設定
                cell = ws[f"{column_letter}{row_th}"]
                cell.fill = self._board_fill

        for row_th in range(6, 19, 2):  # セル結合
            ws.merge_cells(f"E{row_th}:F{row_th+1}")
            cell = ws[f"E{row_th}"]
            cell.font = self._LARGE_FONT
            cell.alignment = self._center_center_alignment

        # 後手の持ち駒の数のリスト
        w_hand = gymnasium.table.pieces_in_hand[1]
        # 後手の持ち駒の数
        ws['E6'].value      = w_hand[6]     # 歩
        ws['E8'].value      = w_hand[5]     # 香
        ws['E10'].value     = w_hand[4]     # 桂
        ws['E12'].value     = w_hand[3]     # 銀
        ws['E14'].value     = w_hand[2]     # 金
        ws['E16'].value     = w_hand[1]     # 角
        ws['E18'].value     = w_hand[0]     # 飛


    def _render_earth_hands(self, ws, gymnasium):
        """九段目側の持ち駒の描画。
        """
        # 駒台を塗り潰し
        for row_th in range(9, 25):
            for column_letter in xa.ColumnLetterRange(start='AE', end='AI'):
                # セル設定
                cell = ws[f"{column_letter}{row_th}"]
                cell.fill = self._board_fill

        for row_th in range(10, 23, 2):  # セル結合
            ws.merge_cells(f"AG{row_th}:AH{row_th+1}")
            cell = ws[f"AG{row_th}"]
            cell.font = self._LARGE_FONT
            cell.alignment = self._center_center_alignment

        # 先手、後手の持ち駒の数のリスト
        b_hand = gymnasium.table.pieces_in_hand[0]
        # 先手の持ち駒の数
        ws['AG10'].value    = b_hand[6]     # 飛
        ws['AG12'].value    = b_hand[5]     # 角
        ws['AG14'].value    = b_hand[4]     # 金
        ws['AG16'].value    = b_hand[3]     # 銀
        ws['AG18'].value    = b_hand[2]     # 桂
        ws['AG20'].value    = b_hand[1]     # 香
        ws['AG22'].value    = b_hand[0]     # 歩


    def _render_board_background_except_squares(self, ws, gymnasium):
        """盤の背景を描画。マスを除く。
        """
        # 枠の辺を塗り潰し
        # 上辺
        for row_th in range(4, 6):
            for column_letter in xa.ColumnLetterRange(start='H', end='AD'):
                ws[f"{column_letter}{row_th}"].fill = self._board_fill

        # 下辺
        for row_th in range(24, 26):
            for column_letter in xa.ColumnLetterRange(start='H', end='AD'):
                ws[f"{column_letter}{row_th}"].fill = self._board_fill

        # 左辺
        for row_th in range(6, 24):
            for column_letter in xa.ColumnLetterRange(start='H', end='J'):
                ws[f"{column_letter}{row_th}"].fill = self._board_fill

        # 右辺
        for row_th in range(6, 24):
            for column_letter in xa.ColumnLetterRange(start='AB', end='AD'):
                ws[f"{column_letter}{row_th}"].fill = self._board_fill

        # 筋の番号
        for index, column_letter in enumerate(xa.ColumnLetterRange(start='I', end='Z', step=2)):
            next_column_letter = xa.ColumnLetterLogic.add(column_letter, 1)
            ws.merge_cells(f"{column_letter}4:{next_column_letter}5")
            cell = ws[f"{column_letter}4"]
            cell.value = f"'{StringResourcesModel.zenkaku_suji_list()[9-index]}"
            cell.font = self._LARGE_FONT
            cell.alignment = self._center_center_alignment

        # 段の番号
        for index, row_th in enumerate(range(6, 23, 2)):
            ws.merge_cells(f"AA{row_th}:AB{row_th+1}")
            cell = ws[f"AA{row_th}"]
            cell.value = f"{StringResourcesModel.kan_suji_list()[index+1]}"
            cell.font = self._LARGE_FONT
            cell.alignment = self._center_center_alignment


    def _render_board_frame(self, ws, gymnasium):
        """盤の枠を描画。
        """
        # 盤の各マス
        for row_th in range(6, 23, 2):
            for column_letter in xa.ColumnLetterRange(start='I', end='Z', step=2):
                # セル設定
                cell = ws[f"{column_letter}{row_th}"]
                cell.border = self._board_cell_border
                cell.fill = self._board_fill

                next_column_letter = xa.ColumnLetterLogic.add(column_letter, 1)

                # セル結合
                ws.merge_cells(f"{column_letter}{row_th}:{next_column_letter}{row_th+1}")

        # 盤の枠を太線にします。セル結合を考えず描きます。
        ws['I6'].border = self._board_top_left_border
        ws['Z6'].border = self._board_top_right_border
        ws['I23'].border = self._board_bottom_left_border
        ws['Z23'].border = self._board_bottom_right_border
        for column_letter in xa.ColumnLetterRange(start='J', end='Z'):
            cell = ws[xa.CellAddressModel.from_code(f"{column_letter}6").to_code()]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = self._board_top_border)

            cell = ws[xa.CellAddressModel.from_code(f"{column_letter}23").to_code()]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = self._board_bottom_border)

        for row_th in range(7, 23):
            cell = ws[f"I{row_th}"]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = self._board_left_border)

            cell = ws[f"Z{row_th}"]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = self._board_right_border)
