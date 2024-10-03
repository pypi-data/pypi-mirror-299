# Библиотека работы с изображениями
import base64
import requests

class Im:
    # Палитра Цветов
    RED          = "#ff0000"
    LIGHT_GREEN  = "#c9f4d3"
    GREY         = "#b2b4b4"
    LIGHT_GREY   = "#dedcdf"
    BLUE         = "#1553ba"
    MAGENTA      = "#902aa5"
    BLACK        = "0000000"

    # jpegURI по jpegURL
    @staticmethod
    def jpegURI(jpegURL):
        response = requests.get(jpegURL)
        if response.status_code == 200:
            jpeg_data = response.content
            base64_encoded = base64.b64encode(jpeg_data).decode('utf-8')
            return "data:image/jpeg;base64," + base64_encoded
        else:
            return None

    # jpegURI по fileId нужен ли???
    @staticmethod
    def jpegURIbyFileId(fileId, drive_service):
        # Получить ссылку на миниатюру файла из Google Drive
        file = drive_service.files().get(fileId=fileId, fields='thumbnailLink').execute()
        thumbnailLink = file.get('thumbnailLink')
        return Im.jpegURI(thumbnailLink)

    # Размер Изображения
    @staticmethod
    def jpegSize(im):
        # im - это объект Image из библиотеки PIL
        return im.size  # (width, height)

    # Проверка, является ли объект ключевым (имеет ли необходимые ключи)
    @staticmethod
    def isKeyObject(obj, keys):
        return all(key in obj for key in keys)

    # Получить Изображения для вставки в Ячейку
    @staticmethod
    def cellImage(image):
        required_keys = ['uri', 'name', 'id']
        if image and Im.isKeyObject(image, required_keys):
            # Вставка изображения в ячейку с помощью формулы IMAGE
            formula = '=IMAGE("{}")'.format(image['uri'])
            return formula
        return None

    # Вставить изображния в ячейку
    @staticmethod
    def toCell(sh, r, c, image):
        formula = Im.cellImage(image)
        if formula:
            # Предполагается, что sh - объект листа, и мы можем использовать метод update_cells
            sh.update_cell(r, c, formula)

    # Извлечь изображение из ячейки
    @staticmethod
    def fromCell(sh, r, c):
        # Предполагается, что sh - объект листа, и мы можем получить формулу ячейки
        cell = sh.cell(r, c)
        return cell.formula
