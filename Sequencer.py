# the layout of the 8 x n sequencer floor:
# 0    0    0    0    0    0    0    0 (first 8 note set)
# 0    0    0    0    0    0    0    0 (second 8 note set)
# sound type selection

import time

from lightsweeper.lsapi import *

PREFIX = 'sequencer/'

class Sequencer():
    def __init__(self, display, audio, rows, cols):
        self.display = display
        self.display.setAll(Shapes.ZERO, Colors.BLUE)
        self.audio = audio
        self.audio.setDebug(False)
        self.rows = rows
        self.cols = cols
        self.ended = False
        self.handlesEvents = True
        self.audio.setSongVolume(0.1)
        self.board = None
        #which sounds will play on what tile / beat. Each beat is represented as a set
        #containing the index to the file for every sound that should be played
        if (self.rows - 1) % 2 == 0:
            self.beatRows = self.rows - 1
        elif self.rows - 1 > 1:
            self.beatRows = self.rows - 2
        else:
            self.beatRows = 1
        if self.cols >= 8:
            self.beatCols = 8
        elif self.cols >= 4:
            self.beatCols = 4
        elif self.cols >= 2:
            self.beatCols = 2
        else: # come on
            self.ended = True
        self.beats = [[set() for i in range(self.beatCols)] for i in range(self.beatRows)]
        self.files = ['cymbal/26895__vexst__semi-kick-2-2.wav',  'cymbal/26879__vexst__closed-hi-hat-1.wav', 'snare/26900__vexst__snare-1.wav', 'kick/41148__sandyrb__dnb-kick-001.wav', 'kick/26888__vexst__kick-4.wav', 'tap/437__tictacshutup__prac-sidestick-2.wav', 'misc/2074__twistedlemon__mattel-tom21.wav', 'misc/26878__vexst__bass-stab.wav']
        for sound in self.files:
            self.audio.loadSound(PREFIX + sound, PREFIX + sound)
        #which type of sound the player has currently selected
        self.selector = 0
        self.display.set(self.beatRows, 0, Shapes.ZERO, Colors.RED)
        #where the current beat is
        self.beatRow = 0
        self.beatCol = 0
        self.clock = -1
        self.msPerBeat = 60
        self.duration = 0
        self.frameRate = 120

        for col in range(len(self.beats[0])):
            self.display.set(self.beatRows, col, Shapes.DASH, Colors.GREEN)

    def heartbeat(self, sensorsChanged):
        if self.clock == -1:
            self.clock = time.time()
        if time.time() - self.clock > self.msPerBeat / 1000:
            print('{0}'.format(time.time() - self.clock), end='/r')
            self.clock = time.time()

            self.incrementCurrentTile()
            if self.beats[self.beatRow][self.beatCol]:
                #print(str(self.beatRow), str(self.beatCol), "playing", self.beats[self.beatRow][self.beatCol], "took", str(self.clock))
                for sound in self.beats[self.beatRow][self.beatCol]:
                    self.audio.playLoadedSound(PREFIX + self.files[sound])
                    if sound != self.selector:
                        self.display.set(self.beatRows, sound, Shapes.DASH, Colors.MAGENTA)
            

    def stepOn(self, row, col):
        if row < self.beatRows:
            # player stepped on a beat, add or remove the current sound
            if self.selector in self.beats[row][col]:
                self.beats[row][col].discard(self.selector)
                self.display.set(row, col, Shapes.ZERO, Colors.BLUE)
            else:
                self.beats[row][col].add(self.selector)
                self.display.set(row, col, Shapes.ZERO, Colors.YELLOW)
        else:
            #select a new sound
            self.display.set(row, self.selector, Shapes.DASH, Colors.GREEN)
            self.selector = col
            self.display.set(row, col, Shapes.DASH, Colors.RED)
            self.audio.playLoadedSound(PREFIX + self.files[self.selector])
            #show all beats where this sound will be played
            for r in range(len(self.beats)):
                for c in range(len(self.beats[0])):
                    if self.selector in self.beats[r][c]:
                        self.display.set(r, c, Shapes.ZERO, Colors.YELLOW)
                    else:
                        self.display.set(r, c, Shapes.ZERO, Colors.BLUE)

    def incrementCurrentTile(self):
        if self.selector in self.beats[self.beatRow][self.beatCol]:
            self.display.setColor(self.beatRow, self.beatCol, Colors.YELLOW)
        else:
            self.display.setColor(self.beatRow, self.beatCol, Colors.BLUE)
        self.beatCol += 1
        if self.beatCol >= self.beatCols:
            self.beatCol = 0
            self.beatRow += 1
        if self.beatRow >= self.beatRows:
            self.beatRow = 0
        self.display.setColor(self.beatRow, self.beatCol, Colors.WHITE)
        #reset colors of the sound selection row
        for c in range(len(self.beats[0])):
            if c != self.selector:
                self.display.set(self.beatRows, c, Shapes.DASH, Colors.GREEN)
            else:
                self.display.set(self.beatRows, c, Shapes.DASH, Colors.RED)

def main():
    gameEngine = LSGameEngine(Sequencer)
    gameEngine.beginLoop()

if __name__ == '__main__':
    main()
