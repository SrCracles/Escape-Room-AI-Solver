from .Room import Room
from .Game_State import GameState
from .Puzzle import Puzzle
from .Door import Door
from .Enemy import Enemy
class GameConstants:
    
    def __init__(self):
        self.init_lvl_1()
        self.init_lvl_2()
        self.init_lvl_3()
    
    

        
    def __str__(self):
        return f"GameConstants(Room: {self.room1})"
    
    def init_lvl_1(self): 
        #Rooms inicialization
        door_1=Door(pos=(9,1))
        room_1 = Room(number=1, width=10, height=3,puzzle=None,door=door_1)
        #Initial position
        initial_player_pos=(0, 1)
        #Final position
        final_player_pos=(9,1)
        

        self.initial_state_1=GameState(player_pos=initial_player_pos,room=room_1,has_item_puzzle=True)
        self.final_state_1=GameState(player_pos=final_player_pos,room=room_1,has_item_puzzle=True,has_won=True)
    
    def lvl_1_get_initial_state(self):
        return self.initial_state_1
    
    def lvl_1_get_final_state(self):
        return self.final_state_1
    

    #####

    def init_lvl_2(self):
        #Rooms inicialization
        puzzle_2= Puzzle(pos=(14,2))
        door_2=Door(pos=(14,0))
        room_2 = Room(number=1, width=15, height=3,puzzle=puzzle_2,door=door_2)
        #Initial position
        initial_player_pos=(0, 1)
        #Final position
        final_player_pos=(5,2)
        
        self.initial_state_2=GameState(player_pos=initial_player_pos,room=room_2,has_item_puzzle=False)
        self.final_state_2=GameState(player_pos=final_player_pos,room=room_2,has_item_puzzle=True,has_won=True)
    
    def lvl_2_get_initial_state(self):
        return self.initial_state_2
    
    def lvl_2_get_final_state(self):
        return self.final_state_2
    
    #### 

    def init_lvl_3(self):
        #Rooms inicialization
        
        puzzle_3= Puzzle(pos=(13,2))
        door_3=Door(pos=(5,0))
        enemy_3=Enemy(pos=(12,2))
        
        room_3 = Room(number=1, width=14, height=4,puzzle=puzzle_3,door=door_3,enemy=enemy_3)
        #Initial position
        initial_player_pos=(0, 1)
        #Final position
        final_player_pos=(5,2)
        
        #
        self.initial_state_3=GameState(player_pos=initial_player_pos,room=room_3,has_item_puzzle=False)
        self.final_state_3=GameState(player_pos=final_player_pos,room=room_3,has_item_puzzle=True,has_won=True)

    
    def lvl_3_get_initial_state(self):
        return self.initial_state_3
    
    def lvl_3_get_final_state(self):
        return self.final_state_3
    
    
        

