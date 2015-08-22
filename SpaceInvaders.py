'''
Aliens are invading! Grab the nearest space fighter and take 'em down!

Step on the bottom row to shoot at the ships from that position. May the best planetary civilization win!
'''

from lightsweeper.lsapi import *
import math
import random

LASER_SPEED = 2 # frames

class SpaceInvaders(LSGame):
    def init(game):
        game.enemyShips = [Shapes.H + Shapes.SEG_D, Shapes.o + Shapes.SEG_A, Shapes.SEG_B + Shapes.SEG_E + Shapes.SEG_G, Shapes.SEG_A + Shapes.SEG_C  + Shapes.SEG_E, Shapes.H - Shapes.SEG_G]
        game.enemyColors = [Colors.RANDOM(game.enemyShips) for ship in game.enemyShips]
        
        i = 0
        game.ships = [[None for col in range(game.cols)] for row in range(game.rows)]
        for row in range(1, game.rows - 3):
            for col in range(1, game.cols - 2):
                game.ships[row][col] = i
            i = random.randint(0,len(game.enemyShips)-1)# % len(game.enemyShips)
        game.distFromFirstCol = 1
        game.distFromLastCol = 2
        game.distFromBottom = 2

        game.lasers = [] # (row, col, frames since last move)
        game.audio.playSound('Space invaders remix.ogg')
        game.state = 'playing'
        game.frameCounter = 0
        
        game.score = 0
        game.speed = 1.
        
    def heartbeat(game, moves):
        if game.state is 'playing':
            # recalculate how far the bottom row of ships is from the bottom
            for row in range(game.rows):
                for col in range(game.cols):
                    if game.ships[row][col] is not None:
                        game.distFromBottom = game.rows - row - 1
        
            if random.random() < 0.05 * game.speed and game.distFromFirstCol > 0:
                game.moveShips('left')
                game.distFromFirstCol -= 1
                game.distFromLastCol += 1
            if random.random() < 0.05 * game.speed and game.distFromLastCol > 0:
                game.moveShips('right')
                game.distFromFirstCol += 1
                game.distFromLastCol -= 1
            if random.random() < 0.01 * game.speed:
                game.moveShips('down')
                game.distFromBottom -= 1
                ship = random.randint(0,len(game.enemyShips)-1)# % len(game.enemyShips)
                for col in range(game.distFromFirstCol, game.cols-game.distFromLastCol):
                    game.ships[1][col] = ship            

            # display ships and check for win state
            game.display.setRow(game.rows-1, Shapes.UNDERSCORE, Colors.WHITE)            
            for row in range(game.rows):
                for col in range(game.cols):
                    if game.ships[row][col] is not None:
                        #won = False
                        i = game.ships[row][col]
                        game.display.set(row, col, game.enemyShips[i], game.enemyColors[i])  
                    elif row != game.rows-1:
                        game.display.set(row,col,Shapes.ZERO,Colors.BLACK)
            
            game.display.setRow(0, Shapes.UNDERSCORE, Colors.YELLOW)

            if game.score < 20:
                game.display.set(0, 0, Shapes.digitToHex(math.floor(game.score / 10)), Colors.WHITE)
                game.display.set(0, 1, Shapes.digitToHex(game.score % 10), Colors.WHITE)
                #game.display.setMessage(0, 'saturn', color = Colors.RANDOM())    
            elif game.score < 40:
                game.display.setMessage(0, 'yes', color = Colors.RANDOM())
            elif game.score < 60:
                game.display.setMessage(0, 'lasers', color = Colors.RANDOM())
            elif game.score < 80:
                game.display.setMessage(0, 'cats', color = Colors.RANDOM())
            elif game.score < 100:
                game.display.setMessage(0, 'pizza', color = Colors.RANDOM())
            elif game.score < 150:
                game.display.setMessage(0, 'space', color = Colors.RANDOM())
            elif game.score < 200:
                game.display.setMessage(0, 'moon', color = Colors.RANDOM())
            elif game.score < 300:
                game.display.setMessage(0, 'mars', color = Colors.RANDOM())
            elif game.score < 400:
                game.display.setMessage(0, 'ceres', color = Colors.RANDOM())
            elif game.score < 500:
                game.display.setMessage(0, 'jupiter', color = Colors.RANDOM())
            elif game.score < 600:
                game.display.setMessage(0, 'saturn', color = Colors.RANDOM())
            elif game.score < 700:
                game.display.setMessage(0, 'pluto', color = Colors.RANDOM())
            elif game.score < 2000:
                game.display.setMessage(0, 'galaxy', color = Colors.RANDOM())
            else:
                game.display.setMessage(0, 'infinity', color = Colors.RANDOM())
# alphabet: a,b,c,d,e,f,g,h,i,j,k,l,n,o,p,q,r,t,u,s,v,x,y,z
            # display lasers and check for destroyed ships
            for laser in game.lasers:
                game.display.set(laser[0],laser[1],Shapes.SEG_C,Colors.RED)            
                if laser[2] > LASER_SPEED and game.ships[laser[0]][laser[1]] is not None:
                    game.ships[laser[0]][laser[1]] = None
                    game.audio.playSound('Explosion.wav')
                    game.display.set(laser[0], laser[1], Shapes.ZERO, Colors.BLACK)
                    game.score += 1
                    laser[0] = -1
                elif laser[2] > LASER_SPEED:
                    laser[0] -= 1
                    laser[2] = 0
                else:
                    laser[2] += 1
                
            game.lasers = [laser for laser in game.lasers if laser[0] > 0]

            #if won:
            #    game.state = 'won'
            #    game.audio.stopSounds()
            #    game.audio.playSound('Success.wav')
            
            if game.distFromBottom == 0:
                game.state = 'lost'
                game.audio.stopSounds()
                game.audio.playSound('big explosion.wav')

            game.speed += 0.001
        if game.state is 'lost':
            #if game.frameCounter == 1:   
            if game.frameCounter < 100:
                game.frameCounter += 1
                if game.frameCounter % 5 == 0:
                    game.display.set(random.randint(0,game.rows-1),random.randint(0,game.cols-1),
                                     Shapes.H, Colors.RED) 
            else:
                game.ended = True
        if game.state is 'won':
            if game.frameCounter < 100:
                game.frameCounter += 1
                if game.frameCounter % 5 == 0:
                    game.display.set(random.randint(0,game.rows-1),random.randint(0,game.cols-1),
                                     Shapes.ZERO, Colors.RANDOM()) 
            else:
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
            print('down', game.distFromBottom)
            for row in range(game.rows-1,-1,-1):
                for col in range(game.cols):
                    if game.ships[row][col] is not None:
                        game.ships[row+1][col] = game.ships[row][col]
                        game.ships[row][col] = None

    def stepOn(game, row, col):
        if row == game.rows-1 and game.state is not 'won' and game.state is not 'lost':
            game.audio.playSound('laser.ogg')
            game.lasers.append([row-1,col,0])

    def stepOff(game, row, col):
        pass

def main():
    gameEngine = LSGameEngine(SpaceInvaders)
    gameEngine.beginLoop()

if __name__ == "__main__":
    main()
