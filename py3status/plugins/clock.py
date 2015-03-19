import time

from py3status.BarItem import UpdateType
from py3status import BarItem


class DateTime(BarItem):
    def __init__(self, dt_format='%H:%M:%S'):
        super().__init__('DateTime')
        self.set('color', '#AAAAAA')
        self.format = dt_format
        self.update(trigger=UpdateType.initial)

    def update(self, trigger=UpdateType.interval):
        self.set('full_text', time.strftime(self.format))
