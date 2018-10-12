from datetime import datetime


a = 'haoweihua'

print(a[0:3])
tick = datetime.strptime('20150101 15:00:00.56', '%Y%m%d %H:%M:%S.%f')
cday = datetime.strptime('2015-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
print(cday)
print(tick)