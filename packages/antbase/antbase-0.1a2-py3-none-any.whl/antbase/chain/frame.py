from google import Drive as Io
from google import She as S

from antbase import Im, Meta

class Frame:
    @staticmethod
    def entangle(sko):
        """
        Загрузка метаданных и спутывание sko с фреймом.
        """
        sko['_frame']['image']       = Meta.image_frame(sko['_sko'])
        sko['_frame']['reg']         = Meta.reg_frame(sko['_sko'], "ui")
        sko['_frame']['doc']         = Meta.doc_frame(sko['_sko'], "ui")
        sko['_frame']['doc_archive'] = Meta.doc_frame(sko['_sko'], "archive")
        sko['_frame']['reg_archive'] = Meta.reg_frame(sko['_sko'], "archive")

    class image:
        @staticmethod
        def link(sko):
            frame = sko['_frame']['image']
            file_list = Io.get_file_list(sko['_key'], frame['_folder'], frame['_drive'], 'image/jpeg')
            if not file_list:
                return None
            im_list = []
            for f in file_list:
                if f.get('hasThumbnail'):
                    im_list.append({
                        'id': f['id'],
                        'name': f['name'],
                        'uri': Im.jpeg_uri(f['thumbnailLink']),
                        'url': f['thumbnailLink'],
                        'w': f['imageMediaMetadata']['width'],
                        'h': f['imageMediaMetadata']['height'],
                        'size': f['size']
                    })
            sko['_images'] = im_list
            sko['_image'] = im_list[0] if im_list else None
            return sko

    class reg:
        @staticmethod
        def exchange(operation, sko, frame=None):
            """
            Выполнение операции над фреймом ("GET" | "SET" | "UPDATE").
            """
            frame = frame or sko['_frame']['reg']
            sheets = [sheet for sheet in frame.keys() if not sheet.startswith('_')]
            ss = S.get_spreadsheet(frame['_fileId'])
            for sh_name in sheets:
                sh = ss.get_sheet_by_name(sh_name)
                Frame.reg.perform_operation(operation, sh, sko)

        @staticmethod
        def perform_operation(operation, sh, sko):
            """
            Вспомогательный метод для выполнения операции над регистрами.
            """
            if operation == "GET":
                Frame.reg.GET(sh, sko)
            elif operation == "SET":
                Frame.reg.SET(sh, sko)
            elif operation == "UPDATE":
                Frame.reg.UPDATE(sh, sko)

        @staticmethod
        def GET(sh, sko):
            frame = sko['_frame']['reg']
            sh_name = sh.get_name()
            key_col = frame.get(sh_name, {}).get("keyCol", 1)
            rs = S.find_rows(sh, sko['_key'], key_col)
            for r in rs:
                for c, fn in frame[sh_name].items():
                    if c > 0:
                        S.set_cell(sko, fn, S.get_cell(sh, r, c))

        @staticmethod
        def SET(sh, sko):
            frame = sko['_frame']['reg']
            sh_name = sh.get_name()
            key_col = frame.get(sh_name, {}).get("keyCol", 1)
            r = sh.get_last_row() + 1
            S.delete_rows(sh, sko['_key'], key_col)
            for c, fn in frame[sh_name].items():
                if c > 0: S.set_cell(sh, r, c, S.get_value_from_object(sko, fn))

    class doc:
        @staticmethod
        def create(sko):
            """
            Создать пустой документ на основе шаблона и спутать его с объектом sko.
            """
            if sko['_docId']:
                Io.delete_file(sko['_docId'])
            ss = S.get_spreadsheet(sko['_frame']['doc']['_template']).copy(sko['_key'])
            sko['_docId'] = ss.get_id()
            sko['_docUrl'] = ss.get_url()
            folder = Io.get_folder_by_id(sko['_frame']['doc']['_folder'])
            Io.move_file(sko['_docId'], folder)
            Io.update_file_props(sko['_docId'], {
                '_sko': sko['_sko'],
                '_key': sko['_key'],
                '_id': sko['_id'],
                '_version': sko['_version']
            })

        @staticmethod
        def remove(sko):
            """
            Удалить спутанный документ.
            """
            if sko['_docId']:
                Io.delete_file(sko['_docId'])
                sko['_docId'] = None
                sko['_docUrl'] = None