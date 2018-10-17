import shelve
f = shelve.open('123.txt')
f['hao'] = [1,2,3,54]
f.close()

f = shelve.open('123')
a = f.get('hao')
print(a)