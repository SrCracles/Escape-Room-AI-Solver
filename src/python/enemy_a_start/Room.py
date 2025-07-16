class Room:

    def __init__(self, number, width, height,puzzle=None, door=None, enemy=None,items_pos=None):
        self.items_pos=set()
        self.number = number
        self.width = width
        self.height = height
        self.puzzle=puzzle
        self.door=door
        self.enemy=enemy
        if (puzzle!=None):
            self.items_pos.add(puzzle.pos)
        if (door!=None):
            self.items_pos.add(door.pos)
        if (enemy!=None):
            self.items_pos.add(enemy.pos)
        
    def __str__(self):
        return f"Room(Number: {self.number}, Width: {self.width}, Height: {self.height})"
    
    def get_prev_action(self):
        return self.action
    
    def update_items_pos(self):
        self.items_pos.clear()  # Limpia las posiciones anteriores
        if self.puzzle is not None:
            self.items_pos.add(self.puzzle.pos)
        if self.door is not None:
            self.items_pos.add(self.door.pos)
        if self.enemy is not None:
            self.items_pos.add(self.enemy.pos)


    

