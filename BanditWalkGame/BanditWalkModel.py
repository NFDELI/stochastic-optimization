import sys

sys.path.append("./")
from collections import namedtuple
from BaseClasses.SDPModel import SDPModel
import pandas as pd

class BanditWalkModel(SDPModel):
    def __init__(
        self,
        stateNames = ["posX", "posY", "isInHole", "isWin", "stepsTaken"],
        decisionNames = ["direction"],
        t0 = 0,
        T = 1000
    ):
        initialState = {"posX": 0, "posY": 0, "isInHole": False, "isWin": False, "stepsTaken": 0}
        super().__init__(stateNames, decisionNames, initialState, t0, T)
        
        self.grid = [
            [0, 0, 0, 0],
            [0, -100, 0, -100],
            [0, 0, 0, -100],
            [-100, 0, 0, 1000]
        ]
    
    def exog_info_fn(self, decision):
        rng = self.prng.randint(1, 4)
        direction = decision.direction
        if(rng == 2):
            if(direction in [1, 2]):
                direction = 3
            else:
                direction = 1
        elif(rng == 3):
            if(direction in [1, 2]):
                direction = 4
            else:
                direction = 2
        return {"direction": direction}
    
    def transition_fn(self, decision, exog_info):
        x = self.state.posX
        y = self.state.posY
        direction = exog_info["direction"]
        
        if(direction == 1):
            # Go Up
            x = max(x - 1, 0)
        elif(direction == 2):
            # Go Down
            x = min(x + 1, 3)
        elif(direction == 3):
            # Go Right
            y = min(y + 1, 3)
        elif(direction == 4):
            y = max(y - 1, 0)
        
        # Check if bandit fell into hole.
        if(self.grid[x][y] == -100):
            inHole = True
        else:
            inHole = False
        
        if(self.grid[x][y] == 1000):
            isWin = True
        else:
            isWin = False
        
        return {"posX": x, "posY": y, "isInHole": inHole, "isWin": isWin, "stepsTaken": self.state.stepsTaken + 1}
    
    def objective_fn(self, decision, exog_info):
        x, y = self.state.posX, self.state.posY
        return self.grid[int(x)][int(y)]
    
    def is_finished(self):
        return self.state.isInHole or self.state.isWin 
        
            
        

    
    
