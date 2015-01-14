from BarItem import BarItem, UpdateType
import time


class DateTime(BarItem):
    def __init__(self, dt_format='%H:%M:%S'):
        super().__init__('DateTime')
        self.set('color', '#AAAAAA')
        self.format = dt_format
        self.update(trigger=UpdateType.initial)

    def update(self, trigger=UpdateType.interval):
        self.set('full_text', time.strftime(self.format))