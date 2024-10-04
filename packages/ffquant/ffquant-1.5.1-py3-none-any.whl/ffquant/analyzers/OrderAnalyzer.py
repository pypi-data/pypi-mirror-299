import backtrader as bt
import pytz

__ALL__ = ['OrderAnalyzer']

class OrderAnalyzer(bt.Analyzer):
    def __init__(self):
        self.order_infos = []
    
    def notify_order(self, order):
        if order.status == order.Completed:
            dt = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
            order_info = {
                'datetime': dt,
                'data': order,
                'position_after': self.strategy.position.size
            }
            self.order_infos.append(order_info)
    
    def get_analysis(self):
        return self.order_infos