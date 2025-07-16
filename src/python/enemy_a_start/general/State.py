from abc import ABC, abstractmethod
import copy
class State(ABC):
    @abstractmethod
    def get_hash(self):
        pass
    @abstractmethod
    def get_sucessors(self):
        pass
    @abstractmethod
    def get_h(self, goal_state):
        pass

    @abstractmethod
    def is_goal(self):
        """Says whether current state is a goal"""
        pass
   
    def copy(self):
        """Returns a copy"""
        return copy.deepcopy(self)
    
    

    
