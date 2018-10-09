#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ctypes import *

from ctp_enum import *

class CThostFtdcDisseminationField(Structure):
    """信息分发"""
    _fields_ = [
        # 序列系列号
        ("SequenceSeries", c_int32),
        # 序列号
        ("SequenceNo", c_int32),
        ]

    def getSequenceSeries(self):
        return self.SequenceSeries
    def getSequenceNo(self):
        return self.SequenceNo

    def __str__(self):
        return 'SequenceSeries = {0}, SequenceNo = {1}'.format(self.SequenceSeries, self.SequenceNo)

    @property
    def __dict__(self):
        return {'SequenceSeries': self.SequenceSeries,'SequenceNo': self.SequenceNo}

    def clone(self):
        obj=CThostFtdcDisseminationField()
        obj.SequenceSeries=self.SequenceSeries
        obj.SequenceNo=self.SequenceNo
        return obj

AA = CThostFtdcDisseminationField()
print(AA. _fields_)
print(type([1,1]))