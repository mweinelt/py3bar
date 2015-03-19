#!/usr/bin/env python3
from py3status import Bar
from py3status.plugins import clock

bar = Bar.Bar(lc_all='de_DE.UTF-8')

# Initizalize BarItems
dt = clock.DateTime()

# Add them to your Bar
bar.register(dt)

# Run!
bar.loop()
