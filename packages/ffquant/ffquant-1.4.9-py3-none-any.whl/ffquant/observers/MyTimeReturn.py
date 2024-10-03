import backtrader as bt
import pytz
import ffquant.utils.observer_data as observer_data

__ALL__ = ['MyTimeReturn']

class MyTimeReturn(bt.observers.TimeReturn):
    def __init__(self):
        super(MyTimeReturn, self).__init__()
        self.msg_queue = observer_data.treturn

    def next(self):
        super(MyTimeReturn, self).next()
        msg = {
            "datetime": self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "timereturn": self.lines.timereturn[0]
        }
        print(f"MyTimeReturn, next, msg: {msg}")
        self.msg_queue.append(msg)
