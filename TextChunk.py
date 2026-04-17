# bagatelle
# https://github.com/Hajime-Saitou/bagatelle
#
# Copyright (c) 2026 Hajime Saito
# MIT License
import re
import os
from Cursor import Cursor

class TextChunk(list[str]):
    def __init__(self, lines:list[str]=[]):
        super().__init__(lines)
        self.cursor = Cursor
        self.updateCursorSize()

    def loadFromFile(self, filename:str, encoding:str="utf-8"):
        self.clear()
        self.appendFromFile(filename, encoding)
        self.updateCursorSize()

    def appendFromFile(self, filename:str, encoding:str="utf-8"):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        with open(filename, "r", encoding=encoding) as f:
            self.extend(f.read().splitlines())

        self.updateCursorSize()

    def saveToFile(self, filename:str, encoding:str="utf-8"):
        with open(filename, "w", encoding=encoding) as f:
            f.write("\n".join(self))

    def forwardSearch(self, keywords:list) -> int:
        for index, line in enumerate(self):
            if self.matches(line, keywords):
                return index
        else:
            return -1

    def backwardSearch(self, keywords:list) -> int:
        for index, line in enumerate(reversed(self)):
            if self.matches(line, keywords):
                return len(self) - 1 - index
        else:
            return -1

    def matches(self, line:str, keywords:list):
        return any(re.match(keyword, line) for keyword in keywords)

    def pickFrom(self, startKeywords:list):
        startIndex = self.forwardSearch(startKeywords)
        return TextChunk(self[startIndex:] if startIndex != -1 else [])

    def pickTo(self, endKeywords:list):
        endIndex:int = self.forwardSearch(endKeywords)
        return TextChunk(self[:endIndex if endIndex != -1 else len(self)])
    
    def pick(self, startKeywords:list, endKeywords:list):
        return TextChunk(self.pickFrom(startKeywords).pickTo(endKeywords))

    def filter(self, keywords:list):
        return TextChunk([line for line in self if self.matches(line, keywords)])
    
    def toList(self) -> list:
        return self

    # with Cursor
    def updateCursorSize(self):
        self.cursor.size = len(self)

    def fetchNext(self) -> str:
        return self[self.cursor.next()]
    
    def fetchPrevious(self) -> str:
        return self[self.cursor.previous()]
    
    def fetchCurrent(self) -> str:
        return self[self.cursor.current()]
    
    def pickRange(self, startPosition:int=None, endPosition:int=None):
        startPosition = startPosition if startPosition is not None else self.cursor.current()
        endPosition = endPosition if endPosition is not None else len(self)
        return TextChunk(self[startPosition, endPosition])
