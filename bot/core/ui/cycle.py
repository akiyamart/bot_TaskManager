class Cycle:
    def __init__(self, iterable: list):
        self.iterable = iterable
        self.pointer = -1

    def move(self, direction: int):
        if self.iterable:
            self.pointer = (self.pointer + direction) % len(self.iterable)
            return self.iterable[self.pointer]
        return None

    def __len__(self):
        return len(self.iterable)

    def current(self):
        if self.iterable:
            return self.iterable[self.pointer]
        return None
