import threading, time


class Delay(threading.Thread):

    def __init__(self, args=()):
        super().__init__()

        self.cola = args[0]

    def run(self):
        time.sleep(5)
        self.cola.put("c")