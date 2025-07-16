from ..general.Action import Action


class WalkLeft(Action):
    def apply(self, state):
        x, y = state.player_pos
        new_pos = (x - 1, y)

        if not (0 <= new_pos[0] < state.room.width and 0 <= new_pos[1] < state.room.height):
            raise ValueError(f" Invalid pos {new_pos} for room ({state.room.width}, {state.room.height})")
        if new_pos in state.room.items_pos:
            raise ValueError(f"Item at the same position")

        cloned_state = state.copy()  
        cloned_state.player_pos = new_pos
        cloned_state.action = "Walk Left"  
        return cloned_state
    
    def __str__(self):
        return "Walk Left"