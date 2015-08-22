'''
Travel with Captain Starface as she explores the galaxy to explode the crap out of her enemies.

Step on a square next to Captain Starface's ship to move the ship to that square, or step on the square to shoot forward. Enemies are pink--get a friend to hold an enemy ship down while you help Starface destroy it! Can you get to a higher level than your friends?

'''

from lightsweeper.lsapi import *

class CaptainStarface():
    def init(game):
        pass

    def heartbeat(game, activeSensors):
        pass

    def stepOn(game, row, col):
        pass

    def stepOff(game, row, col):
        pass

def main():
    gameEngine = LSGameEngine(CaptainStarface)
    gameEngine.beginLoop()

if __name__ == "__main__":
    main()

