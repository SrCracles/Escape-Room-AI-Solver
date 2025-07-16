from ..general.Action import Action

class WalkUp(Action):
    def apply(self, state):
        cloned_state = state.copy()
        x, y = cloned_state.player_pos
        new_pos = (x, y + 1)
        if not (0 <= new_pos[0] < state.room.width and 0 <= new_pos[1] < state.room.height):
            raise ValueError(f"Invalid pos {new_pos} for room ({state.room.width}, {state.room.height})")
        
        if new_pos in state.room.items_pos:
            raise ValueError(f"Item at the same position")
        cloned_state.player_pos = new_pos
        cloned_state.action = "Walk up"
        
        return cloned_state
    def __str__(self):
        return "Walk Up"
