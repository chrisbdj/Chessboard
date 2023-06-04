from __future__ import print_function

import RPi.GPIO as GPIO
import time
import datetime
import math
import heapq
import neopixel
import board

GPIO.setwarnings(False)

class SN74LS165:
    pulse_time = .000005     # 5 microseconds
    def __init__(self, clock, latch, data, clock_enable, num_chips=1):
        self.latch = latch                 # AKA pload AKA PL, pin 1
        self.clock = clock                 # AKA CP, pin 2
        self.data = data                   # AKA Q7, pin 9
        self.clock_enable = clock_enable   # AKA CE, pin 15

        self.num_chips = num_chips
        self.datawidth = self.num_chips * 8

        GPIO.setup(self.latch, GPIO.OUT)
        GPIO.setup(self.clock, GPIO.OUT)
        GPIO.setup(self.data, GPIO.IN)
        GPIO.setup(self.clock_enable, GPIO.OUT)

    def read_shift_regs(self):
        # Trigger a parallel Load to latch the state of the data lines,
        GPIO.output(self.clock_enable, GPIO.HIGH)
        GPIO.output(self.latch, GPIO.LOW)
        time.sleep(SN74LS165.pulse_time)
        GPIO.output(self.latch, GPIO.HIGH)
        GPIO.output(self.clock_enable, GPIO.LOW)
        arr = []
        # Loop to read each bit value from the serial out line of the SN74HC165N.
        for i in range(self.datawidth):
            bit = GPIO.input(self.data)
            arr.append(bit)
            # Pulse the clock: rising edge shifts the next bit.
            GPIO.output(self.clock, GPIO.HIGH)
            time.sleep(SN74LS165.pulse_time)
            GPIO.output(self.clock, GPIO.LOW)
            time.sleep(SN74LS165.pulse_time)

        #return bytes_val
        return arr

gameState = False

def startNewGame():
    if not gameState:
        lightBoard()
        gameState=True



def arrays_equal(A, B):
    # If lengths of array are not equal means array are not equal
    if len(A) != len(B):
        return False
    
    #Simple test if all values ate the same
    if A == B:
        return True
    else: #they are not the same
        return False

def whats_the_dif(A, B):
    differences = []
    for i in range(len(A)):
        if A[i] != B[i]:
            differences.append(i)
            
    return differences


pixels = neopixel.NeoPixel(board.D18, 64, pixel_order=neopixel.GRBW, brightness=0.5)
x=0

def lightBoard(boardArr):
    a = len(boardArr) 
    j = 0
    #i is the sensor on the board 
    for i in range(a):
        #Light Board Based on occupied spaces
        if boardArr[i] == 0:
            #occupied space
            updateLED(i, 0)
        else:
            #empty space
            updateLED(i, 1)

        #Light Predicted Move


def convertSensorToLED(num):
    #LED ROWS ARE REVERSED EVERY OTHER ROW IN HARDWARE, THIS IS COMPENSATING FOR THAT
    row = (num-1)//8  #calculate row index
    column = (num -1) % 8 #calculate column index
    if row %2 ==1: #if the column is an odd number
        column = 7 - column #reverse the column order for hardware sync
    converted_num = row*8+column+1 #calculate it all back up to get the proper LED number
    return converted_num

def updateLED(led, state):
    led = convertSensorToLED(led)

    if state==0: #square is occupied
        pixels[led] = (51, 51, 191)
    elif state==1: #square is empty
        pixels[led] = (255, 0, 102)
    elif state==2: #square is a possible move
        pixels[led] = (0, 0, 255)
    elif state==3: #square is a possible take
        pixels[led] = (255, 0, 0)


#Take arr and make it 2d
def make2D(arr):
    return [arr[i:i+8] for i in range(0, len(arr), 8)]

preBoard = []
gameBoard = []


def updateBoard(boardArr, updatedBoardArr):
    differences = []
    differences = whats_the_dif(boardArr, updatedBoardArr)
    for i in range(len(differences)):
        updateLED(differences[i], updatedBoardArr[i])

    gameBoard = make2D(updatedBoardArr)



if __name__ == '__main__':
    #STARTGAME
    if not gameState:
        startNewGame()


    # Use GPIO numbering:
    GPIO.setmode(GPIO.BCM)
    #init game board shift registers
    shiftr = SN74LS165(clock=11, latch=7, data=9, clock_enable=8, num_chips=8)
    try:
        while True:
            #build initial array of game board
            shiftBoard = shiftr.read_shift_regs()
            #test if board has changed
            if not arrays_equal(preBoard, shiftBoard):
                updateBoard(preBoard, shiftBoard)

                #update array for initial change test
                preBoard = shiftBoard[:]
                

                
                print(preBoard)
                print("")

            time.sleep(0.05)
    except KeyboardInterrupt:
        GPIO.cleanup()


