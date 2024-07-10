import backtrader as bt

class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'{dt.isoformat()}, {txt}')
    
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.order = None
    
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED {order.executed.price}')
            elif order.issell():
                self.log(f'SELL EXECUTED {order.executed.price}')
            self.bar_executed = len(self)
        self.order = None

    def next(self):
        self.log(f'Close {self.dataclose[0]}')

        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                # current close less than previous cycle
                if self.dataclose[-1] < self.dataclose[-2]:
                    # previous close less than the previous close
                    self.log(f'BUY CREATE {self.dataclose[0]}')
                    self.order = self.order_target_percent(target=0.1)
        else:
            if len(self) >= self.bar_executed + 20:
                self.log(f'SELL CREATED {self.dataclose[0]}')
                self.order = self.sell(size=self.position.size)