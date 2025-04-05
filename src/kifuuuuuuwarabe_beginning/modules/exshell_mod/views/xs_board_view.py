import openpyxl as xl


class XsBoardView():


    @staticmethod
    def render(gymnasium):
        """描画。
        """

        # 設定
        canvas_width = 100
        canvas_height = 100

        # ワークブックを新規生成
        wb = xl.Workbook()

        # ワークシート
        ws = wb['Sheet']

        # 方眼紙を作成します。
        # 行の横幅
        for column_th in range(1, canvas_width+1):
            column_letter = xl.utils.get_column_letter(column_th)
            ws.column_dimensions[column_letter].width = 2.7    # 2.7 characters = about 30 pixels

        # 列の高さ
        for row_th in range(1, canvas_height+1):
            ws.row_dimensions[row_th].height = 15    # 15 points = about 30 pixels

        ws[f'A1'].value = 'next'
        ws[f'C1'].value = "'xxx"
        ws[f'E1'].value = 'move(s)'
        ws[f'G1'].value = 'black'
        ws[f'I1'].value = 'repetition'
        ws[f'M1'].value = "'-"

        ws[f'A3'].value = '飛'
        ws[f'B3'].value = '角'
        ws[f'C3'].value = '金'
        ws[f'D3'].value = '銀'
        ws[f'E3'].value = '桂'
        ws[f'F3'].value = '香'
        ws[f'G3'].value = '歩'

        ws[f'A4'].value = '0'
        ws[f'B4'].value = '0'
        ws[f'C4'].value = '0'
        ws[f'D4'].value = '0'
        ws[f'E4'].value = '0'
        ws[f'F4'].value = '0'
        ws[f'G4'].value = '0'

        ws[f'A6'].value = '9'
        ws[f'B6'].value = '8'
        ws[f'C6'].value = '7'
        ws[f'D6'].value = '6'
        ws[f'E6'].value = '5'
        ws[f'F6'].value = '4'
        ws[f'G6'].value = '3'
        ws[f'H6'].value = '2'
        ws[f'I6'].value = '1'

        ws[f'A7'].value = 'v香'
        ws[f'B7'].value = 'v桂'
        ws[f'C7'].value = 'v銀'
        ws[f'D7'].value = 'v金'
        ws[f'E7'].value = 'v玉'
        ws[f'F7'].value = 'v金'
        ws[f'G7'].value = 'v銀'
        ws[f'H7'].value = 'v桂'
        ws[f'I7'].value = 'v香'

        ws[f'B8'].value = 'v飛'
        ws[f'H8'].value = 'v角'

        ws[f'A9'].value = 'v歩'
        ws[f'B9'].value = 'v歩'
        ws[f'C9'].value = 'v歩'
        ws[f'D9'].value = 'v歩'
        ws[f'E9'].value = 'v歩'
        ws[f'F9'].value = 'v歩'
        ws[f'G9'].value = 'v歩'
        ws[f'H9'].value = 'v歩'
        ws[f'I9'].value = 'v歩'

        ws[f'A13'].value = '歩'
        ws[f'B13'].value = '歩'
        ws[f'C13'].value = '歩'
        ws[f'D13'].value = '歩'
        ws[f'E13'].value = '歩'
        ws[f'F13'].value = '歩'
        ws[f'G13'].value = '歩'
        ws[f'H13'].value = '歩'
        ws[f'I13'].value = '歩'

        ws[f'B14'].value = '飛'
        ws[f'H14'].value = '角'

        ws[f'A15'].value = '香'
        ws[f'B15'].value = '桂'
        ws[f'C15'].value = '銀'
        ws[f'D15'].value = '金'
        ws[f'E15'].value = '玉'
        ws[f'F15'].value = '金'
        ws[f'G15'].value = '銀'
        ws[f'H15'].value = '桂'
        ws[f'I15'].value = '香'

        # ワークブック保存
        gymnasium.exshell.save_workbook(wb=wb)

        # エクセル開く
        gymnasium.exshell.open_virtual_display()

        line = input('何か入力してください。例： y\n')
        print() # 空行

        # エクセル閉じる
        gymnasium.exshell.close_virtual_display()
