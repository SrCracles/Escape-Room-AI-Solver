from .Item import Item


class Door(Item):
    def __init__(self, pos=None):
        super().__init__(pos)
    
    def __str__(self):
        return f"Puzzle at position {self.pos}"