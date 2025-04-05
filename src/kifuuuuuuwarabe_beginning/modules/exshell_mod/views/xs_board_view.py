import openpyxl as xl


class XsBoardView():


    @staticmethod
    def render(gymnasium):
        # ワークブックを新規生成
        wb = xl.Workbook()

        # ワークシート
        ws = wb['Sheet']

        cell = ws[f'A1']
        cell.value = "Hello, world!"

        # ワークブック保存
        gymnasium.exshell.save_workbook(wb=wb)

        # エクセル開く
        gymnasium.exshell.open_virtual_display()

        line = input('何か入力してください。例： y')
        print() # 空行

        # エクセル閉じる
        gymnasium.exshell.close_virtual_display()
