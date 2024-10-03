from antbase import F, R, K

class Metadata:
    sn = []             # Текущее значение Сериального Номера
    keySyntax = []      # Синтаксис ключа _key соответствующего _sko
    skoBody = []        # Структура данных _sko
    imageFrames = []    # Дефиниция Фреймов Изображений
    regFrames = []      # Дефиниция Фреймов Регистров
    docFrames = []      # Дефиниция Фреймов Документов

# sn
Metadata.sn = [
    {"_metaType": "serialNumber", "_sko": "cjob",    "_sn": 1078},
    {"_metaType": "serialNumber", "_sko": "order",   "_sn": 8007},
    {"_metaType": "serialNumber", "_sko": "person",  "_sn": 13},
    {"_metaType": "serialNumber", "_sko": "trigger", "_sn": 79}
]

# keySyntax
Metadata.keySyntax = [
    {"_metaType": "keySyntax", "_sko": "cjob",   "key": {"prefix": "c", "suffix": "", "type": "DL1D3", "syntax": R.cjob,   "snMin": 1, "snMax": K.MAX["DL1D3"]}},
    {"_metaType": "keySyntax", "_sko": "pjob",   "key": {"prefix": "p", "suffix": "", "type": "DL1D3", "syntax": R.pjob,   "snMin": 1, "snMax": K.MAX["DL1D3"]}},
    {"_metaType": "keySyntax", "_sko": "djob",   "key": {"prefix": "d", "suffix": "", "type": "DL1D3", "syntax": R.djob,   "snMin": 1, "snMax": K.MAX["DL1D3"]}},
    {"_metaType": "keySyntax", "_sko": "sjob",   "key": {"prefix": "s", "suffix": "", "type": "DL1D3", "syntax": R.sjob,   "snMin": 1, "snMax": K.MAX["DL1D3"]}},
    {"_metaType": "keySyntax", "_sko": "jjob",   "key": {"prefix": "j", "suffix": "", "type": "DL1D3", "syntax": R.jjob,   "snMin": 1, "snMax": K.MAX["DL1D3"]}},
    {"_metaType": "keySyntax", "_sko": "order",  "key": {"prefix": "o", "suffix": "", "type": "DL1D3", "syntax": R.order,  "snMin": 1, "snMax": K.MAX["DL1D3"]}},
    {"_metaType": "keySyntax", "_sko": "person", "key": {"prefix": "e", "suffix": "", "type": "D3",    "syntax": R.person, "snMin": 1, "snMax": K.MAX["D3"]}},
    {"_metaType": "keySyntax", "_sko": "trigger","key": {"prefix": "T", "suffix": "", "type": "L4",    "syntax": R.trigger,"snMin": 1, "snMax": K.MAX["L4"]}}
]

# skoBody
Metadata.skoBody = [
    {
        "_metaType": "skoBody",
        "_sko": "cjob",
        "body": {
            "alloy": None,
            "date": None,
            "total": {"ingridients": 0, "cast": 0, "dust": 0, "scrap": 0, "balance": 0, "pjobs": 0, "partsQ": 0, "partsW": 0},
            "ingridient": [],  # [ {ingridient:"Au750W_Pd", weight: 0.0} ]
            "cast": [],  # [ 12.2, 125.44 ]
            "dust": [],  # [ 12.1, 125.44 ]
            "scrap": [],  # [ 12.3, 125.44 ]
            "pjobs": [],
            "partsQ": [],
            "partsW": [],
            "comments": []
        }
    },
    {
        "_metaType": "skoBody",
        "_sko": "person",
        "body": {
            "idOld": None,
            "prefix": None,
            "fname": None,
            "sname": None,
            "name": None,
            "nameth": None,
            "position": None,
            "type": None,
            "department": None,
            "status": None,
            "sdate": None,
            "sdateth": None,
            "email": None,
            "doer": None,
            "email2": None,
            "manager": None,
            "idCard": None,
            "hPhone": None,
            "mPhone": None,
            "wPhone": None,
            "nick": None,
            "fdate": None
        }
    },
    {
        "_metaType": "skoBody",
        "_sko": "order",
        "body": {
            "order": None,
            "model": None,
            "parent": None,
            "customer": None,
            "brand": None,
            "endUser": None,
            "kind": None,
            "name": None,
            "collection": None,
            "quantity": None,
            "comment": None,
            "payCond": None,
            "urgency": None,
            "targetDate": None,
            "targetPlace": None,
            "shipTerm": None,
            "orderDate": None,
            "finishDate": None
        }
    }
]

# imageFrames
Metadata.imageFrames = [
    {"_metaType": "imageFrame", "_sko": "cjob",   "_type": "imageFolder", "_drive": F.CASTING, "_folder": F.Cjob_im},
    {"_metaType": "imageFrame", "_sko": "order",  "_type": "imageFolder", "_drive": F.ANT,     "_folder": F.Order_im},
    {"_metaType": "imageFrame", "_sko": "person", "_type": "imageFolder", "_drive": F.ANT,     "_folder": F.Person_im}
]

# regFrames
Metadata.regFrames = [
    {
        "_metaType": "regFrame", "_sko": "cjob", "_name": "ui", "_lastVersion": True, "_version": 1, "_type": "sheetRegister", "_fileId": F.casting,
        "cjob": {
            1: "_key",
            2: "caster",
            3: "alloy",
            4: "date",
            5: "total.ingridients",
            6: "total.cast",
            7: "total.dust",
            8: "total.scrap",
            9: "total.balance"
        }
    },
    {
        "_metaType": "regFrame", "_sko": "cpart", "_name": "ui", "_lastVersion": True, "_version": 1, "_type": "sheetRegister", "_fileId": F.casting,
        "cparts": {
            1: "_key",
            2: "cjob",
            3: "date",
            4: "alloy",
            5: "pjob",
            6: "partsW",
            7: "partsQ",
            8: "comment"
        }
    },
    {
        "_metaType": "regFrame", "_sko": "order", "_name": "ui", "_lastVersion": True, "_version": 1, "_type": "sheetRegister", "_fileId": F.orders,
        "order": {
            1: "_key",
            2: "model",
            3: "parent",
            4: "customer",
            5: "brand",
            6: "endUser",
            7: "kind",
            8: "name",
            9: "collection",
            10: "quantity",
            11: "comment",
            12: "payCond",
            13: "urgency",
            14: "targetDate",
            15: "targetPlace",
            16: "shipTerm",
            17: "orderDate",
            18: "shipDate"
        }
    },
]

# docFrames
Metadata.docFrames = [
    {
        "_metaType": "docFrame", "_sko": "cjob", "_name": "ui", "_lastVersion": True, "_version": 3, "_type": "sheetFolder",
        "_drive": F.CASTING, "_folder": F.Casting, "_template": F.cjobTemplate,
        "im": {"_images": {"t": "rowIm", "rc": [1, 1, 1, 8], "h": ["images"]}},
        "cjob": {
            "alloy": {"t": "cell", "rc": [2, 2, 1, 1], "h": ["alloy:castAlloy"]},
            "_key": {"t": "cell", "rc": [2, 3, 1, 1], "h": [f"cjob:{R.cjob}"]},
            "_image": {"t": "cellIm", "rc": [3, 2, 1, 1], "h": ["image"]},
            "date": {"t": "cell", "rc": [2, 4, 1, 1], "h": ["date:date:Dt.dateCell"]},
            "caster": {"t": "cell", "rc": [2, 5, 1, 1], "h": ["caster:casterList"]},
            "invoice": {"t": "cell", "rc": [2, 6, 1, 1], "h": ["invoice"]},
            "ingridient": {"t": "mapSum", "rc": [10, 2, 16, 2], "h": ["ingridient:", "weight"]},
            "cast": {"t": "cell", "rc": [6, 4, 1, 1], "h": ["cast"]},
            "dust": {"t": "col", "rc": [10, 5, 16, 1], "h": ["dust"]},
            "scrap": {"t": "col", "rc": [10, 6, 16, 1], "h": ["scrap"]},
            "pjobs": {"t": "col", "rc": [10, 7, 16, 1], "h": [f"pjobs:{R.cjob}"]},
            "partsQ": {"t": "col", "rc": [10, 8, 16, 1], "h": ["partsQ"]},
            "partsW": {"t": "col", "rc": [10, 9, 16, 1], "h": ["partsW"]},
            "comments": {"t": "col", "rc": [10, 10, 16, 1], "h": ["comments"]}
        }
    },
    {
        "_metaType": "docFrame", "_sko": "cjob", "_name": "archive", "_lastVersion": True, "_version": 2, "_type": "sheetFolder",
        "_drive": F.CASTING, "_folder": F.Cjob_arch, "_template": F.cjobTemplate,
        "cjob": {
            "alloy": {"t": "cell", "rc": [3, 1, 1, 1], "h": ["alloy"]},
            "_key": {"t": "cell", "rc": [1, 11, 1, 1], "h": [f"cjob:{R.cjob}"]},
            "_image": {"t": "cellIm", "rc": [1, 11, 1, 1], "h": ["image"]},
            "date": {"t": "cell", "rc": [1, 3, 1, 1], "h": ["date:date:Dt.dateCell"]},
            "caster": {"t": "cell", "rc": [1, 11, 1, 1], "h": ["caster:casterList"]},
            "invoice": {"t": "cell", "rc": [1, 11, 1, 1], "h": ["invoice"]},
            "ingridient": {"t": "mapSum", "rc": [4, 2, 16, 2], "h": ["ingridient", "weight"]},
            "cast": {"t": "cell", "rc": [3, 4, 1, 1], "h": ["cast"]},
            "dust": {"t": "col", "rc": [4, 5, 16, 1], "h": ["dust"]},
            "scrap": {"t": "col", "rc": [4, 6, 16, 1], "h": ["scrap"]},
            "partsW": {"t": "col", "rc": [4, 7, 16, 1], "h": ["partsW"]},
            "partsQ": {"t": "col", "rc": [4, 8, 16, 1], "h": ["partsQ"]},
            "pjobs": {"t": "col", "rc": [4, 10, 16, 1], "h": ["pjobs::pjobNorm"]},
            "comments": {"t": "col", "rc": [4, 11, 16, 1], "h": ["comments"]}
        }
    },
    {
        "_metaType": "docFrame", "_sko": "order", "_name": "ui", "_lastVersion": True, "_version": 12, "_type": "sheetFolder",
        "_drive": F.CASTING, "_folder": F.Casting, "_template": F.orderTemplate,
        "order": {
            "_key": {"t": "cell", "rc": [2, 3, 1, 1], "h": [f"key:{R.order}"]},
            "_image": {"t": "cellIm", "rc": [2, 5, 1, 1], "h": ["image"]},
            "parent": {"t": "cell", "rc": [3, 3, 1, 1], "h": [f"parent:{R.order}"]},
            "customer": {"t": "cell", "rc": [4, 3, 1, 1], "h": ["customer:activeCustomer"]},
            "brand": {"t": "cell", "rc": [5, 3, 1, 1], "h": ["brand:activeBrand"]},
            "endUser": {"t": "cell", "rc": [6, 3, 1, 1], "h": ["endUser:activeEndUser"]},
            "kind": {"t": "cell", "rc": [7, 3, 1, 1], "h": ["kind:itemKind"]},
            "name": {"t": "cell", "rc": [8, 3, 1, 1], "h": ["name"]},
            "collection": {"t": "cell", "rc": [9, 3, 1, 1], "h": ["collection:"]},
            "quantity": {"t": "cell", "rc": [10, 3, 1, 1], "h": [f"quantity:{R.qnty}"]},
            "comment": {"t": "cell", "rc": [11, 3, 1, 1], "h": ["comment"]},
            "payCond": {"t": "cell", "rc": [13, 3, 1, 1], "h": ["payCond:"]},
            "urgency": {"t": "cell", "rc": [14, 3, 1, 1], "h": ["urgency:"]},
            "targetDate": {"t": "cell", "rc": [15, 3, 1, 1], "h": ["targetDate:date:Dt.dateCell"]},
            "targetPlace": {"t": "cell", "rc": [16, 3, 1, 1], "h": ["targetPlace:"]},
            "shipTerm": {"t": "cell", "rc": [17, 3, 1, 1], "h": ["shipTerm:"]},
            "orderDate": {"t": "cell", "rc": [18, 3, 1, 1], "h": ["orderDate:date:Dt.dateCell"]},
            "finishDate": {"t": "cell", "rc": [19, 3, 1, 1], "h": ["finishDate:date:Dt.dateCell"]}
        }
    },
    {
        "_metaType": "docFrame", "_sko": "person", "_name": "ui", "_lastVersion": True, "_version": 1, "_type": "sheetFolder",
        "_drive": F.ANT, "_folder": F.Persons, "_template": F.personTemplate,
        "person": {
            "_key": {"t": "cell", "rc": [2, 3, 1, 1], "h": [f"key:{R.person}"]},
            "_image": {"t": "cellIm", "rc": [2, 5, 1, 1], "h": ["image"]},
            "idOld": {"t": "cell", "rc": [3, 3, 1, 1], "h": ["idOld"]},
            "prefix": {"t": "cell", "rc": [4, 3, 1, 1], "h": ["prefix:namePrefix"]},
            "fname": {"t": "cell", "rc": [5, 3, 1, 1], "h": ["fname"]},
            "sname": {"t": "cell", "rc": [6, 3, 1, 1], "h": ["sname"]},
            "nameth": {"t": "cell", "rc": [8, 3, 1, 1], "h": ["nameth"]},
            "position": {"t": "cell", "rc": [9, 3, 1, 1], "h": ["position:"]},
            "type": {"t": "cell", "rc": [10, 3, 1, 1], "h": ["type:positionType"]},
            "department": {"t": "cell", "rc": [11, 3, 1, 1], "h": ["department"]},
            "status": {"t": "cell", "rc": [12, 3, 1, 1], "h": ["status"]},
            "sdate": {"t": "cell", "rc": [13, 3, 1, 1], "h": ["sdate:date:Dt.dateCell"]},
            "email": {"t": "cell", "rc": [15, 3, 1, 1], "h": ["email:email"]},
            "doer": {"t": "cell", "rc": [16, 3, 1, 1], "h": ["doer:"]},
            "email2": {"t": "cell", "rc": [17, 3, 1, 1], "h": ["email2:email"]},
            "manager": {"t": "cell", "rc": [18, 3, 1, 1], "h": ["manager"]},
            "idCard": {"t": "cell", "rc": [19, 3, 1, 1], "h": ["idCard"]},
            "hPhone": {"t": "cell", "rc": [20, 3, 1, 1], "h": ["hPhone"]},
            "mPhone": {"t": "cell", "rc": [21, 3, 1, 1], "h": ["mPhone"]},
            "wPhone": {"t": "cell", "rc": [22, 3, 1, 1], "h": ["wPhone"]},
            "nick": {"t": "cell", "rc": [23, 3, 1, 1], "h": ["nick"]},
            "fdate": {"t": "cell", "rc": [24, 3, 1, 1], "h": ["fdate:date:Dt.dateCell"]}
        }
    }
]


