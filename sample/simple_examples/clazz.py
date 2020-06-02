
class Counter(dict):
    def __init__(self):
        super().__init__()

    def add(self):
        self.update({'counter': self.get('counter', 0) + 1})

    def get_count(self):
        self.get('counter', 0)

    def clear(self):
        self.update({'counter': 0})
