import sys

sys.path.append("./")
from collections import namedtuple
from BaseClasses.SDPModel import SDPModel
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import clear_output

class Tile:
    def __init__(self, is_alive = False):
        self.is_alive = is_alive
        if(self.is_alive == True):
            self.generation = 0
        else:
            self.generation = -1
    
    def SurvivedGeneration(self):
        if(self.is_alive):
            self.generation += 1
    
    def __str__(self):
        return f"{'Alive' if self.is_alive else 'Dead'}, Generation: {self.generation}"

class ConwayGameLife(SDPModel):
    def __init__(self, grid_size, t0 = 0, T = 10, seed = 42):
        state_names = ['grid']
        decision_names = []
        S0 = {'grid': self.InitialState(grid_size)}
        super().__init__(state_names, decision_names, S0, t0, T, seed)
        self.grid_size = grid_size
    
    def InitialState(self, grid_size):
        grid = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                tile = Tile(is_alive = False)
                row.append(tile)
            grid.append(row)
        return grid

    def GetNextGrid(self):
        nextGrid = []
        for i in range(self.grid_size):
            row = [Tile() for _ in range(self.grid_size)]
            nextGrid.append(row)
        return nextGrid
    
    def transition_fn(self, decision, current_state):
    
        current_state = self.state.grid
        next_grid = self.GetNextGrid()
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                alive_neighbours = self.CountAliveNeighbours(current_state, i, j)
                
                # When the current tile is Alive...
                if(current_state[i][j].is_alive == True):
                    if(alive_neighbours == 2 or alive_neighbours == 3):
                        # Stable, stay alive.
                        next_grid[i][j].is_alive = True
                        next_grid[i][j].generation = current_state[i][j].generation + 1
                    
                    else:
                        # Over crowded or too lonely...
                        next_grid[i][j].is_alive = False
                        next_grid[i][j].generation = -1
                else:
                    # When the current tile is Dead...
                    if(alive_neighbours == 3):
                        # A tile is born!
                        next_grid[i][j].is_alive = True
                        next_grid[i][j].generation = 0
        
        self.Visualize(current_state)
        # Every tile has been checked and updated!
        return {'grid': next_grid}
    
    def exog_info_fn(self, decision):
        
        # No known Exogenous Information.
        
        return {}
    
    def objective_fn(self, decision, exog_info):
        alive_tiles = 0
        for row in self.state.grid:
            for tile in row:
                if(tile.is_alive):
                    alive_tiles += 1
        return alive_tiles
    
    def CountAliveNeighbours(self, grid, x, y):
        directions_to_check = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
        ]
        aliveNeighbours = 0
        for directionX, directionY in directions_to_check:
            offsetX = x + directionX
            offsetY = y + directionY
            if (0 <= offsetX < self.grid_size) and (0 <= offsetY < self.grid_size):
                if(grid[offsetX][offsetY].is_alive):
                    aliveNeighbours += 1
        return aliveNeighbours
    
    def Visualize(self, grid):
        plt.clf()
        visual_grid = np.zeros((self.grid_size, self.grid_size))
        
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if (grid[i][j].is_alive):
                    visual_grid[i][j] = 1
                else:
                    visual_grid[i][j] = 0
    
        #plt.imshow(visual_grid, cmap = "binary", interpolation = "nearest")
        plt.imshow(visual_grid, cmap = "binary")
        plt.title("Current State")
        plt.axis('off')
        
        plt.pause(0.5)
        
        plt.draw()
        
                