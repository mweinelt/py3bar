#!/usr/bin/python3
from Bar import Bar
from plugins import datetime, thinkpad_battery, wireless, ingress_portal

bar = Bar()

# Initizalize BarItems
dt = datetime.DateTime()
battery = thinkpad_battery.ThinkpadBattery()
wireless_wlp2s0 = wireless.Wireless()

# Add them to your Bar
bar.register(wireless_wlp2s0)
bar.register(battery)
bar.register(dt)

# Run!
bar.loop()
