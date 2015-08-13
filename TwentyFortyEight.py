from lightsweeper.lsapi import *
import random

class TwentyFortyEight(LSGame):

    def init(game):  
        game.tiles = [(random.randint(0,game.rows-1), random.randint(0,game.cols-1), Colors.RED),(random.randint(0,game.rows-1), random.randint(0,game.cols-1), Colors.RED)]
        
        game.step_zone_width = 1
        
    def heartbeat(game, moves):
        for tile in game.tiles:
            game.display.set(tile[0], tile[1], Shapes.ZERO, tile[2])

    def stepOn(game, row, col):
        # check if we're shifting in a direction
        # eliminate the corners
        if row < game.step_zone_width:
            if col < game.step_zone_width or col >= game.cols - game.step_zone_width:
                print('corner {0},{1}'.format(row,col))
            else:
                game.shiftDirection('up')
        elif row >= game.rows - game.step_zone_width:
            if col < game.step_zone_width or col >= game.cols - game.step_zone_width:
                print('corner {0},{1}'.format(row,col))
            else:
                game.shiftDirection('down')
        elif col <= game.step_zone_width:
            game.shiftDirection('left')
        elif col >= game.cols - game.step_zone_width:
            game.shiftDirection('right')
        

    def shiftDirection(game,d):
    # the algorithm for shifting is as follows
    # # start with the row or column that is the furthest to the direction which we are moving,
    # # move all tiles 0 tiles in that direction, combining as appropriate. Do this iteratively
    # # for all tiles, moving one row or column further away from the row or column which we're
    # # moving everything towards.
        print('shift ' + d)
