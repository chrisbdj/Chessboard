import RPi.GPIO as GPIO
import time
import neopixel

from app_code.translation import convert_sensor_to_LED, convert_square_to_LED

class LED:
    def __init__(self, gpio, num_leds, brightness):
        self.gpio = gpio
        self.num_leds = num_leds
        self.brightness = brightness
        self.pixels = neopixel.NeoPixel(self.gpio, self.num_leds, pixel_order=neopixel.GRBW, brightness=self.brightness)




    def setAllLEDs(self, boardArr):
        a = len(boardArr) 
        j = 0
        #i is the sensor on the board 
        for i in range(a):
            #Light Board Based on occupied spaces
            led = convert_sensor_to_LED(i)
            if boardArr[i] == 0:
                #occupied space
                self.setLED(led, 0)
            else:
                #empty space
                self.setLED(led, 1)



    def setLED(self, led, state):
        if state == 0:  # square is occupied
            self.pixels[led] = (51, 51, 191)
        elif state == 1:  # square is empty
            self.pixels[led] = (255, 0, 102)
        elif state == 2:  # square is a possible move
            self.pixels[led] = (186, 235, 52)
        elif state == 3:  # square is a possible take
            self.pixels[led] = (255, 0, 0)
        elif state == 4:  # error color
            self.pixels[led] = (255, 165, 0)

    def setLEDbySensor(self, sensor, state):
        led = convert_sensor_to_LED(sensor)
        self.setLED(led, state)


    def setErrorLights(self):
        for i in range(self.num_leds):
            self.setLED(i, 4)
