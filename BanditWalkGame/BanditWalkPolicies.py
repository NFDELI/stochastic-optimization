import sys

sys.path.append("./")
from BaseClasses.SDPModel import SDPModel
from BaseClasses.SDPPolicy import SDPPolicy

class GoGetItPolicy(SDPPolicy):
    def get_decision(self, state, t, T):
        x = state.posX
        y = state.posY

        # 1 is Up
        # 2 is Down
        # 3 is Right
        # 4 is Left
        
        # First Row
        if(x == 0):
            if(y < 2):
                return {"direction": 3}
            elif(y > 2):
                return {"direction": 4}
            else:
                return {"direction": 2}
        
        # Second Row
        elif(x == 1):
            if(y == 0 or y == 2):
                return {"direction": 2}
            
        # Third Row
        elif(x == 2):
            if(y < 2):
                return {"direction": 3}
            elif(y > 2):
                return {"direction": 4}
            else:
                return {"direction": 2}
        # Fourth Row
        else:
            return {"direction": 3}
            