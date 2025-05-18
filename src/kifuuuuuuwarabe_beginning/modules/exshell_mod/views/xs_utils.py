import cshogi
import openpyxl as xl
import os

from openpyxl.drawing.image import Image as XlImage

from ....models.layer_o1o0 import SquareModel


class XsUtils:


    @staticmethod
    def render_piece_1(ws, cell_number, image_basename):
        try:
            ws.add_image(XlImage(os.path.join('./assets/img', image_basename)), cell_number)
        except FileNotFoundError as e:
            print(f'FileNotFoundError {e=} {cell_number=} {image_basename=}')


    _piece_basename = {
        cshogi.BLACK: {
            cshogi.PAWN: 'hiyoko-earth-40x40.png',
            cshogi.LANCE: 'inosisi-earth-40x40.png',
            cshogi.KNIGHT: 'usagi-earth-40x40.png',
            cshogi.SILVER: 'neko-earth-40x40.png',
            cshogi.BISHOP: 'zou-earth-40x40.png',
            cshogi.ROOK: 'kirin-earth-40x40.png',
            cshogi.GOLD: 'inu-earth-40x40.png',
            cshogi.KING: 'raion-earth-40x40.png',
            cshogi.PROM_PAWN: 'hiyoko-prom-earth-40x40.png',
            cshogi.PROM_LANCE: 'inosisi-prom-earth-40x40.png',
            cshogi.PROM_KNIGHT: 'usagi-prom-earth-40x40.png',
            cshogi.PROM_SILVER: 'neko-prom-earth-40x40.png',
            cshogi.PROM_BISHOP: 'zou-prom-earth-40x40.png',
            cshogi.PROM_ROOK: 'kirin-prom-earth-40x40.png',
        },
        cshogi.WHITE: {
            cshogi.PAWN: 'hiyoko-mars-40x40.png',
            cshogi.LANCE: 'inosisi-mars-40x40.png',
            cshogi.KNIGHT: 'usagi-mars-40x40.png',
            cshogi.SILVER: 'neko-mars-40x40.png',
            cshogi.BISHOP: 'zou-mars-40x40.png',
            cshogi.ROOK: 'kirin-mars-40x40.png',
            cshogi.GOLD: 'inu-mars-40x40.png',
            cshogi.KING: 'raion-mars-40x40.png',
            cshogi.PROM_PAWN: 'hiyoko-prom-mars-40x40.png',
            cshogi.PROM_LANCE: 'inosisi-prom-mars-40x40.png',
            cshogi.PROM_KNIGHT: 'usagi-prom-mars-40x40.png',
            cshogi.PROM_SILVER: 'neko-prom-mars-40x40.png',
            cshogi.PROM_BISHOP: 'zou-prom-mars-40x40.png',
            cshogi.PROM_ROOK: 'kirin-prom-mars-40x40.png',
        }
    }

    @staticmethod
    def render_piece_2(ws, sq, color, pt):
        if color == cshogi.NONE or pt == cshogi.NONE:    # 空きマス
            return

        try:
            image_basename = XsUtils._piece_basename[color][pt]
        except Exception as ex:
            raise ValueError(f"{color=} {pt=} {ex=}")
            
        sq_obj = SquareModel(sq)
        column_th = 10 + sq_obj.file * 2
        row_th = 6 + sq_obj.rank * 2
        column_letter = xl.utils.get_column_letter(column_th)
        cell_address = f"{column_letter}{row_th}"

        try:
            ws.add_image(XlImage(os.path.join('./assets/img', image_basename)), cell_address)
        except FileNotFoundError as e:
            print(f'FileNotFoundError {e=} {cell_address=} {image_basename=}')
