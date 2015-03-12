import json
import sys
import traceback


class ClickHandler(object):
    def __init__(self):
        """
        initialize click handler registry
        """
        self.storage = {}

    def register(self, module):
        """
        registers a plugins click handlers
        """
        self.log.write("Registering %s\n" % module.name)
        self.log.flush()

        # create module
        self.storage.update({module.name: {}})

        # add events
        self.storage[module.name][1] = module.left_click
        self.storage[module.name][2] = module.middle_click
        self.storage[module.name][3] = module.right_click

    def trigger(self, buffer):
        """
        try to parse data received from sys.stdin as json objects
        if successful, parse for module name and button id to
        trigger the modules registered click method
        :param buffer: continous json list received from stdin
        """
        if buffer == '[':
            return

        try:
            if buffer.startswith(','):
                buffer = buffer[1:]
            event = json.loads(buffer)
        except ValueError:
            return

        module = event['name']
        button = event['button']

        if module not in self.storage:
            return
        if button not in self.storage[module]:
            return

        """
        As we are unable to guess what exceptions plugins might
        throw, we have to widely catch and log all exceptions
        """
        try:
            self.storage[module][button]()
        except Exception:
            print("Exception in '%s' (button %d) caught:\n%s\n" %
                  (module, button, traceback.format_exc()),
                  file=sys.stderr)
