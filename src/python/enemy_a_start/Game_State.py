from .general.State import State
from .actions.Walk_Left import  WalkLeft
from .actions.Walk_Right import  WalkRight
from .actions.Walk_Up import  WalkUp
from .actions.Walk_Down import  WalkDown
from .actions.Solve_Puzzle import SolvePuzzle
from .actions.Use_Door import UseDoor
from .Utils import Utils as Util



class GameState(State):
    "Player pos must be (x,y) pair"

    def __init__(self, player_pos=None, action=None,room=None, has_item_puzzle=False, has_won=False):
        self.player_pos = player_pos
        self.action=action
        self.room=room
        self.has_item_puzzle=has_item_puzzle
        self.has_won=has_won
        self.Actions = [WalkLeft(), WalkRight(), WalkUp(), WalkDown(), SolvePuzzle(), UseDoor()]
       

    def get_hash(self):
        if self.room.enemy:
            return str(self.player_pos)+str(self.has_item_puzzle)+str(self.has_won)+str(self.room.enemy.pos)
        return str(self.player_pos)+str(self.has_item_puzzle)+str(self.has_won)
    
    def is_goal(self):
        return self.has_won

    def get_sucessors(self):
        successors = []
        for action in self.Actions:  
            try:
                new_state = action.apply(self)  
                if new_state.room.enemy:
                    new_state = new_state.room.enemy.get_next_state(new_state)
                    new_state.room.update_items_pos()
                    
                successors.append(new_state)

            except Exception as e:
                pass
        return successors
    
    def get_succesors_for_score_computation(self):
        successors = []
        for action in self.Actions:  
            try:
                new_state = action.apply(self)  
                successors.append(new_state)

            except Exception as e:
                pass
        return successors

    def get_h(self, goal_state):
        if self.has_won==True: #If I have has_won in true, my heuristic is zero
            return 0
        if (self.has_item_puzzle==True): # If I already have the item puzzle, I just need to go to the door
            return Util.manhattan_distance(self.player_pos, self.room.door.pos)
        #If I don't have the item puzzle, I need to go from my position to the puzzle and from the puzzle to the door
        return Util.manhattan_distance(self.player_pos,self.room.puzzle.pos)+Util.manhattan_distance(self.room.puzzle.pos, self.room.door.pos)
    def copy(self):
        return GameState(player_pos=self.player_pos,room=self.room,has_item_puzzle=self.has_item_puzzle, has_won=self.has_won, action=self.action)
    
    def get_prev_action(self):
        return self.action
    
    
    def get_score(self, state):

        if not state.has_item_puzzle:
            return (Util.manhattan_distance(state.room.enemy.pos, state.room.puzzle.pos)*1.6+
                   Util.manhattan_distance(state.room.enemy.pos, state.player_pos)*1.4-
                    Util.manhattan_distance(state.player_pos, state.room.puzzle.pos)*0.1
                    )
        else:
            return (Util.manhattan_distance(state.room.enemy.pos, state.room.door.pos)*1.6+
                    Util.manhattan_distance(state.room.enemy.pos, state.player_pos)*1.4-
                    Util.manhattan_distance(state.player_pos, state.room.door.pos)*0.1
                    )

        
        
    

    
 
    
    def draw(self):
        msg=""
        for y in range(self.room.height-1,-1,-1):
            for x in range(self.room.width):
                if ((x,y)==self.player_pos): #PLAYER
                    msg+="P"
                elif (self.room.puzzle and (x,y)==self.room.puzzle.pos): # PUZZLE
                    msg+="?"
                elif (self.room.door and (x,y)==self.room.door.pos): # Door
                    msg+="D"
                elif (self.room.enemy and (x,y)==self.room.enemy.pos):
                    msg+="E"
                else:
                    msg+='_'
            msg+="\n"
        return msg
 
    def __str__(self):
        return f"""
{self.draw()}
"""
    





    

    


