class CtpMdApi:
    """CTP行情API实现"""

    # ----------------------------------------------------------------------
    def __init__(self, gateway):

        self.Session = ''
        dllpath = os.path.join(os.path.split(os.path.realpath(__file__))[0], '..', 'dll')
        self.MDAPI = Quote(os.path.join(dllpath, 'ctp_quote.' + ('dll' if 'Windows' in platform.system() else 'so')))

        self.gateway = gateway  # gateway对象
        self.gatewayName = gateway.gatewayName  # gateway对象名称

        self.reqID = EMPTY_INT  # 操作请求编号

        self.connectionStatus = False  # 连接状态
        self.loginStatus = False  # 登录状态

        self.subscribedSymbols = set()  # 已订阅合约代码

        self.userID = EMPTY_STRING  # 账号
        self.password = EMPTY_STRING  # 密码
        self.brokerID = EMPTY_STRING  # 经纪商代码
        self.address = EMPTY_STRING  # 服务器地址

    # ----------------------------------------------------------------------
    def onFrontConnected(self):
        """服务器连接"""
        self.connectionStatus = True

        self.writeLog(text.DATA_SERVER_CONNECTED)

        self.login()

    # ----------------------------------------------------------------------
    def onFrontDisconnected(self, n):
        """服务器断开"""
        self.connectionStatus = False
        self.loginStatus = False
        self.gateway.mdConnected = False

        self.writeLog(text.DATA_SERVER_DISCONNECTED)

    # ----------------------------------------------------------------------
    def onHeartBeatWarning(self, n):
        """心跳报警"""
        # 因为API的心跳报警比较常被触发，且与API工作关系不大，因此选择忽略
        pass

    # ----------------------------------------------------------------------
    def onRspError(self, error, n, last):
        """错误回报"""
        err = VtErrorData()
        err.gatewayName = self.gatewayName
        err.errorID = error['ErrorID']
        err.errorMsg = error['ErrorMsg'].decode('gbk')
        self.gateway.onError(err)

    # ----------------------------------------------------------------------
    def onRspUserLogin(self, data, error, n, last):
        """登陆回报"""
        # 如果登录成功，推送日志信息
        if error['ErrorID'] == 0:
            self.loginStatus = True
            self.gateway.mdConnected = True

            self.writeLog(text.DATA_SERVER_LOGIN)

            # 重新订阅之前订阅的合约
            for subscribeReq in self.subscribedSymbols:
                self.subscribe(subscribeReq)

        # 否则，推送错误信息
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)

    # ----------------------------------------------------------------------
    def onRspUserLogout(self, data, error, n, last):
        """登出回报"""
        # 如果登出成功，推送日志信息
        if error['ErrorID'] == 0:
            self.loginStatus = False
            self.gateway.mdConnected = False

            self.writeLog(text.DATA_SERVER_LOGOUT)

        # 否则，推送错误信息
        else:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)

    # ----------------------------------------------------------------------
    def onRspSubMarketData(self, data, error, n, last):
        """订阅合约回报"""
        if 'ErrorID' in error and error['ErrorID']:
            err = VtErrorData()
            err.gatewayName = self.gatewayName
            err.errorID = error['ErrorID']
            err.errorMsg = error['ErrorMsg'].decode('gbk')
            self.gateway.onError(err)

    # ----------------------------------------------------------------------
    def onRspUnSubMarketData(self, data, error, n, last):
        """退订合约回报"""
        # 同上
        pass

        # ----------------------------------------------------------------------

    def onRtnDepthMarketData(self, data):
        """行情推送"""
        # 过滤尚未获取合约交易所时的行情推送
        symbol = data['InstrumentID']
        if symbol not in symbolExchangeDict:
            return

        # 创建对象
        tick = VtTickData()
        tick.gatewayName = self.gatewayName

        tick.symbol = symbol
        tick.exchange = symbolExchangeDict[tick.symbol]
        tick.vtSymbol = tick.symbol  # '.'.join([tick.symbol, tick.exchange])

        tick.lastPrice = data['LastPrice']
        tick.volume = data['Volume']
        tick.openInterest = data['OpenInterest']
        tick.time = '.'.join([data['UpdateTime'], str(data['UpdateMillisec'] / 100)])

        # 上期所和郑商所可以直接使用，大商所需要转换
        tick.date = data['ActionDay']

        tick.openPrice = data['OpenPrice']
        tick.highPrice = data['HighestPrice']
        tick.lowPrice = data['LowestPrice']
        tick.preClosePrice = data['PreClosePrice']

        tick.upperLimit = data['UpperLimitPrice']
        tick.lowerLimit = data['LowerLimitPrice']

        # CTP只有一档行情
        tick.bidPrice1 = data['BidPrice1']
        tick.bidVolume1 = data['BidVolume1']
        tick.askPrice1 = data['AskPrice1']
        tick.askVolume1 = data['AskVolume1']

        # 大商所日期转换
        if tick.exchange is EXCHANGE_DCE:
            tick.date = datetime.now().strftime('%Y%m%d')

        self.gateway.onTick(tick)

    # ----------------------------------------------------------------------
    def onRspSubForQuoteRsp(self, data, error, n, last):
        """订阅期权询价"""
        pass

    # ----------------------------------------------------------------------
    def onRspUnSubForQuoteRsp(self, data, error, n, last):
        """退订期权询价"""
        pass

        # ----------------------------------------------------------------------

    def onRtnForQuoteRsp(self, data):
        """期权询价推送"""
        pass

        # ----------------------------------------------------------------------

    def connect(self, userID, password, brokerID, address):
        """初始化连接"""
        self.userID = userID  # 账号
        self.password = password  # 密码
        self.brokerID = brokerID  # 经纪商代码
        self.address = address  # 服务器地址

        # 如果尚未建立服务器连接，则进行连接
        if not self.connectionStatus:
            # 创建C++环境中的API对象，这里传入的参数是需要用来保存.con文件的文件夹路径
            path = getTempPath(self.gatewayName + '_')
            self.createFtdcMdApi(path)
            self.MDAPI.RegisterFront()
            # 注册服务器地址
            self.registerFront(self.address)

            # 初始化连接，成功会调用onFrontConnected
            self.init()

        # 若已经连接但尚未登录，则进行登录
        else:
            if not self.loginStatus:
                self.login()

    # ----------------------------------------------------------------------
    def subscribe(self, subscribeReq):
        """订阅合约"""
        # 这里的设计是，如果尚未登录就调用了订阅方法
        # 则先保存订阅请求，登录完成后会自动订阅
        if self.loginStatus:
            self.subscribeMarketData(str(subscribeReq.symbol))
        self.subscribedSymbols.add(subscribeReq)

        # ----------------------------------------------------------------------

    def login(self):
        """登录"""
        # 如果填入了用户名密码等，则登录
        if self.userID and self.password and self.brokerID:
            req = {}
            req['UserID'] = self.userID
            req['Password'] = self.password
            req['BrokerID'] = self.brokerID
            self.reqID += 1
            self.reqUserLogin(req, self.reqID)

            # ----------------------------------------------------------------------

    def close(self):
        """关闭"""
        self.exit()

    # ----------------------------------------------------------------------
    def writeLog(self, content):
        """发出日志"""
        log = VtLogData()
        log.gatewayName = self.gatewayName
        log.logContent = content
        self.gateway.onLog(log)        
