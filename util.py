import threading

class AtomicBool:
    _value = True

    def __init__(self, initial_value: bool):
        self.lock = threading.Lock()
        self.set(initial_value)

    def set(self, new_value: bool):
        with self.lock:
            self._value = new_value

    def get(self):
        with self.lock:
            return self._value