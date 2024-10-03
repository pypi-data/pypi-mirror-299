from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import platform

from .observer_queue import treturn_queue

if platform.system() != 'Windows':
    from .MqProducer import MqProducer