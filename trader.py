import backtrader as bt
import datetime
from test_strategy import TestStrategy
from indicator_avg_strategy import AvgStrategy
from commission_info_fractional import CommInfoFractional

starting_cash = 12284
start_date = datetime.datetime(2019, 7, 9)
end_date = datetime.datetime(2024, 7, 9)
num_days = (end_date - start_date).days - 1
cerebro = bt.Cerebro()
cerebro.broker.set_cash(starting_cash)
cerebro.broker.addcommissioninfo(CommInfoFractional())
data = bt.feeds.YahooFinanceCSVData(
    dataname='BTC-USD.csv', fromdate=start_date,
    todate=end_date)
cerebro.adddata(data)
cerebro.addstrategy(AvgStrategy)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
buy_and_hold_value = (1 + (1.0 * (data[0] - data[-num_days]) / data[-num_days])) * starting_cash
print('Buy/Hold Value: %.2f' % buy_and_hold_value)
cerebro.plot()
