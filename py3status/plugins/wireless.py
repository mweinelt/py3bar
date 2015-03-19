import basiciw
import netifaces
from py3status.BarItem import UpdateType, BarItem


class Wireless(BarItem):
    def __init__(self, interface=None):
        super().__init__('Wireless')
        self.set('color', '#AAAAAA')

        # Interface auto-detection
        if interface is None:
            ethernet_interfaces = netifaces.interfaces()
            # see predictable network interface device names
            # http://cgit.freedesktop.org/systemd/systemd/tree/src/udev/udev-builtin-net_id.c#n20
            wireless_interfaces = [interface
                                   for interface
                                   in ethernet_interfaces
                                   if interface.startswith('wl')]

            # assert we have at least one wlan interface and take it
            assert wireless_interfaces
            self.interface = wireless_interfaces.pop(0)

        else:
            self.interface = interface

        self.update(trigger=UpdateType.initial)

    def update(self, trigger=UpdateType.interval):
        if trigger in [UpdateType.interval]:
            try:
                iw = basiciw.iwinfo(self.interface)
            except RuntimeError:
                self.set('color', '#AAAAAA')
                self.set('full_text', 'disabled')
                return

            essid = iw['essid']
            if essid:
                self.set('color', '#FFFFFF')
                self.set('full_text', essid)
            else:
                self.set('color', '#AAAAAA')
                self.set('full_text', 'disconnected')
