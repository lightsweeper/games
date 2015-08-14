from lightsweeper.lsapi import *
import random

class TwentyFortyEight(LSGame):

    def init(game):
        game.tiles = [[None for i in range(game.cols)] for i in range(game.rows)]
        game.tiles[random.randint(0,game.rows-1)][random.randint(0,game.cols-1)] = 1
        game.tiles[random.randint(0,game.rows-1)][random.randint(0,game.cols-1)] = 1
        game.step_zone_width = 1
        
    def heartbeat(game, moves):
        for col in range(len(game.tiles[0])):
            for row in range(len(game.tiles)):
                if game.tiles[row][col] is not None:
                    if game.tiles[row][col] < 7:
                        game.display.set(row, col, Shapes.ZERO, Colors.colorArrayInts[game.tiles[row][col]])
                    elif game.tiles[row][col] < 13:
                        game.display.set(row,col, Shapes.ONE, Colors.colorArrayInts[game.tiles[row][col]] - 6)
                else:
                    game.display.set(row, col, Shapes.ZERO, Colors.BLACK)
        lost = True        
        for row in range(game.rows):
            for col in range(game.cols):
                if game.tiles[row][col] is None:
                    lost = False
                if game.tiles[row][col] == 7:
                    game.ended = True
        if lost:
            game.ended = True

    def stepOn(game, row, col):
        # check if we're shifting in a direction
        # eliminate the corners
        if row < game.step_zone_width:
            if col < game.step_zone_width or col >= game.cols - game.step_zone_width:
                print('corner {0},{1}'.format(row,col))
                return
            else:
                game.shiftDirection('up')
        elif row >= game.rows - game.step_zone_width:
            if col < game.step_zone_width or col >= game.cols - game.step_zone_width:
                print('corner {0},{1}'.format(row,col))
                return
            else:
                game.shiftDirection('down')
        elif col <= game.step_zone_width:
            game.shiftDirection('left')
        elif col >= game.cols - game.step_zone_width:
            game.shiftDirection('right')
        
        
        # add new tile
        newTile = (random.randint(0,game.rows-1),random.randint(0,game.cols-1))
        while game.tiles[newTile[0]][newTile[1]] is not None:
            newTile = (random.randint(0,game.rows-1),random.randint(0,game.cols-1))
        game.tiles[newTile[0]][newTile[1]] = 1
        
    def shiftDirection(game,d):
    # the algorithm for shifting is as follows
    # # start with the row or column that is the furthest to the direction which we are moving,
    # # move all tiles 0 tiles in that direction, combining as appropriate. Do this iteratively
    # # for all tiles, moving one row or column further away from the row or column which we're
    # # moving everything towards.
        print('shift ' + d)
        if d is 'up':
            for row in range(game.rows):
                for col in range(game.cols):
                    if game.tiles[row][col] is not None:
                        currRow = row - 1
                        while currRow >= 0 and game.tiles[currRow][col] is None:
                            game.tiles[currRow][col] = game.tiles[currRow+1][col]
                            game.tiles[currRow+1][col] = None
                            currRow -= 1
                        currRow += 1
                        if currRow > 0 and game.tiles[currRow][col] == game.tiles[currRow-1][col]:
                            game.tiles[currRow][col] = None
                            game.tiles[currRow-1][col] += 1
        if d is 'down':
            for row in range(game.rows-1, -1, -1):
                for col in range(game.cols):
                    if game.tiles[row][col] is not None:
                        currRow = row + 1
                        while currRow < game.rows and game.tiles[currRow][col] is None:
                            game.tiles[currRow][col] = game.tiles[currRow-1][col]
                            game.tiles[currRow-1][col] = None
                            currRow += 1
                        currRow -= 1
                        if currRow < game.rows-1 and game.tiles[currRow][col] == game.tiles[currRow-1][col]:
                            game.tiles[currRow][col] = None
                            game.tiles[currRow+1][col] += 1
        if d is 'left':
            for col in range(game.cols):
                for row in range(game.rows-1, -1, -1):
                    if game.tiles[row][col] is not None:
                        currCol = col - 1
                        while currCol >= 0 and game.tiles[row][currCol] is None:
                            game.tiles[row][currCol] = game.tiles[row][currCol+1]
                            game.tiles[row][currCol+1] = None
                            currCol -= 1
                        currCol += 1
                        if currCol > 0 and game.tiles[row][currCol] == game.tiles[row][currCol-1]:
                            game.tiles[row][currCol] = None
                            game.tiles[row][currCol-1] += 1
        if d is 'right':
            for col in range(game.cols-1, -1, -1):
                for row in range(game.rows):                
                    if game.tiles[row][col] is not None:
                        currCol = col + 1
                        while currCol < game.cols and game.tiles[row][currCol] is None:
                            game.tiles[row][currCol] = game.tiles[row][currCol-1]
                            game.tiles[row][currCol-1] = None
                            currCol += 1
                        currCol -= 1
                        if currCol < game.cols-1 and game.tiles[row][currCol] == game.tiles[row][currCol+1]:
                            game.tiles[row][currCol] = None
                            game.tiles[row][currCol+1] += 1
        for row in game.tiles:
            print(row)
