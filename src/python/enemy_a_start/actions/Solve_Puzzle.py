from ..general.Action import Action
from ..Utils import Utils as Util
class SolvePuzzle(Action):
    def apply(self, state):
        player_pos = state.player_pos
        
        if state.room.puzzle == None:
            raise ValueError(f"No item puzzle in room")
        else:
            puzzle_pos=state.room.puzzle.pos

        if state.has_item_puzzle==True:
            raise ValueError(f"Player already has item puzzle")
        if Util.manhattan_distance(player_pos,puzzle_pos)>1:
            raise ValueError(f"Player is too far from puzzle")
        
        cloned_state = state.copy()
        cloned_state.has_item_puzzle = True
        cloned_state.action = "Solve puzzle"
        
        return cloned_state
        

            

    def __str__(self):
        return "Puzzle"