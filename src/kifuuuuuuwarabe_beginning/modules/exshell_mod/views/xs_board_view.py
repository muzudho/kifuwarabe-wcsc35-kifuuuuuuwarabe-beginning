import openpyxl as xl
import pyxlart as xa
import re

from openpyxl.styles import PatternFill, Font
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.alignment import Alignment

from ....models.layer_o1o_8o0_str import StringResourcesModel
from ....models.layer_o1o0 import TurnModel


class XsBoardView():


    @staticmethod
    def render(gymnasium):
        """描画。
        """

        # 色
        BLACK = '000000'
        BOARD_COLOR = 'DAEEF3'
        HEADER_1_COLOR = 'FDE9D9'
        HEADER_2_COLOR = 'FCD5B4'

        # フォント
        LARGE_FONT = Font(size=20.0)

        # 罫線
        thin_black_side = Side(style='thin', color=BLACK)
        thick_black_side = Side(style='thick', color=BLACK)
        #board_top_border = Border(top=thick_black_side)
        board_cell_border = Border(left=thin_black_side, right=thin_black_side, top=thin_black_side, bottom=thin_black_side)
        board_top_left_border = Border(left=thick_black_side, top=thick_black_side)
        board_top_border = Border(top=thick_black_side)
        board_top_right_border = Border(right=thick_black_side, top=thick_black_side)
        board_left_border = Border(left=thick_black_side)
        board_right_border = Border(right=thick_black_side)
        board_bottom_left_border = Border(left=thick_black_side, bottom=thick_black_side)
        board_bottom_border = Border(bottom=thick_black_side)
        board_bottom_right_border = Border(right=thick_black_side, bottom=thick_black_side)

        # フィル
        board_fill = PatternFill(patternType='solid', fgColor=BOARD_COLOR)
        header_1_fill = PatternFill(patternType='solid', fgColor=HEADER_2_COLOR)
        header_2_fill = PatternFill(patternType='solid', fgColor=HEADER_1_COLOR)

        # 寄せ
        #   horizontal は 'distributed', 'fill', 'general', 'center', 'centerContinuous', 'justify', 'right', 'left' のいずれかから選ぶ
        #   vertical は 'center', 'top', 'bottom', 'justify', 'distributed' のいずれかから選ぶ
        left_center_alignment = Alignment(horizontal='left', vertical='center')
        center_center_alignment = Alignment(horizontal='center', vertical='center')
        right_center_alignment = Alignment(horizontal='right', vertical='center')

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

        # 手数等部
        ws['C2'].value = 'next'
        ws['E2'].value = gymnasium.table.move_number
        ws['G2'].value = 'move(s)'
        ws['K2'].value = TurnModel.code(gymnasium.table.turn)
        ws['M2'].value = 'repetition'
        ws['Q2'].value = "'-"
        ws['C2'].fill = header_2_fill
        ws['E2'].fill = header_1_fill
        ws['G2'].fill = header_2_fill
        ws['K2'].fill = header_1_fill
        ws['M2'].fill = header_2_fill
        ws['Q2'].fill = header_1_fill
        ws.merge_cells('C2:D2')
        ws.merge_cells('E2:F2')
        ws.merge_cells('G2:J2')
        ws.merge_cells('K2:L2')
        ws.merge_cells('M2:P2')
        ws['C2'].alignment = right_center_alignment
        ws['E2'].alignment = center_center_alignment
        ws['G2'].alignment = left_center_alignment
        ws['K2'].alignment = center_center_alignment
        ws['M2'].alignment = right_center_alignment
        ws['Q2'].alignment = left_center_alignment

        # 駒台を塗り潰し
        # 先手
        for row_th in range(8, 24):
            for column_letter in xa.ColumnLetterRange(start='AE', end='AI'):
                # セル設定
                cell = ws[f"{column_letter}{row_th}"]
                cell.fill = board_fill

        for row_th in range(9, 22, 2):  # セル結合
            ws.merge_cells(f"AG{row_th}:AH{row_th+1}")
            cell = ws[f"AG{row_th}"]
            cell.font = LARGE_FONT
            cell.alignment = center_center_alignment

        # 後手
        for row_th in range(4, 20):
            for column_letter in xa.ColumnLetterRange(start='C', end='G'):
                # セル設定
                cell = ws[f"{column_letter}{row_th}"]
                cell.fill = board_fill

        for row_th in range(5, 18, 2):  # セル結合
            ws.merge_cells(f"E{row_th}:F{row_th+1}")
            cell = ws[f"E{row_th}"]
            cell.font = LARGE_FONT
            cell.alignment = center_center_alignment

        # 先手、後手の持ち駒の数のリスト
        b_hand = gymnasium.table.pieces_in_hand[0]
        w_hand = gymnasium.table.pieces_in_hand[1]

        # 先手の持ち駒の数
        ws['AG9'].value     = b_hand[6]     # 飛
        ws['AG11'].value    = b_hand[5]     # 角
        ws['AG13'].value    = b_hand[4]     # 金
        ws['AG15'].value    = b_hand[3]     # 銀
        ws['AG17'].value    = b_hand[2]     # 桂
        ws['AG19'].value    = b_hand[1]     # 香
        ws['AG21'].value    = b_hand[0]     # 歩

        # 後手の持ち駒の数
        ws['E5'].value      = w_hand[6]     # 歩
        ws['E7'].value      = w_hand[5]     # 香
        ws['E9'].value      = w_hand[4]     # 桂
        ws['E11'].value     = w_hand[3]     # 銀
        ws['E13'].value     = w_hand[2]     # 金
        ws['E15'].value     = w_hand[1]     # 角
        ws['E17'].value     = w_hand[0]     # 飛

        # 枠の辺を塗り潰し
        # 上辺
        for row_th in range(4, 7):
            for column_letter in xa.ColumnLetterRange(start='H', end='AD'):
                ws[f"{column_letter}{row_th}"].fill = board_fill

        # 下辺
        for column_letter in xa.ColumnLetterRange(start='H', end='AD'):
            ws[f"{column_letter}25"].fill = board_fill

        # 左辺
        for row_th in range(7, 25):
            ws[f"H{row_th}"].fill = board_fill

        # 右辺
        for row_th in range(7, 25):
            for column_letter in xa.ColumnLetterRange(start='AA', end='AD'):
                ws[f"{column_letter}{row_th}"].fill = board_fill

        # 筋の番号
        for index, column_letter in enumerate(xa.ColumnLetterRange(start='I', end='Z', step=2)):
            next_column_letter = xa.ColumnLetterLogic.add(column_letter, 1)
            ws.merge_cells(f"{column_letter}5:{next_column_letter}6")
            cell = ws[f"{column_letter}5"]
            cell.value = f"'{StringResourcesModel.zenkaku_suji_list[9-index]}"
            cell.font = LARGE_FONT
            cell.alignment = center_center_alignment

        # 段の番号
        for index, row_th in enumerate(range(7, 24, 2)):
            ws.merge_cells(f"AA{row_th}:AB{row_th+1}")
            cell = ws[f"AA{row_th}"]
            cell.value = f"{StringResourcesModel.kan_suji_list[index+1]}"
            cell.font = LARGE_FONT
            cell.alignment = center_center_alignment

        # 盤の各マス
        for row_th in range(7, 24, 2):
            for column_letter in xa.ColumnLetterRange(start='I', end='Z', step=2):
                # セル設定
                cell = ws[f"{column_letter}{row_th}"]
                cell.border = board_cell_border
                cell.fill = board_fill

                next_column_letter = xa.ColumnLetterLogic.add(column_letter, 1)

                # セル結合
                ws.merge_cells(f"{column_letter}{row_th}:{next_column_letter}{row_th+1}")

        # 盤の枠を太線にします。セル結合を考えず描きます。
        ws['I7'].border = board_top_left_border
        ws['Z7'].border = board_top_right_border
        ws['I24'].border = board_bottom_left_border
        ws['Z24'].border = board_bottom_right_border
        for column_letter in xa.ColumnLetterRange(start='J', end='Z'):
            cell = ws[xa.CellAddressModel.from_code(f"{column_letter}7").to_code()]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = board_top_border)

            cell = ws[xa.CellAddressModel.from_code(f"{column_letter}24").to_code()]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = board_bottom_border)

        for row_th in range(8, 24):
            cell = ws[f"I{row_th}"]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = board_left_border)

            cell = ws[f"Z{row_th}"]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = board_right_border)
        

        # a7 = ws[f'A7']
        # a7.value = 'v香'
        # a7.border = board_top_boarder
        # a7.fill = board_fill

        # b7 = ws[f'B7']
        # b7.value = 'v桂'
        # b7.border = board_top_boarder
        # a7.fill = board_fill

        # c7 = ws[f'C7']
        # c7.value = 'v銀'
        # c7.border = board_top_boarder
        # a7.fill = board_fill

        # d7 = ws[f'D7']
        # d7.value = 'v金'
        # d7.border = board_top_boarder
        # a7.fill = board_fill

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
