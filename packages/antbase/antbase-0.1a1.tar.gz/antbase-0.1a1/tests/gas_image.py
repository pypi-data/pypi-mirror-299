
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from antbase.base.gas import Gas

function = "insertCellImage"
ssId     = "1kHjoFh3xfLoit6UVksqn_xnKjkBSGettUB4Qt5vWrRY"
shName   = "TestSheet"
fileName = "p6638ph"
r        = 12
c        = 5

result = Gas.run(function, ssId, shName, fileName, r, c)

print(result)