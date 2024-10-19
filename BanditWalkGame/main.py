import random
import time

class Bandit:
    def __init__(self):
        # Bandit starting position
        self.currentPosX = 0
        self.currentPosY = 0
        self.isInHole = False
        self.banditIcon = 8
        self.isWin = False
        self.stepsTaken = 0
        self. grid = [
        [0, 0, 0, 0],
        [0, -100, 0, -100],
        [0, 0, 0, -100],
        [-100, 0, 0, 1000]
        ]
        
    def ResetBandit(self):
        self.currentPosX = 0
        self.currentPosY = 0
        self.isInHole = False
        self.banditIcon = 8
        self.isWin = False
        self.stepsTaken = 0
        self. grid = [
        [0, 0, 0, 0],
        [0, -100, 0, -100],
        [0, 0, 0, -100],
        [-100, 0, 0, 1000]
        ]

def main():
    
    player = Bandit()
    
    winResults = []
    stepsResults = []
    
    # 8 Represents the player.
    player.grid[player.currentPosX][player.currentPosY] = 8

    def ShowGrid():
        for i in player.grid:
            print(i)

    def SlipperyFloor(desired_direction):
        rng = random.randint(1, 3)
        if(rng == 1):
            print("Bandit Move Successful!")
            return desired_direction
        elif(rng == 2):
            print("Bandit Slipped!")
            if(desired_direction == 1 or desired_direction == 2):
                return 3
            elif(desired_direction == 3 or desired_direction == 4):
                return 1
        elif(rng == 3):
            print("Bandit Slipped!")
            if(desired_direction == 1 or desired_direction == 2):
                return 4
            elif(desired_direction == 3 or desired_direction == 4):
                return 2
        return -1
    
    def Move(desired_direction):
        
        if(player.isInHole):
            print("BANDIT IS STUCK, GAME OVER!")
            return
        
        player.grid[player.currentPosX][player.currentPosY] = 0
        
        # Go through RNG
        desired_direction = SlipperyFloor(desired_direction)
        
        if(desired_direction == 1):
            # Move Up
            player.currentPosX = max(player.currentPosX - 1, 0)
            print("Bandit Moved UP!")
        elif(desired_direction == 2):
            # Move Down
            player.currentPosX = min(player.currentPosX + 1, 3)
            print("Bandit Moved DOWN!")
        elif(desired_direction == 3):
            # Move Right
            player.currentPosY = min(player.currentPosY + 1, 3)
            print("Bandit Moved RIGHT!")
        elif(desired_direction == 4):
            # Move Left
            player.currentPosY = max(player.currentPosY - 1, 0)
            print("Bandit Moved LEFT!")
        
        if(player.grid[player.currentPosX][player.currentPosY] == -100):
            player.banditIcon = 2
            player.isInHole = True
        
        if(player.grid[player.currentPosX][player.currentPosY] == 1000):
            player.isWin = True
        
        player.stepsTaken += 1
        
        # Update Grid Visuals
        player.grid[player.currentPosX][player.currentPosY] = player.banditIcon
        ShowGrid()

    def TellPlayerLocation():
        print("PosX is: " + str(player.currentPosX))
        print("PosY is: " + str(player.currentPosY))
    
    # TODO: IMPLEMENT THE POLICIES

    def GoGetItPolicy():        
        while(player.isWin == False and player.isInHole == False):
            if(player.currentPosX == 0):
                if(player.currentPosY < 2):
                    Move(3)
                elif(player.currentPosY > 2):
                    Move(4)
                elif(player.currentPosY == 2):
                    Move(2)
                    
            elif(player.currentPosX == 1):
                if(player.currentPosY == 0 or player.currentPosY == 2):
                    Move(2)
                    
            elif(player.currentPosX == 2):
                if(player.currentPosY < 2):
                    Move(3)
                elif(player.currentPosY > 2):
                    Move(4)
                elif(player.currentPosY == 2):
                    Move(2)
            else:
                Move(3)
        # After Policy is finished.
        if(player.isWin):
            winResults.append(True)
        else:
            winResults.append(False)
            
        stepsResults.append(player.stepsTaken)
        
    
    # 1 - Up
    # 2 - Down
    # 3 - Right
    # 4 - Left
    for i in range(1, 4):
        GoGetItPolicy()
    
    # After Running Policy 3 times...
    print(winResults)
    print(stepsResults)
        
main()