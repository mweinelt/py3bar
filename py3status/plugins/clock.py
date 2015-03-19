import time
from py3status.BarItem import UpdateType, BarItem


class DateTime(BarItem):
    def __init__(self, format=None):
        super().__init__('DateTime')
        self.set('color', '#AAAAAA')

        self.format_index = 0
        if isinstance(format, str):
            self.formats = list(format)
        elif isinstance(format, list):
            self.formats = format
        else:
            self.formats = ['%X', '%x']

        self.update(trigger=UpdateType.initial)

    def update(self, trigger=UpdateType.interval):
        self.set('full_text', time.strftime(self.formats[self.format_index]))

    def left_click(self):
        if self.format_index < len(self.formats) - 1:
            self.format_index += 1
        else:
            self.format_index = 0
        self.update(trigger=UpdateType.click)