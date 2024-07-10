import backtrader as bt
import datetime
from test_strategy import TestStrategy
from commission_info_fractional import CommInfoFractional

cerebro = bt.Cerebro()

cerebro.broker.set_cash(10000)
cerebro.broker.addcommissioninfo(CommInfoFractional())
data = bt.feeds.YahooFinanceCSVData(
    dataname='BTC-USD.csv', fromdate=datetime.datetime(2023, 7, 9),
    todate=datetime.datetime(2024, 7, 9))
cerebro.adddata(data)
cerebro.addstrategy(TestStrategy)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.plot()
