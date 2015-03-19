from py3status.BarItem import UpdateType, BarItem


class ThinkpadBattery(BarItem):
    def __init__(self, path='/sys/devices/platform/smapi/BAT0/'):
        super().__init__('Battery')
        self.base_path = path
        self.update()

    def get_data(self, node):
        with open("%s%s" % (self.base_path, node), 'r') as file:
            return file.read().strip()

    def update(self, trigger=UpdateType.interval):
        self.set('full_text', '{remainder}%'.format(
            remainder=self.get_data('remaining_percent')))
