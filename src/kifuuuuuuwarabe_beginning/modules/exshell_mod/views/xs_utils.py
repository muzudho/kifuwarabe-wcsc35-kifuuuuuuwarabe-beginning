import cshogi
import openpyxl as xl
import os

from openpyxl.drawing.image import Image as XlImage

from ....models.layer_o1o0 import SquareModel


class XsUtils:


    _piece_basename = {
        cshogi.BLACK: {
            cshogi.PAWN: 'size40x40-earth-hiyoko.png',
            cshogi.LANCE: 'size40x40-earth-inosisi.png',
            cshogi.KNIGHT: 'size40x40-earth-usagi.png',
            cshogi.SILVER: 'size40x40-earth-neko.png',
            cshogi.BISHOP: 'size40x40-earth-zou.png',
            cshogi.ROOK: 'size40x40-earth-kirin.png',
            cshogi.GOLD: 'size40x40-earth-inu.png',
            cshogi.KING: 'size40x40-earth-raion.png',
            cshogi.PROM_PAWN: 'size40x40-earth-prom-hiyoko.png',
            cshogi.PROM_LANCE: 'size40x40-earth-prom-inosisi.png',
            cshogi.PROM_KNIGHT: 'size40x40-earth-prom-usagi.png',
            cshogi.PROM_SILVER: 'size40x40-earth-prom-neko.png',
            cshogi.PROM_BISHOP: 'size40x40-earth-prom-zou.png',
            cshogi.PROM_ROOK: 'size40x40-earth-prom-kirin.png',
        },
        cshogi.WHITE: {
            cshogi.PAWN: 'size40x40-mars-hiyoko.png',
            cshogi.LANCE: 'size40x40-mars-inosisi.png',
            cshogi.KNIGHT: 'size40x40-mars-usagi.png',
            cshogi.SILVER: 'size40x40-mars-neko.png',
            cshogi.BISHOP: 'size40x40-mars-zou.png',
            cshogi.ROOK: 'size40x40-mars-kirin.png',
            cshogi.GOLD: 'size40x40-mars-inu.png',
            cshogi.KING: 'size40x40-mars-raion.png',
            cshogi.PROM_PAWN: 'size40x40-mars-prom-hiyoko.png',
            cshogi.PROM_LANCE: 'size40x40-mars-prom-inosisi.png',
            cshogi.PROM_KNIGHT: 'size40x40-mars-prom-usagi.png',
            cshogi.PROM_SILVER: 'size40x40-mars-prom-neko.png',
            cshogi.PROM_BISHOP: 'size40x40-mars-prom-zou.png',
            cshogi.PROM_ROOK: 'size40x40-mars-prom-kirin.png',
        }
    }


    @staticmethod
    def render_piece_1(ws, cell_address, color, pt):
        if pt == cshogi.NONE:    # 空きマス
            return

        try:
            image_basename = XsUtils._piece_basename[color][pt]
        except Exception as ex:
            raise ValueError(f"{color=} {pt=} {ex=}")
        
        try:
            ws.add_image(XlImage(os.path.join('./assets/img', image_basename)), cell_address)
        except FileNotFoundError as e:
            print(f'FileNotFoundError {e=} {cell_address=} {image_basename=}')


    @staticmethod
    def render_piece_2(ws, sq, color, pt):
        #print(f"{sq=} {color=} {pt=}")
        if pt == cshogi.NONE:    # 空きマス
            return

        try:
            image_basename = XsUtils._piece_basename[color][pt]
        except Exception as ex:
            raise ValueError(f"{color=} {pt=} {ex=}")
            
        sq_obj = SquareModel(sq)
        column_th = 10 + (8 - sq_obj.file) * 2
        row_th = 6 + sq_obj.rank * 2
        column_letter = xl.utils.get_column_letter(column_th)
        cell_address = f"{column_letter}{row_th}"

        try:
            ws.add_image(XlImage(os.path.join('./assets/img', image_basename)), cell_address)
        except FileNotFoundError as e:
            print(f'FileNotFoundError {e=} {cell_address=} {image_basename=}')
