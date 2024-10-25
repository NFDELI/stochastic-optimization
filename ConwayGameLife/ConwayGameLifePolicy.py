import sys
import random

sys.path.append("./")
from BaseClasses.SDPPolicy import SDPPolicy

class ConwayGameOfLifePolicy(SDPPolicy):
    def __init__(self, model, policy_name = "RandomConwayPolicy"):
        super().__init__(model, policy_name)
    
    def get_decision(self, state, t, T):
        # Randomly Initialize the Grid at the start.
        
        if (t == 0):
            grid = state.grid
            for i in range(self.model.grid_size):
                for j in range(self.model.grid_size):
                    grid[i][j].is_alive = random.choice([True, False])
                    
                    
            # No decisions to be made.
            return {}
        return {}

class FixedConwayGameOfLifePolicy(SDPPolicy):
    def __init__(self, model, policy_name = "FixedConwayPolicy"):
        super().__init__(model, policy_name)
    
    def get_decision(self, state, t, T):
        # Randomly Initialize the Grid at the start.
        
        if (t == 0):
            grid = state.grid
            for i in range(self.model.grid_size):
                for j in range(self.model.grid_size):
                    grid[i][j].is_alive = False
            
            # grid[25][25].is_alive = True
            # grid[25][26].is_alive = True
            # grid[26][26].is_alive = True
            
            # grid[29][29].is_alive = True
            # grid[30][29].is_alive = True
            # grid[33][29].is_alive = True
            
            grid[0][0].is_alive = True
            
            grid[25][25].is_alive = True
            grid[26][25].is_alive = True
            grid[25][26].is_alive = True
            grid[24][24].is_alive = True
            
            # No decisions to be made.
            return {}
        return {}