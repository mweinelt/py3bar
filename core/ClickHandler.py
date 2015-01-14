import json


class ClickHandler(object):
    def __init__(self):
        self.storage = {}
        self.log = open('/tmp/click.log', 'w')

    def register(self, module):
        self.log.write("Registering %s\n" % module.name)
        self.log.flush()

        # create module
        self.storage.update({module.name: {}})

        # add events
        self.storage[module.name][1] = module.left_click
        self.storage[module.name][2] = module.middle_click
        self.storage[module.name][3] = module.right_click

    def trigger(self, event):
        if event == '[':
            return

        try:
            self.log.write("%s\n" % event)
            event = json.loads(event)
        except (ValueError, KeyError) as e:
            # malformed json in stdin
            self.log.write('Error: %s\n' % e)
            return

        self.log.flush()

        module = event['name']
        button = event['button']

        if not module in self.storage:
            return
        if not button in self.storage[module]:
            return

        self.log.write('running\n')
        self.log.flush()
        try:
            self.storage[module][button]()
        except Exception as e:
            self.log.write(e)


