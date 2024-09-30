import backtrader as bt

__ALL__ = ['MyBuySell']

class MyBuySell(bt.observers.BuySell):

    params = (
        ('msg_queue', None),
    )

    def __init__(self):
        super(MyBuySell, self).__init__()
        self.msg_queue = self.p.msg_queue