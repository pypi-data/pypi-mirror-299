from antbase.server_base.r import R


def test_regex(pattern, test_strings):
    for test_string in test_strings:
        match = pattern.match(test_string)
        print(f"Testing '{test_string}' against pattern '{pattern.pattern}': {'Match' if match else 'No match'}")

# Примеры тестов для каждого регулярного выражения
test_regex(R.stage, ["presale", "purchase", "invalid"])
test_regex(R.work, ["#print", "#cast", "#invalid"])
test_regex(R.design, ["@sketch", "@cad", "@invalid"])
test_regex(R.wdesign, ["@modeling", "@silicon", "@invalid"])
test_regex(R.production, ["@sort", "@filing", "@invalid"])
test_regex(R.status, ["?active", "?inactive", "?Invalid"])
test_regex(R.terminate, ["end", "cancel", "invalid"])

test_regex(R.jjob, ["jAB12", "jXY34", "invalid"])
test_regex(R.pjob, ["pA123", "pZ456", "invalid"])
test_regex(R.cjob, ["cA123", "cZ456", "invalid"])
test_regex(R.sjob, ["sA123", "sZ456", "invalid"])
test_regex(R.djob, ["dA123", "dZ456", "invalid"])
test_regex(R.order, ["oA123", "oZ456", "invalid"])
test_regex(R.trigger, ["TABCD", "TXYZA", "invalid"])

test_regex(R.qnty, ["10", "25", "invalid"])
test_regex(R.model, ["mAB12", "mXY34", "invalid"])
test_regex(R.item, ["xAB12", "xXY34", "invalid"])
test_regex(R.address, ["aAB12", "aXY34", "invalid"])

test_regex(R.modelOld, ["m1234", "m5678", "invalid"])
test_regex(R.orderOld, ["o1234", "o5678", "invalid"])
test_regex(R.itemOld, ["ABC", "XYZ", "invalid"])

test_regex(R.ringSize, ["ru20.50", "eu50", "invalid"])
test_regex(R.productQnt, ["10", "99", "invalid"])

test_regex(R.Number, ["NaN", "123.45", "-123.45E+6", "invalid"])
test_regex(R.Boolean, ["true", "FALSE", "invalid"])
test_regex(R.IsoDate, ["2023-10-01T12:34:56.789Z", "2023-10-01T12:34:56Z", "invalid"])