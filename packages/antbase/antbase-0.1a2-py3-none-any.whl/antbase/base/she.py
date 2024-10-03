from typing import Any, TypedDict, NotRequired, List, Callable

from antbase import Auth, Drive, Log

class CellFormat(TypedDict):
    numberFormat:  str = "@"
    alligment:     str = "center"
    columtWidth:   int = 0
    fontSize:      int = 8

class Cell:
    types = {'empty', 'string', 'number', 'boolean', 'cellImage', 'date', 'link', 'undef'}
    def __init__(self, r: int, c : int, v: any=None, image=None, link: str=None, note: str=None, formate: CellFormat=None):
        self.r:     int = r 
        self.c:     int = c
        self.v:     any = v
        self.image: any = image
        self.link:  any = link
        self.note:  str = note
        self.formate: CellFormat = formate
        self.formula: str = None

    @property
    def type(self):
        import re
        if   self.v == None:                                                     return "empty"
        elif isinstance(self.v, str) and re.match(r'^\s*$', self.v):             return "empty"
        elif isinstance(self.v, str):                                            return "string"
        elif isinstance(self.v, (int, float)):                                   return "number"
        elif isinstance(self.v, bool):                                           return "boolean"
        elif isinstance(self.v, dict) and self.v.get('type') == 'image':         return "cellImage"
        elif isinstance(self.v, str) and re.match(r'\d{4}-\d{2}-\d{2}', self.v): return "date"
        elif isinstance(self.v, str) and self.v == "link":                       return "link"
        else: return "undef"
    
    def get(self, v: any=None, image=None, link: str=None, note: str=None, formate: CellFormat=None):
        range = f'{self.sheet_name}!R{self.r}C{self.c}'
        result = She.__service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id, ranges=range,
            fields="sheets/data/rowData/values/note"
        ).execute()
        self.note = result.get('note', '')


class Cells:
    def __init__(self, r: int, c: int, nr: int, nc: int, v: List[List[any]] ):
        self.r:    int = r 
        self.c:    int = c
        self.nr:   int = nr
        self.nc:   int = nc
        self.v:    List[List[any]]  = v
        self.type: any = "string" # She.cell_type(self)

class She:
    __service = Auth.get_sheet_service()

    def __init__(self, spreadsheet_id: str, sheet_name: str):

        self.spreadsheet_id: str  = spreadsheet_id
        self.spreadsheet:    dict = She.__service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        self.sheet:          dict = None
        self.sheet_id:       str  = None
        self.sheet_name:     str  = sheet_name

        sheets = self.spreadsheet.get('sheets', [])
        if sheet_name:
            self.sheet = sheets[0]
            for sheet in sheets:
                if sheet['properties']['title'] == sheet_name:
                    self.sheet = sheet

        self.sheet_id   = self.sheet['properties']['sheetId']
        self.sheet_name = self.sheet['properties']['title']
  
    def set_cell(self, r: int, c: int, v: any) -> None:
        ''' Установить значение ячейки'''
        range   = f'{self.sheet_name}!R{r}C{c}' 
        body    = { 'values': [[v]] }
        result  = She.__service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id, range=range, valueInputOption='RAW', body=body).execute()
        return self
    
    def get_cell(self, r: int, c: int) -> Cell:
        Log.pc(self.is_valid_range(r,c), "r,c exide sheet limit")
        ''' Получить значение ячейки'''
        range   = f'{self.sheet_name}!R{r}C{c}'
        result  = She.__service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range).execute()
        v       = result.get('values', [])
        if v:
            v = v[0][0]
            cell    = Cell(r, c, v)
        else:
            cell = Cell(r, c, None)
        return cell
    
    def is_valid_range(self, r: int, c: int) -> bool:
        ''' Проверить, что диапазон не превышает границы таблицы'''
        max_rows = self.sheet['properties']['gridProperties']['rowCount']
        max_cols = self.sheet['properties']['gridProperties']['columnCount']
        return 1 <= r <= max_rows and 1 <= c <= max_cols
    
    def get_cells(self, r: int, c: int, nr: int, nc: int) -> Cell:
        ''' Получить значения массива ячеек'''
        range   = f'{self.sheet_name}!R{r}C{c}:R{r+nr-1}C{c+nc-1}'
        result  = She.__service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range).execute()
        v       = result.get('values', [])
        cells   = Cells(r, c, nr, nc, v)
        return cells
    
    def get_all_cells(self) -> list:
        '''Получить все значения ячеек на листе'''
        max_rows = self.sheet['properties']['gridProperties']['rowCount']
        max_cols = self.sheet['properties']['gridProperties']['columnCount']
        range_name = f'{self.sheet_name}!R1C1:R{max_rows}C{max_cols}'
        result = She.__service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        return values
  
    def column_format(
            self,
            c:             int,
            header:        str=None,
            number_format: str=None,
            alignment:     str=None,
            c_width:       int=None,
            font_size:     int=None):
        """Форматирование столбца в таблице (number_format="@", alignment="CENTER", c_width=100, font_size=10)"""

        requests = []

        if header:
            requests.append({
                'updateCells': {
                    'range': {
                        'sheetId': self.sheet_id,
                        'startRowIndex': 0,        'endRowIndex': 1,
                        'startColumnIndex': c - 1, 'endColumnIndex': c
                    },
                    'rows': [{
                        'values': [{
                            'userEnteredValue': {'stringValue': header},
                            'userEnteredFormat': {
                                'textFormat': {'bold': True, 'fontSize': font_size},
                                'horizontalAlignment': alignment,
                            }
                        }]
                    }],
                    'fields': 'userEnteredValue,userEnteredFormat.textFormat,userEnteredFormat.horizontalAlignment'
                }
            })

        if number_format:
            requests.append({
                'repeatCell': {
                    'range': {
                        'sheetId': self.sheet_id,
                        'startColumnIndex': c - 1,'endColumnIndex': c
                    },
                    'cell': {
                        'userEnteredFormat': {
                            'numberFormat': {'type': 'NUMBER','pattern': number_format},
                            'horizontalAlignment': alignment
                        }
                    },
                    'fields': 'userEnteredFormat.numberFormat,userEnteredFormat.horizontalAlignment'
                }
            })

        if c_width:
            requests.append({
                'updateDimensionProperties': {
                    'range': {
                        'sheetId': self.sheet_id, 'dimension': 'COLUMNS',
                        'startIndex': c - 1, 'endIndex': c
                    },
                    'properties': { 'pixelSize': c_width},
                    'fields': 'pixelSize'
                }
            })

        body = { 'requests': requests }
        response = She.__service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()
        return response

    @staticmethod
    def get_sheet_list(file_name: str, folder_id: str, drive_id: str) -> str:
        ''' Получить список таблиц по имени файла, id папки, id диска и имени листа'''
        list = Drive.get_file_list(file_name, folder_id, drive_id, Drive.MIME_TYPE_GOOGLE_SHEET)
        return list #file_list[0]['id']

    def set_spreadsheet_name(self, name: str) -> None :
        Drive.update_file_metadata(file_id=self.spreadsheet_id, name=name)

    def get_active_key() -> str:
        ''' Получить ключ активной строки
        Предполагается, что ключ находится к первой колонке активной строки
        Если активная ячейка находится в зоне замороженных строк возвращается null
        Если значение в первой колонке активной строки не пустая строка, возвращается null'''

    def set_link(self, r: int, c: int, url: str) -> None:
        ''' Установить гиперссылку в ячейку'''
    
    def set_note(self, r: int, c: int, note: str) -> None:
        '''Устанавливает заметку в указанную ячейку'''
        range = f'{self.sheet_name}!R{r}C{c}'
        She.__service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range,
            valueInputOption='RAW',
            body={'values': [[note]]},
            fields='updates/updatedData/notes'  # Only update the notes field
        ).execute()

    def clear_note(self, r: int, c: int): self.set_note(r, c, None)

    def get_note(self, r: int, c: int) -> str:
        '''Получить заметку из указанной ячейки'''
        range = f'{self.sheet_name}!R{r}C{c}'
        result = She.__service.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id, ranges=range, fields="sheets/data/rowData/values/note"
        ).execute()
        self.note = result.get('note', '')
        return self.note


    def find_rows(self, key: str, key_col: int = 1) -> list:
        ''' Найти номера строк в массиве строк с указанным ключом в указанной колонке
            KeySheet - Лист в первой колонке которого стоит ключ,
            а строка содержит значения атрибутов с Заголовками в перывой строке
                sh     - Лист, где расположена таблица
                key    - значение Ключа
                keyCol - номер колонки, где находится ключ
                return - номера строк, с указанным ключом'''

    def get_keys(self, key_col: int=1) -> list:
        ''' Получить множество строк по ключу всех ключей в массиве строк'''

    def rename_keys(self, f: Callable[[str, str],str], key_col: int=1) -> None:
        '''Переименовать все ключи в массиве строк с помощью функции f
        f - функция переименования ключа'''

    def get_rows(self,  key: str, keyCol: int=1) -> list:
        ''' Получить массив строк с указанным ключом'''

    def delete_row(self,  r: int=1) -> None:
        '''Удалить строку с указанным номером'''
        self.delete_rows([r])
    
    def delete_rows(self, rows: list, batch_size: int = 100) -> None:
        '''Удалить строки с указанными номерами'''
        rows = sorted(rows, reverse=True)
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            requests = []
            for row in batch:
                requests.append({
                    "deleteDimension": {
                        "range": {
                            "sheetId": self.sheet_id, "dimension": "ROWS",
                            "startIndex": row - 1,    "endIndex": row
                        }
                    }
                })
            body = {'requests': requests}
            response = She.__service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheet_id, body=body).execute()

    def delete_rows_by_key(self,  key: str, keyCol: int=1) -> None:
        '''Удалить строки с указанным ключом'''

        rows = self.find_rows(key, keyCol)
        if not rows:
            return 0
        return self.delete_rows(rows)