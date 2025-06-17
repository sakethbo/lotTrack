from typing import List, Tuple
from abc import ABC, abstractmethod

class PlayType(ABC):
    """Base class for all play types."""
    
    def __init__(self, numbers: str):
        self.numbers = numbers
        
    @abstractmethod
    def calculate_prize(self, ticket: List[str], winning: List[str]) -> Tuple[bool, float]:
        """Calculate if ticket wins and prize amount."""
        pass
        
    @classmethod
    def create(cls, play_type: str, numbers: str) -> 'PlayType':
        """Create a play type instance."""
        if play_type == 'straight':
            return Straight(numbers)
        elif play_type == 'box':
            return Box(numbers)
        elif play_type == 'straightbox':
            return StraightBox(numbers)
        elif play_type == 'combo':
            return Combo(numbers)
        elif play_type == 'oneoff':
            return OneOff(numbers)
        return None

class Straight(PlayType):
    """Straight play - numbers must match in exact order."""
    
    def calculate_prize(self, ticket: List[str], winning: List[str]) -> Tuple[bool, float]:
        if ticket == winning:
            return True, 5000.0
        return False, 0.0

class Box(PlayType):
    """Box play - numbers must match in any order."""
    
    def calculate_prize(self, ticket: List[str], winning: List[str]) -> Tuple[bool, float]:
        if sorted(ticket) == sorted(winning):
            return True, 500.0
        return False, 0.0

class StraightBox(PlayType):
    """Straight/Box play - wins on either straight or box."""
    
    def calculate_prize(self, ticket: List[str], winning: List[str]) -> Tuple[bool, float]:
        if ticket == winning:
            return True, 5500.0  # Straight + Box prize
        if sorted(ticket) == sorted(winning):
            return True, 500.0
        return False, 0.0

class Combo(PlayType):
    """Combo play - all possible straight combinations."""
    
    def calculate_prize(self, ticket: List[str], winning: List[str]) -> Tuple[bool, float]:
        if ticket == winning:
            return True, 5000.0
        return False, 0.0

class OneOff(PlayType):
    """One-Off play - one digit can be off by one."""
    
    def calculate_prize(self, ticket: List[str], winning: List[str]) -> Tuple[bool, float]:
        if ticket == winning:
            return True, 5000.0
        if len(ticket) != len(winning):
            return False, 0.0
            
        # Check if exactly one digit is off by one
        differences = 0
        for t, w in zip(ticket, winning):
            if abs(int(t) - int(w)) == 1:
                differences += 1
            elif t != w:
                return False, 0.0
                
        return differences == 1, 1000.0 