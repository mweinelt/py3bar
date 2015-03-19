import subprocess
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
            assert len(wireless_interfaces)
            interface = wireless_interfaces.pop(0)

        self.interface = interface
        self.update()

    def update(self, trigger=UpdateType.interval):
        if trigger in [UpdateType.interval]:
            iw = basiciw.iwinfo(self.interface)
            self.set('color', '#ffffff')
            essid = iw['essid']
            if len(essid) > 0:
                self.set('full_text', essid)
            else:
                self.set('full_text', 'off')

    def left_click(self):
        self.set('color', '#ff0000')
        try:
            subprocess.Popen(['/usr/bin/nm-connection-editor'])
        except OSError as e:
            foo = open('/tmp/test', 'w')
            foo.write(e)
            foo.close()
