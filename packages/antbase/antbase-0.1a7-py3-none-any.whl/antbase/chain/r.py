import re

class R:
    stage       = re.compile(r"^(presale|purchase|design|cast|sorting|production|wdesign|postproduction)$")
    work        = re.compile(r"^\#(print|cast|cert|cut|mark|plate|set)$")
    design      = re.compile(r"^\@(sketch|cad|cam|spec|idle)$")
    wdesign     = re.compile(r"^\@(modeling|silicon|silicut|waxinject|wax|tree|cast|idle)$")
    production  = re.compile(r"^\@(sort|filing|assemble|set|engrave|polish|plate|idle)$")
    status      = re.compile(r"^\?[a-z]+$")
    terminate   = re.compile(r"^(end|cancel|suspend)$")

    jjob        = re.compile(r"^j[A-Z]{2}\d{2}$")
    pjob        = re.compile(r"^p[0-9A-Z]\d{3}$")
    cjob        = re.compile(r"^c[0-9A-Z]\d{3}$")
    sjob        = re.compile(r"^s[0-9A-Z]\d{3}$")
    djob        = re.compile(r"^d[0-9A-Z]\d{3}$")
    order       = re.compile(r"^o[0-9A-Z]\d{3}$")
    trigger     = re.compile(r"^T[A-Z]{4}$")

    person      = re.compile(r"^e\d{3}$")
    trigger     = re.compile(r"^T\d{3}$")

    qnty        = re.compile(r"^[1-3]*[0-9]+$")
    model       = re.compile(r"^m[A-Z]{2}[0-9]{2}$")
    item        = re.compile(r"^x[A-Z]{2}[0-9]{2}$")
    address     = re.compile(r"^a[A-Z]{2}[0-9]{2}$")

    modelOld    = re.compile(r"^m\d{4}$")
    orderOld    = re.compile(r"^o\d{4}$")
    itemOld     = re.compile(r"^[A-Z]{3}$")

    ringSize    = re.compile(r"^(ru[12][0-9]\.[0-9]{2})|(eu[2-7][0-9])$")
    productQnt  = re.compile(r"^([1-9][0-9]{0,1})$")

    Number      = re.compile(r"^NaN|-?((\d*\.\d+|\d+)([Ee][+-]?\d+)?|Infinity)$")
    Boolean     = re.compile(r"^(true|TRUE|false|FALSE)$")
    IsoDate     = re.compile(r"^(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d\.\d+([+-][0-2]\d:[0-5]\d|Z))|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d:[0-5]\d([+-][0-2]\d:[0-5]\d|Z))|(\d{4}-[01]\d-[0-3]\dT[0-2]\d:[0-5]\d([+-][0-2]\d:[0-5]\d|Z))$")
