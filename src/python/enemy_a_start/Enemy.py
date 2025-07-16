import copy
from .Item import Item
from .Minimax import minimax
from .Utils import Utils as Util
from .Game_State import GameState

class Enemy(Item):
    def __init__(self, pos=None):
        super().__init__(pos)

    import copy

    def get_successors(self, state):
        successors = []

        try:
            successors.append(self.walk_right(copy.deepcopy(state)))
        except:
            pass
        try:
            successors.append(self.walk_left(copy.deepcopy(state)))
        except:
            pass
        try:
            successors.append(self.walk_up(copy.deepcopy(state)))
        except:
            pass
        try:
            successors.append(self.walk_down(copy.deepcopy(state)))
        except:
            pass
        return successors


    def walk_right(self, state):
        # print("------------")
        # print("ESTADO QUE RECIBO EN WALK RIGHT")
        # print(state)
        # print("------------")
        cloned_state = copy.deepcopy(state)
        x, y = state.room.enemy.pos
        new_pos = (x + 1, y)
        if not (0 <= new_pos[0] < cloned_state.room.width and 0 <= new_pos[1] < cloned_state.room.height):
            raise ValueError("Invalid position")
        if new_pos in cloned_state.room.items_pos or new_pos==state.player_pos:
            raise ValueError("Item at the same position")
        cloned_state.room.enemy = Enemy(new_pos)
        return cloned_state

    def walk_left(self, state):
        # print("------------")
        # print("ESTADO QUE RECIBO EN WALK LEFT")
        # print(state)
        # print("------------")
        cloned_state = copy.deepcopy(state)
        x, y = state.room.enemy.pos
        new_pos = (x - 1, y)
        if not (0 <= new_pos[0] < cloned_state.room.width and 0 <= new_pos[1] < cloned_state.room.height):
            raise ValueError("Invalid position")
        if new_pos in cloned_state.room.items_pos or new_pos==state.player_pos:
            raise ValueError("Item at the same position")
        cloned_state.room.enemy = Enemy(new_pos)
        return cloned_state

    def walk_up(self, state):
        # print("------------")
        # print("ESTADO QUE RECIBO EN WALK UP")
        # print(state)
        # print("------------")
        cloned_state = copy.deepcopy(state)
        x, y = state.room.enemy.pos
        new_pos = (x, y + 1)
        if not (0 <= new_pos[0] < cloned_state.room.width and 0 <= new_pos[1] < cloned_state.room.height):
            raise ValueError("Invalid position")
        if new_pos in cloned_state.room.items_pos or new_pos==state.player_pos:
            raise ValueError("Item at the same position")
        cloned_state.room.enemy = Enemy(new_pos)
        return cloned_state

    def walk_down(self, state):
        # print("------------")
        # print("ESTADO QUE RECIBO EN WALK DOWN")
        # print(state)
        # print("------------")
        cloned_state = copy.deepcopy(state)
        x, y = state.room.enemy.pos
        new_pos = (x, y - 1)
        if not (0 <= new_pos[0] < cloned_state.room.width and 0 <= new_pos[1] < cloned_state.room.height):
            raise ValueError("Invalid position")
        if new_pos in cloned_state.room.items_pos or new_pos==state.player_pos:
            raise ValueError("Item at the same position")
        cloned_state.room.enemy = Enemy(new_pos)
        return cloned_state

    def get_next_state(self, state):
        score, next_state = minimax(depth=4, current_game_state=state, final_game_state=state, turn=0)
        return next_state

