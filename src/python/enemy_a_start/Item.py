from abc import ABC, abstractmethod

class Item(ABC):
    def __init__(self, pos=None):
        self.pos = pos

    def __str__(self):
        return f"Item at position {self.pos}"

    
