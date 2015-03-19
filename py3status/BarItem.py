from enum import Enum
from collections import OrderedDict


class UpdateType(Enum):
    initial = 1
    interval = 2
    inotify = 3
    click = 4


class BarItem(object):
    # define valid options for i3bar according to
    # http://i3wm.org/docs/i3bar-protocol.html
    options = ['full_text', 'short_text', 'color', 'min_width',
               'align', 'name', 'instance', 'urgent', 'separator',
               'separator_block_width']

    def __init__(self, name):
        self.blocks = OrderedDict()
        self.name = name.lower()

    def get(self):
        return self.blocks

    def get_block_key(self, block):
        return '{prefix}_{suffix}'.format(prefix=self.name, suffix=block)

    def set(self, option, value, block='default'):
        assert option in self.options
        # prefix the module id for collision resistance
        block_key = self.get_block_key(block)
        if block_key not in self.blocks:
            self.blocks[block_key] = {'name': block_key}
        self.blocks[block_key][option] = value

    def update(self, trigger=UpdateType.interval):
        """
        :param trigger: enum UpdateType, what triggered the update?
        """
        pass

    def left_click(self):
        pass

    def right_click(self):
        pass

    def middle_click(self):
        pass
