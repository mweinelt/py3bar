import json
import locale
import signal
import sys
import time
from select import select
from py3status.BarItem import BarItem
from py3status.ClickHandler import ClickHandler


class Bar(object):
    def __init__(self, interval=0.5, lc_all='de_DE.UTF-8'):
        self.items = []
        self.interval = interval
        self.paused = False

        # signals
        self.signal_pause = signal.SIGTSTP
        self.signal_resume = signal.SIGCONT

        signal.signal(self.signal_pause, self.pause)
        signal.signal(self.signal_resume, self.resume)

        # click events
        self.clickHandler = ClickHandler()

        # set locale for sensitive date output among other things
        locale.setlocale(locale.LC_ALL, lc_all)

    def register(self, item):
        assert isinstance(item, BarItem)
        self.clickHandler.register(item)
        self.items.append(item)

    def query(self):
        results = []
        for item in self.items:
            item.update()
            response = item.get()
            for _, block in response.items():
                results.append(block)

        return json.dumps(results)

    def pause(self, signum, frame):
        """
        Signalhandler for the i3bar stop signal, preventing output
        and calls to BarItem.update() when triggered
        """
        self.paused = True

    def resume(self, signum, frame):
        """
        Signalhandler for the i3bar continue signal, reallowing output
        and calls to BarItem.update() when triggered
        """
        self.paused = False

    def loop(self):
        ###############################################
        # http://i3wm.org/docs/i3bar-protocol.html
        ###############################################
        # i3bar header, there are more options...
        print(json.dumps({'version': 1,
                          'stop_signal': self.signal_pause,
                          'cont_signal': self.signal_resume,
                          'click_events': True}))

        # the i3bar protocol expects and endless json list
        # so open it, print an item, add a comma, and so forth.
        print('[')  # open endless list
        print("[],")  # first item is empty
        while True:
            # out
            if not self.paused:
                print("%s," % self.query())
                sys.stdout.flush()

            # in
            input_processed = False
            while sys.stdin in select([sys.stdin], [], [], 0)[0]:
                line = sys.stdin.readline()
                print(line, file=sys.stderr)
                self.clickHandler.trigger(line)
                input_processed = True

            """
            if input was processed earlier we skip the next sleep
            because a visual response might be expected
            """
            if not input_processed:
                time.sleep(self.interval)

            sys.stderr.flush()
