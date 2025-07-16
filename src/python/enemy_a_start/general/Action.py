from abc import ABC, abstractmethod
class Action(ABC):
    @abstractmethod
    def apply(self, state):
        """Receives an state and returns another state.
        If the action is not possible returns an expception."""
        pass
    @abstractmethod
    def __str__(self):
        """A text representation of the action"""
        pass
    