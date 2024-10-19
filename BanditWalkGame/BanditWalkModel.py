import sys

sys.path.append("./")
from BaseClasses.SDPModel import SDPModel
import pandas as pd

class BanditWalkMode(SDPModel):
    def __init__(
        self,
        S0: dict,
        t0: float = 0,
        T: float = 1,
        seed: int = 42,
        # Bandit starting position
        currentPosX: int = 0,
        currentPosY: int = 0,
        isInHole: bool = False,
        banditIcon: int = 8,
        isWin: bool =  False,
        stepsTaken: int = 0,
    ) -> None:
        states = [0, 1, 2, 3,
                    4, 5, 6, 7,
                    8, 9, 10, 11,
                    12, 13, 14, 15]
            
        decisionNames = ["Up", "Down", "Left", "Right"]
        super().__init__(states, decisionNames, S0, t0, T, seed)
        self.currentPosX = currentPosX
        self.currentPosY = currentPosY
        self.isInHole = isInHole
        self.banditIcon = banditIcon
        self.isWin = isWin
        stepsTaken = stepsTaken
    
    def is_finished(self):
        isStuck = self.isInHole
        isWin = self.isWin
        return super().is_finished() or isStuck or isWin
    
    def exog_info_fn(self, decision):
        coin = self.prng.uniform()
        

    
    
