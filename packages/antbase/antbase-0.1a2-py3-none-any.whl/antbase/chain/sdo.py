
from antbase import Db, Drive
from antbase import She as S

class Sdo:
    @staticmethod
    def update(_sdo, o):
        """
        Обновить словарный объект в хранилище
        :param _sdo: Имя словарного объекта
        :param o: Объект для обновления
        :return: Результат обновления
        """
        return Db.update_one('Sdo', 'sdo', {'_sdo': _sdo}, {'$set': o})

    @staticmethod
    def get(_sdo):
        """
        Загрузить словарный объект из базы данных
        :param _sdo: Имя словарного объекта
        :return: Словарный объект или None
        """
        return Db.find_one('Sdo', 'sdo', {'_sdo': _sdo})

    @staticmethod
    def upload():
        """
        Загрузить словарные объекты из таблиц (например, Google Sheets) в базу данных
        :return: Список документов для загрузки в базу данных
        """
        documents = []
        ss = S.get_spreadsheet(Drive.dictionary)
        sheets = ss.get_sheets()
        
        for sh in sheets:
            sh_name = sh.get_sheet_name()
            if sh_name.startswith("_"):
                continue
            
            nf = sh.get_frozen_rows()
            rs = 1 + nf
            header = rs > 1
            nr = sh.get_last_row() - (rs - 1)
            nc = sh.get_last_column()
            v = sh.get_range(rs, 1, nr, nc).get_values()
            name = sh_name  # Объект всегда называется по имени листа
            h = sh.get_range(1, 1, 1, nc).get_values()[0] if header else None
            sdo = {'_sdo': name}
            
            case_a = header and h[0] == "_key"
            case_b = header and h[0] == "_list"
            case_c = not header
            
            if case_a or case_c:
                sdo['_keys'] = [row[0] for row in v if row[0]]
            
            if case_a:
                for row in v:
                    key = row[0]
                    if key:
                        sdo[key] = {}
                        for c in range(1, nc):
                            property = h[c]
                            value = row[c]
                            if property and value:
                                sdo[key][property] = value
            
            if case_b:
                for c in range(nc):
                    property = h[c]
                    if property:
                        sdo[property] = [row[c] for row in v]
            
            documents.append(sdo)
        
        return documents