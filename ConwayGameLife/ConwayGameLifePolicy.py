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