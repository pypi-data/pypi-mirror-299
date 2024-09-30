import backtrader as bt
import pytz
from ffquant.utils.observer_queue import treturn_queue

__ALL__ = ['MyTimeReturn']

class MyTimeReturn(bt.observers.TimeReturn):
    def __init__(self):
        super(MyTimeReturn, self).__init__()
        self.msg_queue = treturn_queue

    def next(self):
        super(MyTimeReturn, self).next()
        msg = {
            "datetime": self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "timereturn": self.lines.timereturn[0]
        }
        print(f"MyTimeReturn, next, msg_queue: {self.msg_queue}, msg: {msg}")
        self.msg_queue.put(msg)

        
