import openpyxl as xl
import pyxlart as xa
import re

from openpyxl.styles import PatternFill, Font
from openpyxl.styles.borders import Border, Side
from openpyxl.styles.alignment import Alignment


class XsBoardView():


    @staticmethod
    def render(gymnasium):
        """描画。
        """

        # 盤のマスのセル結合一覧
        columns_of_start    = ['I', 'K', 'M', 'O', 'Q', 'S', 'U', 'W', 'Y']
        columns_of_end      = ['J', 'L', 'N', 'P', 'R', 'T', 'V', 'X', 'Z']
        rows_of_start       = [5, 7, 9, 11, 13, 15, 17, 19, 21]
        rows_of_end         = [6, 8, 10, 12, 14, 16, 18, 20, 22]

        # 色
        BLACK = '000000'
        BOARD_COLOR = 'DAEEF3'
        HEADER_1_COLOR = 'FCD5B4'
        HEADER_2_COLOR = 'FDE9D9'

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
        header_1_fill = PatternFill(patternType='solid', fgColor=HEADER_1_COLOR)
        header_2_fill = PatternFill(patternType='solid', fgColor=HEADER_2_COLOR)

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
        ws['E2'].value = "'xxx"
        ws['G2'].value = 'move(s)'
        ws['K2'].value = 'blACK'
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

        # ws[f'A3'].value = '飛'
        # ws[f'B3'].value = '角'
        # ws[f'C3'].value = '金'
        # ws[f'D3'].value = '銀'
        # ws[f'E3'].value = '桂'
        # ws[f'F3'].value = '香'
        # ws[f'G3'].value = '歩'

        # ws[f'A4'].value = '0'
        # ws[f'B4'].value = '0'
        # ws[f'C4'].value = '0'
        # ws[f'D4'].value = '0'
        # ws[f'E4'].value = '0'
        # ws[f'F4'].value = '0'
        # ws[f'G4'].value = '0'

        # ws[f'A6'].value = '9'
        # ws[f'B6'].value = '8'
        # ws[f'C6'].value = '7'
        # ws[f'D6'].value = '6'
        # ws[f'E6'].value = '5'
        # ws[f'F6'].value = '4'
        # ws[f'G6'].value = '3'
        # ws[f'H6'].value = '2'
        # ws[f'I6'].value = '1'

        # 枠の辺を塗り潰し
        for column_letter in xa.ColumnLetterIterator(start='H', end='AB'):
            #print(f"D-117: {column_letter=}")
            # H4 ～ AA4
            cell_address = xa.CellAddressModel.from_code(f"{column_letter}4")
            ws[cell_address.to_code()].fill = board_fill

            # H23～AA23
            cell_address = xa.CellAddressModel.from_code(f"{column_letter}23")
            ws[cell_address.to_code()].fill = board_fill

        for row_th in range(5, 23):
            # H5～H22
            cell_address = xa.CellAddressModel.from_code(f"H{row_th}")
            ws[cell_address.to_code()].fill = board_fill

            # AA5～AA22
            cell_address = xa.CellAddressModel.from_code(f"AA{row_th}")
            ws[cell_address.to_code()].fill = board_fill

        # 盤の各マス
        for y in range(0, 9):
            for x in range(0, 9):
                column_of_start = columns_of_start[x]
                column_of_end = columns_of_end[x]
                row_of_start = rows_of_start[y]
                row_of_end = rows_of_end[y]

                # セル設定
                cell = ws[f"{column_of_start}{row_of_start}"]
                cell.border = board_cell_border
                cell.fill = board_fill

                # セル結合
                ws.merge_cells(f"{column_of_start}{row_of_start}:{column_of_end}{row_of_end}")

        # 盤の枠を太線にします。セル結合を考えず描きます。
        ws['I5'].border = board_top_left_border
        ws['Z5'].border = board_top_right_border
        ws['I22'].border = board_bottom_left_border
        ws['Z22'].border = board_bottom_right_border
        for column_letter in xa.ColumnLetterIterator(start='J', end='Z'):
            cell = ws[xa.CellAddressModel.from_code(f"{column_letter}5").to_code()]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = board_top_border)

            cell = ws[xa.CellAddressModel.from_code(f"{column_letter}22").to_code()]
            cell.border = xa.BorderLogic.add(
                    base        = cell.border,
                    addition    = board_bottom_border)

        for row_th in range(6, 22):
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
