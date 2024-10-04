from datetime import datetime, timedelta

class Dt:
    # Константы
    DAY_TO_MS     = 86400000        # Мультипликатор для перевода дней в миллисекунды
    SH_DATE_SHIFT = -2209161600000  # "1899-12-30T00:00:00.000Z"

    # Работа с Tick
    @staticmethod
    def tick_now(): return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def tick(js_date=None):
        if js_date:
            return int(js_date.timestamp() * 1000)
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def tick_min(tick): return tick // 1000 // 60

    @staticmethod
    def tick_sec(tick): return tick // 1000

    # Преобразование Дат в разные форматы
    @staticmethod
    def sh_js(sh_date):   return datetime.utcfromtimestamp((sh_date * Dt.DAY_TO_MS + Dt.SH_DATE_SHIFT) / 1000)

    @staticmethod
    def iso_js(iso_date):   return datetime.fromisoformat(iso_date)

    @staticmethod
    def iso_sh(iso_date):  return (datetime.fromisoformat(iso_date).timestamp() * 1000 - Dt.SH_DATE_SHIFT) / Dt.DAY_TO_MS

    @staticmethod
    def js_sh(js_date): return (js_date.timestamp() * 1000 - Dt.SH_DATE_SHIFT) / Dt.DAY_TO_MS

    @staticmethod
    def sh_iso(sh_date): return Dt.sh_js(sh_date).isoformat()

    @staticmethod
    def js_iso(js_date):  return js_date.isoformat()

    @staticmethod
    def js_db(js_date):  return {"$date": {"$numberLong": str(int(js_date.timestamp() * 1000))}}

    @staticmethod
    def db_js(db_date):  return datetime.utcfromtimestamp(int(db_date["$date"]["$numberLong"]) / 1000)

    @staticmethod
    def string_iso(s):    return datetime.fromisoformat(Dt.norm(s)).isoformat() if s else None

    @staticmethod
    def string_js(s):  return datetime.fromisoformat(Dt.norm(s)) if s else None

    @staticmethod
    def js_thai(js_date):  return js_date.replace(year=js_date.year + 543)

    # Строки Iso Date преобразуются в дату Python
    @staticmethod
    def json_iso_js(obj):
        for key, value in obj.items():
            if isinstance(value, dict):
                Dt.json_iso_js(value)
            elif isinstance(value, str) and Dt.is_iso_date(value):
                obj[key] = datetime.fromisoformat(value)

    # Проверка на соответствие ISO Date
    @staticmethod
    def is_iso_date(string):
        try:
            datetime.fromisoformat(string)
            return True
        except ValueError:
            return False

    # В строке ISO Date меняет дни и месяцы местами
    @staticmethod
    def norm(string_date):
        import re
        re_pattern = r'^(\d{1,2})(\/|\.)(\d{1,2})(\/|\.)(\d{2})?(\d{2})$'
        match = re.match(re_pattern, string_date)
        if match:
            day, _, month, _, year_prefix, year_suffix = match.groups()
            year = f"20{year_suffix}" if year_prefix is None else f"{year_prefix}{year_suffix}"
            return f"{year}-{month}-{day}"
        raise ValueError(f"Dt.norm: Wrong date syntax {string_date}")

    # Ячейка должна содержать дату. Преобразуем.
    @staticmethod
    def date_cell(v):
        try:
            if isinstance(v, datetime):
                return v
            elif isinstance(v, (int, float)):
                return Dt.sh_js(v)
            elif isinstance(v, str):
                return Dt.string_js(v)
            return None
        except Exception as e:
            raise ValueError(f"Dt.dateCell: Wrong date syntax ({v}) {type(v)}")

    # Корректировка формата даты
    @staticmethod
    def correction(v):
        try:
            if isinstance(v, str):
                return Dt.string_iso(v)
            elif isinstance(v, (int, float)):
                return Dt.sh_iso(v)
            elif isinstance(v, datetime):
                return Dt.js_iso(v)
            return v
        except Exception as e:
            raise ValueError(f"Dt.correction: Can't make Date Syntax Correction ({v}) {type(v)}")

### Описание функциональности:
# 1. **Работа с `Tick`**:
#    - `tick_now()` возвращает текущее время в миллисекундах.
#    - `tick(js_date)` принимает объект `datetime` и возвращает его время в миллисекундах.
#    - `tick_min(tick)` и `tick_sec(tick)` преобразуют миллисекунды в минуты и секунды.

# 2. **Преобразование дат**:
#    - Функции, такие как `sh_js()`, `iso_js()`, и `js_sh()`, выполняют преобразования между различными форматами дат, включая формат `sheet`, `ISO`, и JavaScript (в миллисекундах).
# 
# 3. **Работа с ISO форматами**:
#    - Функция `string_iso()` и `string_js()` нормализуют строковые даты в формат `ISO` или `datetime`.

# 4. **Корректировка и нормализация дат**:
#    - Функция `correction(v)` корректирует формат даты в зависимости от типа значения, переданного в `v`.