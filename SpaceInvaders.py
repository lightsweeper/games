'''
Aliens are invading! Grab the nearest space fighter and take 'em down!

Step on the bottom row to shoot at the ships from that position. May the best planetary civilization win!
'''

from lightsweeper.lsapi import *
import math
import random

class SpaceInvaders(LSGame):
    def init(game):
        game.enemyShips = [Shapes.H + Shapes.SEG_D, Shapes.o + Shapes.SEG_A, Shapes.SEG_B + Shapes.SEG_E + Shapes.SEG_G, Shapes.SEG_A + Shapes.SEG_C  + Shapes.SEG_E]
        game.enemyColors = [Colors.RANDOM() for ship in game.enemyShips]
        
        i = 0
        game.ships = [[None for col in range(game.cols)] for row in range(game.rows)]
        for row in range(1, game.rows - 3):
            for col in range(1, game.cols - 2):
                game.ships[row][col] = i
            i = (i + 1) % len(game.enemyShips)
        game.distFromFirstCol = 1
        game.distFromLastCol = 2
        game.distFromBottom = 3      
        
    def heartbeat(game, moves):  
        won = True
        # display ships and check for win state
        for row in range(game.rows):
            for col in range(game.cols):
                if game.ships[row][col] is not None:
                    won = False
                    i = game.ships[row][col]
                    game.display.set(row,col,game.enemyShips[i], game.enemyColors[i])  
                else:
                    game.display.set(row,col,Shapes.ZERO,Colors.BLACK)
        game.display.setRow(game.rows-1, Shapes.UNDERSCORE, Colors.WHITE)

        if won:
            game.ended = True
        
        # recalculate how far the bottom row of ships is from the bottom
        for row in range(game.rows-1, -1, -1):
            for col in range(game.cols):
                if game.ships[row][col] is not None:
                    game.distFromBottom = game.rows - row - 1

        if random.randint(0, game.frameRate * 3) == 0 and game.distFromFirstCol > 0:
            game.moveShips('left')
            game.distFromFirstCol -= 1
            game.distFromLastCol += 1
        if random.randint(0, game.frameRate * 3) == 0 and game.distFromLastCol > 0:
            game.moveShips('right')
            game.distFromFirstCol += 1
            game.distFromLastCol -= 1
        if random.randint(0, game.frameRate * 5) == 0:
            game.moveShips('down')
            game.distFromBottom -= 1

        if game.distFromBottom == 0:
            game.ended = True

    def moveShips(game,d):
        if d == 'left':
            for row in range(game.rows):
                for col in range(game.cols):        
                    if game.ships[row][col] is not None:
                        game.ships[row][col-1] = game.ships[row][col]
                        game.ships[row][col] = None
        if d == 'right':
            for row in range(game.rows):
                for col in range(game.cols-1, -1, -1):
                    if game.ships[row][col] is not None:
                        game.ships[row][col+1] = game.ships[row][col]
                        game.ships[row][col] = None
        if d == 'down':
            for row in range(game.rows-1,-1,-1):
                for col in range(game.cols):
                    if game.ships[row][col] is not None:
                        game.ships[row+1][col] = game.ships[row][col]
                        game.ships[row][col] = None

    def stepOn(game, row, col):
        if row == game.rows - 1:
            for r in range(game.rows-1, -1, -1):
                if game.ships[r][col] is not None:
                    print('hit!!!1')
                    game.ships[r][col] = None
                    game.audio.playSound('Explosion.wav')
                    return

    def stepOff(game, row, col):
        pass

def main():
    gameEngine = LSGameEngine(SpaceInvaders)
    gameEngine.beginLoop()

if __name__ == "__main__":
    main()
