import threading, time

import airsim


class Input(threading.Thread):

    def __init__(self, args=()):
        super().__init__()

        self.client = args[0]
        self.action = args[1]

    def run(self):

        while True:

            input = airsim.wait_key('Press any key to take images')

            self.action.put(input)

