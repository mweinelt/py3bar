import json
import time
import sys
import signal
from select import select
from BarItem import BarItem
from core.ClickHandler import ClickHandler


class Bar(object):
    def __init__(self, interval=0.5):
        self.items = []
        self.interval = interval
        self.pause = False

        # signals
        self.signal_pause = signal.SIGSTOP
        self.signal_resume = signal.SIGCONT

        signal.signal(self.signal_pause, self.pause)
        signal.signal(self.signal_resume, self.resume)

        # click events
        self.clickHandler = ClickHandler()

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

    def pause(self):
        """
        Signalhandler for the i3bar stop signal, preventing output
        and calls to BarItem.update() when triggered
        """
        self.pause = True

    def resume(self):
        """
        Signalhandler for the i3bar continue signal, reallowing output
        and calls to BarItem.update() when triggered
        """
        self.pause = False

    def loop(self):
        log = open('/tmp/py3bar.log', 'w')

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
            if not self.pause:
                print("%s," % self.query())
                sys.stdout.flush()

            # in
            while sys.stdin in select([sys.stdin], [], [], 0)[0]:
                event = sys.stdin.readline()[:-1]
                self.clickHandler.trigger(event)
                log.write('<- %s' % event)
                log.flush()

            time.sleep(self.interval)
