import os

from openpyxl.drawing.image import Image as XlImage


class XsUtils:


    @staticmethod
    def render_piece(ws, cell_number, image_basename):
        try:
            ws.add_image(XlImage(os.path.join('./assets/img', image_basename)), cell_number)
        except FileNotFoundError as e:
            print(f'FileNotFoundError {e=} {cell_number=} {image_basename=}')
