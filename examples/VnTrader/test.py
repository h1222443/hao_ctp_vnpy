import shelve
from vnpy.trader.vtFunction import *


contractDict = {}
contractFileName = 'safa.txt'
contractFilePath = getTempPath(contractFileName)
print(contractFilePath)

f = shelve.open(contractFilePath)
if 'data' in f:

    d = f['data']
    for key, value in d.items():
        contractDict[key] = value

print(contractDict)