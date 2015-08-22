from lightsweeper.lsapi import *
import random

class TwentyFortyEight(LSGame):

    def init(game):
        # the edges are defined as the rows / columns that are outside of the 
        # game board, but border it
        game.lEdge = 0
        game.rEdge = game.cols-1
        game.uEdge = 0
        game.dEdge = game.rows-1
        
        # make a tile space for every tile, even those outside of the game board
        game.tiles = [[None for i in range(0, game.cols)] for i in range(0,game.rows)]
        game.tiles[random.randint(game.uEdge+1,game.dEdge-1)][random.randint(game.lEdge+1,game.rEdge-1)] = 1
        game.tiles[random.randint(game.uEdge+1,game.dEdge-1)][random.randint(game.lEdge+1,game.rEdge-1)] = 1
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
        
        game.display.setRow(game.uEdge, Shapes.SEG_A, Colors.WHITE)
        game.display.setRow(game.dEdge, Shapes.SEG_D, Colors.WHITE)
        
        game.display.setColumn(game.lEdge, Shapes.SEG_E, Colors.WHITE)
        game.display.setColumn(game.rEdge, Shapes.SEG_C, Colors.WHITE)
        
        lost = True
        for row in range(game.uEdge+1,game.dEdge):
            for col in range(game.lEdge+1,game.rEdge):
                if game.tiles[row][col] is None:
                    lost = False
                if game.tiles[row][col] == 7:
                    game.ended = True
        if lost:
            game.ended = True

    def stepOn(game, row, col):
        # check if we're shifting in a direction
        if col == game.lEdge:
            game.shiftDirection('left')
        elif col == game.rEdge:
            game.shiftDirection('right')
        elif row == game.uEdge:
            game.shiftDirection('up')
        elif row == game.dEdge:
            game.shiftDirection('down')

        # add new tile
        newTile = (random.randint(game.uEdge+1,game.dEdge-1),random.randint(game.lEdge+1,game.rEdge-1))
        while game.tiles[newTile[0]][newTile[1]] is not None:
            newTile = (random.randint(game.uEdge+1,game.dEdge-1),random.randint(game.lEdge+1,game.rEdge-1))
        game.tiles[newTile[0]][newTile[1]] = 1
        
    def shiftDirection(game,d):
    # the algorithm for shifting is as follows
    # # start with the row or column that is the furthest to the direction which we are moving,
    # # move all tiles 0 tiles in that direction, combining as appropriate. Do this iteratively
    # # for all tiles, moving one row or column further away from the row or column which we're
    # # moving everything towards.
        print('shift ' + d)
        game.audio.playSound('Blop.wav')
        if d is 'up':
            for row in range(game.uEdge+1,game.dEdge):
                for col in range(game.lEdge+1,game.rEdge):
                    if game.tiles[row][col] is not None:
                        currRow = row - 1
                        while currRow > game.uEdge and game.tiles[currRow][col] is None:
                            game.tiles[currRow][col] = game.tiles[currRow+1][col]
                            game.tiles[currRow+1][col] = None
                            currRow -= 1
                        currRow += 1
                        if currRow > game.uEdge and game.tiles[currRow][col] == game.tiles[currRow-1][col]:
                            game.tiles[currRow][col] = None
                            game.tiles[currRow-1][col] += 1
        if d is 'down':
            for row in range(game.dEdge-1, game.uEdge, -1):
                for col in range(game.lEdge+1,game.rEdge):
                    if game.tiles[row][col] is not None:
                        currRow = row + 1
                        while currRow < game.dEdge and game.tiles[currRow][col] is None:
                            game.tiles[currRow][col] = game.tiles[currRow-1][col]
                            game.tiles[currRow-1][col] = None
                            currRow += 1
                        currRow -= 1
                        if currRow < game.dEdge and game.tiles[currRow][col] == game.tiles[currRow+1][col]:
                            game.tiles[currRow][col] = None
                            game.tiles[currRow+1][col] += 1
        if d is 'left':
            for col in range(game.lEdge-1,game.rEdge):
                for row in range(game.dEdge-1, game.uEdge, -1):
                    if game.tiles[row][col] is not None:
                        currCol = col - 1
                        while currCol > game.lEdge and game.tiles[row][currCol] is None:
                            game.tiles[row][currCol] = game.tiles[row][currCol+1]
                            game.tiles[row][currCol+1] = None
                            currCol -= 1
                        currCol += 1
                        if currCol > game.lEdge and game.tiles[row][currCol] == game.tiles[row][currCol-1]:
                            game.tiles[row][currCol] = None
                            game.tiles[row][currCol-1] += 1
        if d is 'right':
            for col in range(game.rEdge-1, game.lEdge, -1):
                for row in range(game.uEdge+1,game.dEdge):                
                    if game.tiles[row][col] is not None:
                        currCol = col + 1
                        while currCol < game.rEdge and game.tiles[row][currCol] is None:
                            game.tiles[row][currCol] = game.tiles[row][currCol-1]
                            game.tiles[row][currCol-1] = None
                            currCol += 1
                        currCol -= 1
                        if currCol < game.rEdge and game.tiles[row][currCol] == game.tiles[row][currCol+1]:
                            game.tiles[row][currCol] = None
                            game.tiles[row][currCol+1] += 1
        #for row in game.tiles:
        #    print(row)





