import os
currentFolder = os.getcwd()
filePath = os.path.join(currentFolder, 'VT_setting.json')
print(filePath)
print(os.path.exists(filePath))

f = open(filePath,encoding='utf8')
print(f.read())
