class K:
    KEYS = ["DL1", "D3", "D4", "L3", "L4", "Ll3", "Ll4", "L2D2", "L1D3", "DL1D3"]

    MAX = {
        "DL1": 36 - 1,          # 35
        "D3": 10*10*10 - 1,     # 999
        "D4": 10*10*10*10 - 1,  # 9999
        "L3": 26*26*26 - 1,     # 17'575
        "L4": 26*26*26*26 - 1,  # 456'975
        "Ll3": 52*52*52 - 1,    # 140'607
        "Ll4": 52*52*52*52 - 1, # 7'311'615
        "L2D2": 26*26*10*10 - 1, # 67'599
        "L1D3": 26*10*10*10 - 1, # 25'999
        "DL1D3": 36*10*10*10 - 1 # 35'999
    }

    SYNTAX = {
        "DL1": r'[0-9A-Z]',
        "D3": r'\d{3}',
        "D4": r'\d{4}',
        "L3": r'[A-Z]{3}',
        "L4": r'[A-Z]{4}',
        "Ll3": r'[A-Za-z]{3}',
        "Ll4": r'[A-Za-z]{4}',
        "L2D2": r'[A-Z]{2}\d{2}',
        "L1D3": r'[A-Z]\d{3}',
        "DL1D3": r'[0-9A-Z]\d{3}'
    }

class Key:
    
    @staticmethod
    def encode(_sn, _sko):
        from base import Meta
        key = Meta.key(_sko)
        # key: { prefix, suffix, type, syntax, snMin, snMax }
        AZ = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        AZaz = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
        DAZ = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

        en = {
            "D3":   lambda: str((_sn // 10 // 10) % 10) + str((_sn // 10) % 10) + str(_sn % 10),
            "D4":   lambda: str((_sn // 10 // 10 // 10) % 10) + str((_sn // 10 // 10) % 10) + str((_sn // 10) % 10) + str(_sn % 10),
            "L3":   lambda: AZ[(_sn // 26 // 26) % 26] + AZ[(_sn // 26) % 26] + AZ[_sn % 26],
            "Ll3":  lambda: AZaz[(_sn // 52 // 52) % 52] + AZaz[(_sn // 52) % 52] + AZaz[_sn % 52],
            "L4":   lambda: AZ[(_sn // 26 // 26 // 26) % 26] + AZ[(_sn // 26 // 26) % 26] + AZ[(_sn // 26) % 26] + AZ[_sn % 26],
            "Ll4":  lambda: AZaz[(_sn // 52 // 52 // 52) % 52] + AZaz[(_sn // 52 // 52) % 52] + AZaz[(_sn // 52) % 52] + AZaz[_sn % 52],
            "L2D2": lambda: AZ[(_sn // 10 // 10 // 26) % 26] + AZ[(_sn // 10 // 10) % 26] + str((_sn // 10) % 10) + str(_sn % 10),
            "L1D3": lambda: AZ[(_sn // 10 // 10 // 10) % 26] + str((_sn // 10 // 10) % 10) + str((_sn // 10) % 10) + str(_sn % 10),
            "DL1D3":lambda: DAZ[(_sn // 10 // 10 // 10) % 36] + str((_sn // 10 // 10) % 10) + str((_sn // 10) % 10) + str(_sn % 10)
        }

        if not (key['type'] in K.KEYS and 0 <= _sn <= Key.max(key['type'])): return None
        return key['prefix'] + en[key['type']]() + key['suffix']

    @staticmethod
    def decode(_key, key):
        import re
        AZN = {chr(i): i - 65 for i in range(65, 91)}
        AZazN = {chr(i): i - 65 for i in range(65, 91)}
        AZazN.update({chr(i): i - 71 for i in range(97, 123)})
        DAZN = {str(i): i for i in range(10)}
        DAZN.update({chr(i): i - 55 for i in range(65, 91)})

        de = {
            "D3":    lambda s: int(s[0]) * 100 + int(s[1]) * 10 + int(s[2]),
            "D4":    lambda s: int(s[0]) * 1000 + int(s[1]) * 100 + int(s[2]) * 10 + int(s[3]),
            "L3":    lambda s: AZN[s[0]] * 26 * 26 + AZN[s[1]] * 26 + AZN[s[2]],
            "Ll3":   lambda s: AZazN[s[0]] * 52 * 52 + AZazN[s[1]] * 52 + AZazN[s[2]],
            "L4":    lambda s: AZN[s[0]] * 26 * 26 * 26 + AZN[s[1]] * 26 * 26 + AZN[s[2]] * 26 + AZN[s[3]],
            "Ll4":   lambda s: AZazN[s[0]] * 52 * 52 * 52 + AZazN[s[1]] * 52 * 52 + AZazN[s[2]] * 52 + AZazN[s[3]],
            "L2D2":  lambda s: AZN[s[0]] * 26 * 100 + AZN[s[1]] * 100 + int(s[2]) * 10 + int(s[3]),
            "L1D3":  lambda s: AZN[s[0]] * 1000 + int(s[1]) * 100 + int(s[2]) * 10 + int(s[3]),
            "DL1D3": lambda s: DAZN[s[0]] * 1000 + int(s[1]) * 100 + int(s[2]) * 10 + int(s[3])
        }

        if key['type'] not in K.KEYS:
            return None
        if not re.match(key['syntax'], _key):
            raise ValueError(f"Key.decode: Wrong _key ({_key}) syntax")
        return de[key['type']](_key)

    @staticmethod
    def max(key_type):
        if key_type in K.KEYS: return K.MAX[key_type]