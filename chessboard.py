from __future__ import print_function

import RPi.GPIO as GPIO
import time
import datetime
import neopixel
import board


pixels = neopixel.NeoPixel(board.D18, 64, pixel_order=neopixel.RGBW, brightness=0.8)
x=0

GPIO.setwarnings(False)

class SN74LS165:
    #pulse_time = .000005     # 5 microseconds
    pulse_time = .000015625

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
            
            if i < 64:
                if bit == 0:
                    pixels[i] = (220,0,0)
                else:
                    pixels[i] = (0,220,0)
                    
                    
            
            arr.append(bit)
            # Pulse the clock: rising edge shifts the next bit.
            GPIO.output(self.clock, GPIO.HIGH)
            time.sleep(SN74LS165.pulse_time)
            GPIO.output(self.clock, GPIO.LOW)
            time.sleep(SN74LS165.pulse_time)

        #return bytes_val
        return arr

if __name__ == '__main__':
    # Use GPIO numbering:
    GPIO.setmode(GPIO.BCM)

    shiftr = SN74LS165(clock=11, latch=7, data=9, clock_enable=8, num_chips=8)
    try:
        while True:
            bytes = shiftr.read_shift_regs()
            print(bytes)
            print("")
            time.sleep(0.01)
    except KeyboardInterrupt:
        GPIO.cleanup()


