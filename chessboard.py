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

def arrays_equal(A, B):
    # If lengths of array are not equal means array are not equal
    if len(A) != len(B):
        return False

    # Creating 2 heaps for 2 arrays
    heap1 = list(A)
    heap2 = list(B)

    # Convert list into heap
    heapq.heapify(heap1)
    heapq.heapify(heap2)

    # Traverse and check if the top elements of both the
    # heaps are same or not
    while heap1:
        # If top elements are not same then return false
        if heapq.heappop(heap1) != heapq.heappop(heap2):
            return False

    # If all elements were same.
    return True



pixels = neopixel.NeoPixel(board.D18, 64, pixel_order=neopixel.GRBW, brightness=0.5)
x=0

def lightBoard(boardArr):
    a = len(boardArr) 
    j = 0
    #i is the sensor on the board 
    for i in range(a):
        #LED ROWS ARE REVERSED EVERY OTHER ROW IN HARDWARE, THIS IS COMPENSATING FOR THAT
        file=math.floor(i%8)
        if j % 2:
            file=7-math.floor(i%8)
        #led is the led which corresponds to i
        led=(j*8)+file
        if (i+1) % 8 == 0:
            j += 1
        #FINISH MATH FOR LED ROWS ARE REVERSED EVERY OTHER ROW IN HARDWARE

        #Light Board Based on occupied spaces
        if boardArr[i] == 0:
            #occupied space
            pixels[led] = (51, 51, 191)
        else:
            #empty space
            pixels[led] = (255, 0, 102)

        #Light Predicted Move




#Take arr and make it 2d
def make2D(arr):
    return [arr[i:i+8] for i in range(0, len(arr), 8)]

preBoard = []
gameBoard = []

if __name__ == '__main__':
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
                #update array for initial change test
                preBoard = shiftBoard[:]
                gameBoard = make2D(preBoard)

                lightBoard(preBoard)
                print(gameBoard)
                print("")

            time.sleep(0.05)
    except KeyboardInterrupt:
        GPIO.cleanup()


