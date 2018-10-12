




'CombOffsetFlag': '0',
'OrderRef': '1',
'InvestorID': '070150',
'UserID': '070150',
'BrokerID': '9999'
'CombHedgeFlag': '1'
'ContingentCondition': '1'
'ForceCloseReason': '0'
'IsAutoSuspend': 0
'TimeCondition': '3'
'VolumeCondition': '1'
'MinVolume': 1

BrokerID=self.broker,
InvestorID=self.investor,                                   'InstrumentID': 'ag1812',
InstrumentID=f.getInstrumentID(),
OrderRef='{0:>12}'.format(self.req),
UserID=self.investor,
OrderPriceType=ctp.OrderPriceTypeType.LimitPrice,           'OrderPriceType': '2',
Direction=ctp.DirectionType.Buy,                            'Direction': '1',
CombOffsetFlag=ctp.OffsetFlagType.Open.__char__(),
CombHedgeFlag=ctp.HedgeFlagType.Speculation.__char__(),
LimitPrice=f.getLastPrice() - 50,                           'LimitPrice': 3539.0,
VolumeTotalOriginal=1,                                      'VolumeTotalOriginal': 2,
TimeCondition=ctp.TimeConditionType.GFD,
# GTDDate=''
VolumeCondition=ctp.VolumeConditionType.AV,
MinVolume=1,
ContingentCondition=ctp.ContingentConditionType.Immediately,
StopPrice=0,
ForceCloseReason=ctp.ForceCloseReasonType.NotForceClose,
IsAutoSuspend=0,
IsSwapOrder=0,
UserForceClose=0