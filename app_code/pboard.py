import RPi.GPIO as GPIO
import board
import time
import threading

from app_code.shifty import SN74LS165
from app_code.leds import LED
from app_code.util import arrays_equal, whats_the_dif
from app_code.translation import convert_to_square

class PhysicalBoard:
    def __init__(self, game_type, button_callback=None, board_callback=None):
        GPIO.setmode(GPIO.BCM)

        self.button_callback = button_callback  # Callback for button presses
        self.board_callback = board_callback      # Callback for board changes

        # Initialize LEDs and shift registers
        self.leds = LED(board.D18, 64, 0.5)
        self.shiftr = SN74LS165(clock=11, latch=7, data=9, clock_enable=8, num_chips=8)
        

        self.current_board = self.read_board()
        self.last_board = self.current_board[:]
        self.active_squares = []

        self.leds.setAllLEDs(self.current_board)

         # Set up the GPIO touch pins as inputs
        self.touch_pins = [27, 22, 23,17]
        self.bouncetime = 300

        # Initialize a state dictionary to track each button’s "pressed" state
        self.button_states = {pin: False for pin in self.touch_pins}

        for pin in self.touch_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    
    def run(self):
        while self.running:
           self.update_board()
           self.read_buttons()



    def update_board(self):
        self.current_board = self.read_board()
        if not arrays_equal(self.last_board, self.current_board):
            differences = whats_the_dif(self.last_board, self.current_board)
            if self.board_callback:
                self.board_callback(differences)
                print(self.current_board)
            for diff in differences:
                index = diff["index"]
                state = diff["state"]
                self.leds.setLEDbySensor(index, state)

            self.last_board = self.current_board[:]
        
        

    def read_board(self):
        return self.shiftr.read_shift_regs()

    def read_buttons(self):
        for i, pin in enumerate(self.touch_pins):
            if GPIO.input(pin) == GPIO.LOW and not self.button_states[pin]:
                # Button was just pressed
                self.button_states[pin] = True
                self.handle_buttons(i)

            elif GPIO.input(pin) == GPIO.HIGH and self.button_states[pin]:
                # Button was released
                self.button_states[pin] = False

    def handle_buttons(self, button):
        if button == 0:
            print("Black turn end button")
            self.board_at_turn_end = self.current_board[:]

        elif button == 1:
            print("White Hint Button!")

        elif button == 2:
            print("White turn end button")
            self.board_at_turn_end = self.current_board[:]
            
        elif button == 3:
            print("Black Hint Button!")
