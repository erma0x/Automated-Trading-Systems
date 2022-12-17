import backtrader as bt
import datetime 
import os


cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)

class VIXStrategy(bt.Strategy):

    def __init__(self):
        self.vix = self.datas[0].vixclose
        self.spyopen = self.datas[0].open
        self.spyclose = self.datas[0].close

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def next(self):
        if self.vix[0] > 35:
            self.log('Previous VIX, %.2f' % self.vix[0])
            self.log('SPY Open, %.2f' % self.spyopen[0])

            if not self.position or self.broker.getcash() > 5000:
                size = int(self.broker.getcash() / self.spyopen[0])
                print("Buying {} SPY at {}".format(size, self.spyopen[0]))
                self.buy(size=size)
            
        if len(self.spyopen) % 20 == 0:
           self.log("Adding 5000 in cash, never selling. I now have {} in cash on the sidelines".format(self.broker.getcash()))
           self.broker.add_cash(5000)
        #if self.vix[0] < 10 and self.position:
        #    self.close()
        
class SPYVIXData(bt.feeds.GenericCSVData):
    lines = ('vixopen', 'vixhigh', 'vixlow', 'vixclose',)

    params = (
        ('dtformat', '%Y-%m-%d'),
        ('date', 0),
        ('spyopen', 1),
        ('spyhigh', 2),
        ('spylow', 3),
        ('spyclose', 4),
        ('spyadjclose', 5),
        ('spyvolume', 6),
        ('vixopen', 7),
        ('vixhigh', 8),
        ('vixlow', 9),
        ('vixclose', 10)
    )

class VIXData(bt.feeds.GenericCSVData):
        params = (
        ('dtformat', '%m/%d/%Y'),
        ('date', 0),
        ('vixopen', 1),
        ('vixhigh', 2),
        ('vixlow', 3),
        ('vixclose', 4),
        ('volume', -1),
        ('openinterest', -1)
    )

csv_file = os.path.dirname(os.path.realpath(__file__)) + "/spy_vix.csv"
vix_csv_file = os.path.dirname(os.path.realpath(__file__)) + "/vix.csv"

spyVixDataFeed = SPYVIXData(dataname=csv_file)
vixDataFeed = VIXData(dataname=vix_csv_file)
cerebro.adddata(spyVixDataFeed)
cerebro.adddata(vixDataFeed)

cerebro.addstrategy(VIXStrategy)

cerebro.run()
cerebro.plot(volume=False)
