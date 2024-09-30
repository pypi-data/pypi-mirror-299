import backtrader as bt

__ALL__ = ['MyDrawDown']

class MyDrawDown(bt.observers.DrawDown):
    params = (
        ('msg_queue', None),
    )

    def __init__(self):
        super(MyDrawDown, self).__init__()
        self.msg_queue = self.p.msg_queue