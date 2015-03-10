#!/usr/bin/env python3
from Bar import Bar
from plugins import clock

bar = Bar()

# Initizalize BarItems
dt = clock.DateTime()

# Add them to your Bar
bar.register(dt)

# Run!
bar.loop()
