#!/usr/bin/python3

'''
idea by Nate Anderson:
All of the segments would start cycling random colors once or twice a second. 
One digit would briefly switch to a solid color 1 with accompanying sound effect before returning to random cycling 
The user would select it and a confirmation action would occur with a sound effect.
Step 2 would repeat and an additional digit would be added to the sequence(a 2 displayed in a different color than the first)
Rinse and repeat until a user select the incorrect digit(not sure if it should go on indefinitely or if there should be a limit)
The entire board displays a failure animation with sound effects
'''

from lightsweeper.lsapi import *
import random
import time

# constants that keep track of how many frames each state takes
DISPLAY_DIGIT = 10
WAIT_FOR_INPUT = 50
RAINBOW_SHUFFLE = 40
TIMEOUT = 150
class RainbowMemory(LSGame):
    def init(self):
        self.frameRate = 15
        #start us off in the rainbow state
        self.frame = 0
        self.state = 'rainbow'
        self.stateInitialized = False
        self.displayingDigit = False
        self.currentDigit = 1
        self.currentColors = [Colors.RED, Colors.YELLOW, Colors.GREEN, Colors.CYAN, Colors.BLUE, Colors.MAGENTA]
        self.tile = (random.randint(0,2),
                     random.randint(0,self.display.cols-1))
        self.tileChain = [self.tile]
        self.steppedOnDigit = False
        self.lost = False
        self.audio.playSound('8bit/8bit-loop.wav', 0.35)
        self.beingPlayed = False

    def heartbeat(self, sensorsChanged):
        self.frame += 1

        if self.state is 'show digits':
            if not self.stateInitialized:
                self.audio.stopSounds()
                self.frame = DISPLAY_DIGIT
                self.stateInitialized = True
                self.currentDigit = 1
                if not self.beingPlayed:
                    self.tile = (random.randint(0,2),
                     random.randint(0,self.display.cols-1))
                    self.tileChain = [self.tile]
                print(self.state, self.currentDigit, len(self.tileChain))
            # display the next digit
            if self.currentDigit <= len(self.tileChain) and self.frame > DISPLAY_DIGIT:
                self.tile = self.tileChain[self.currentDigit - 1]
                self.audio.playSound('ding_1.wav')
                self.rainbowScreen()
                self.display.set(self.tile[0], self.tile[1], Shapes.digitToHex(self.currentDigit), (self.currentDigit % 6) + 1)
                self.currentDigit += 1
                self.frame = 0
            elif self.frame > DISPLAY_DIGIT:
                self.currentDigit = 1
                self.state = 'wait for input'
                self.stateInitialized = False
        elif self.state is 'wait for input':
            if not self.stateInitialized: 
                self.audio.stopSounds()
                self.audio.playSound('tick_tock.wav')
                self.rainbowScreen()
                self.frame = 0
                self.stateInitialized = True
            if self.frame > WAIT_FOR_INPUT:
                if not self.beingPlayed: # this is for when the game isn't being actively played
                    self.state = 'rainbow'
                    self.stateInitialized = False
                elif self.currentDigit > len(self.tileChain):
                    self.state = 'rainbow'
                    self.stateInitialized = False
                    prevTile = self.tileChain[-1]
                    self.tile = (random.randint(max(0,prevTile[0]-2),
                                  min(self.display.rows-1,prevTile[0]+2)),
                                 random.randint(max(0,prevTile[1]-2),
                                  min(self.display.cols-1,prevTile[1]+2)))
                    self.tileChain.append(self.tile)
            if self.frame == TIMEOUT: # this will only ever be reached when it's being played
                self.audio.playSound('tick_tock.wav')
            if self.frame > TIMEOUT + 30:
                self.state = 'lost'
                self.frame = 0
            if self.frame > DISPLAY_DIGIT:
                self.rainbowScreen()
            if self.currentDigit <= len(self.tileChain):
                self.tile = self.tileChain[self.currentDigit-1]
            
        elif self.state is 'rainbow':
            if not self.stateInitialized:
                self.audio.stopSounds()
                self.audio.playSound('8bit/8bit-loop.wav', 0.35)
                self.frame = 0
                self.stateInitialized = True
            if self.frame > RAINBOW_SHUFFLE:
                self.state = 'show digits'
                self.stateInitialized = False
            self.display.setAllCustom(self.currentColors + [Colors.BLACK])
            color = self.currentColors.pop()
            self.currentColors.insert(0, color)
        elif self.state is 'lost':
            if self.frame < 2:
                self.audio.playSound('game_over_noise.wav')
                self.display.setAll(Shapes.DASH, Colors.RED)

            if self.frame > 15:
                self.ended = True
        elif self.state is 'won':
            if self.frame < 2:
                self.audio.playSound('Success.wav')
            self.rainbowScreen(Shapes.digitToHex(self.frame % 10))
            if self.frame > 20:
                self.ended
        if self.currentDigit > 9 and self.state is 'wait for input':
                self.audio.stopSounds()
                self.state = 'won'
                self.frame = 0
    
    def rainbowScreen(self, shape=Shapes.DASH):
        for i in range(self.display.rows):
            self.display.setRow(i, shape, Colors.colorArrayInts[(i % 7) + 1])

    def stepOn(game, row, col):
        if game.state is not 'won' and game.state is not 'lost':
            game.audio.stopSounds()
        if game.state == 'wait for input':
            if (row,col) == game.tile:
                game.steppedOnDigit = True
                game.beingPlayed = True
                game.audio.playSound('8bit/42.wav')
                game.display.setAll(Shapes.DASH, Colors.GREEN)
                game.currentDigit += 1
                game.frame = 0
            else:
                game.audio.playSound('8bit/16.wav')
                game.display.setAll(Shapes.DASH, Colors.RED)
                game.state = 'lost'
                game.frame = 0
        else:
            print('Game state is "' + game.state + '", ignoring input')

    def stepOff(game, row, col):
        pass

def main():
    gameEngine = LSGameEngine(RainbowMemory)
    gameEngine.beginLoop()

if __name__ == "__main__":
    main()
