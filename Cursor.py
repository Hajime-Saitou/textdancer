# bagatelle
# https://github.com/Hajime-Saitou/bagatelle
#
# Copyright (c) 2026 Hajime Saito
# MIT License

class Cursor:
    def __init__(self, size:int):
        self.position = 0
        self.size = 0

    def current(self) -> int:
        return self.position

    def next(self):
        self.position += 1
        return self.current()

    def previous(self):
        self.position -= 1
        return self.current()

    def hasNext(self) -> bool:
        return self.position < self.size

    def hasPrevious(self) -> bool:
        return self.position > 0
