from ..general.Action import Action
from ..Utils import Utils as Util
class UseDoor(Action):
    def apply(self, state):
        player_pos = state.player_pos
        
        if state.room.door == None:
            raise ValueError(f"No door in room")
        else:
            door_pos=state.room.door.pos
        if not state.has_item_puzzle:
            raise ValueError(f"Player needs item puzzle")
        if Util.manhattan_distance(player_pos,door_pos)>1:
            raise ValueError(f"Player is too far from door")
        cloned_state = state.copy()
        cloned_state.action = "Use door"
        cloned_state.has_won =True
        return cloned_state

            

    def __str__(self):
        return "Use door"