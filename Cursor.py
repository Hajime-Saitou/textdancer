# textdancer
# https://github.com/Hajime-Saitou/textdancer
#
# Copyright (c) 2026 Hajime Saito
# MIT License

class RangeCursor:
    def __init__(self, minPosition:int, maxPosition:int, position:int=None):
        if minPosition > maxPosition:
            raise ValueError(f"minPosition {minPosition} cannot be greater than maxPosition {maxPosition}")
        
        self.position = position if position is not None else minPosition
        self.minPosition = minPosition
        self.maxPosition = maxPosition

        if self.isOutOfBounds():
            raise ValueError(f"position {position} is out of bounds (minPosition: {minPosition}, maxPosition: {maxPosition})")

    def __iadd__(self, value):
        self.position += value
        return self
    
    def __isub__(self, value):
        self.position -= value
        return self

    def current(self) -> int:
        return self.position

    def next(self):
        self.position += 1
        return self.current()

    def previous(self):
        self.position -= 1
        return self.current()

    def hasNext(self) -> bool:
        return self.position <= self.maxPosition

    def hasPrevious(self) -> bool:
        return self.position > self.minPosition

    def isOutOfBounds(self) -> bool:
        return self.position < self.minPosition or self.position > self.maxPosition

    def top(self):
        self.position = self.minPosition

    def bottom(self):
        self.position = self.maxPosition

    def clone(self):
        return RangeCursor(self.minPosition, self.maxPosition, self.position)

class SubscriptCursor(RangeCursor):
    def __init__(self, size:int, position:int=None):
        if size < 1:
            size = 1

        super().__init__(0, size - 1, position)
        self.size = size

    def clone(self):
        return SubscriptCursor(self.size, self.position)

    def updateSize(self, size:int):
        self.size = size
        self.maxPosition = size - 1
