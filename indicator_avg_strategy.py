import backtrader as bt
import backtrader.indicators as btind

class AvgStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')
    
    def __init__(self):
        self.target_percent = 1.0
        self.stop_loss = .1
        self.trades = 0.0
        self.wins = 0.0
        self.dataclose = self.datas[0].close
        self.order = None
        self.stop_loss_order = None
        self.buy_price = None
        self.just_sold = False
        self.sma_5 = btind.SMA(self.data, period=5)
        self.sma_20 = btind.SMA(self.data, period=20)
        self.sma_50 = btind.SMA(self.data, period=50)
        self.sma_200 = btind.SMA(self.data, period=200)
        self.rsi_10 = btind.RSI(self.data, period=10)
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                # self.log(f'BUY EXECUTED {order.executed.price}')
                self.buy_price = order.executed.price
                stop_price = order.executed.price * (1.0 - self.stop_loss)
                self.stop_loss_order = self.sell(size=self.position.size, exectype=bt.Order.Stop, price=stop_price)
            elif order.issell():
                self.log(f'Profit {(order.executed.price - self.buy_price) / self.buy_price}')
                if order.executed.price - self.buy_price > 0:
                    self.wins += 1
                self.trades += 1
                self.stop_loss_order = None
                self.just_sold = True
        # elif order.status in [order.Canceled]:
        #     # self.log(f'CANCELED STOP LOSS ORDER')
        self.order = None

    def notify_fund(self, cash, value, fundvalue, shares):
        if self.just_sold:
            self.log(f'Current value {value}. Win %: {self.wins / self.trades}')
            self.just_sold = False

    def next(self):
        # self.log(f'Close {self.dataclose[0]}')

        if self.order:
            return
        
        avg_indicators = 0
        avg_indicators += self.cross(self.sma_5, self.sma_20)
        avg_indicators += self.cross(self.sma_20, self.sma_50)
        avg_indicators += self.cross(self.sma_50, self.sma_200)
        avg_indicators += self.rsi() * 2

        
        if self.stop_loss_order is None:
            if avg_indicators > 0:
                # self.log(f'BUY CREATE {self.dataclose[0]}')
                self.order = self.order_target_percent(target=self.target_percent)
            return
        if avg_indicators < 0:
            # self.log(f'SELL CREATED {self.dataclose[0]}')
            self.order = self.sell(size=self.position.size)
            self.cancel(self.stop_loss_order)

    
    def cross(self, small_sma, long_sma):
        if small_sma[0] > long_sma[0] and small_sma[-1] < long_sma[-1]:
            return 1
        elif small_sma[0] < long_sma[0] and small_sma[-1] > long_sma[-1]:
            return -1
        return 0
    
    def rsi(self):
        holding_asset = self.stop_loss_order is not None
        curr_rsi = self.rsi_10[0]
        # self.log(curr_rsi)
        if holding_asset:
            if curr_rsi > 70:
                return 1
            if curr_rsi <= 55:
                return -1
            return 0
        if curr_rsi < 20:
            return 1
        if curr_rsi <= 50 and curr_rsi >= 20:
            return -1
        if curr_rsi > 70:
            return 1
        return 0

        
        
