from __future__ import print_function

import RPi.GPIO as GPIO
import time
import datetime
import math
import heapq
import neopixel
import board
import chess
import chess.engine


gameState = False
preBoard = []
piecesActivelyPickedUp = []

# Create a new chess board
gameBoard = chess.Board()


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



def startNewGame():
    #Light up the entire board
    lightBoard(preBoard)
    # Set up the board with a specific position
    gameBoard.set_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")


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

#Take arr and make it 2d
#def make2D(arr):
#    return [arr[i:i+8] for i in range(0, len(arr), 8)]



pixels = neopixel.NeoPixel(board.D18, 64, pixel_order=neopixel.GRBW, brightness=0.5)
x=0

def lightBoard(boardArr):
    a = len(boardArr) 
    j = 0
    #i is the sensor on the board 
    for i in range(a):
        #Light Board Based on occupied spaces
        led = convertSensorToLED(i)
        if boardArr[i] == 0:
            #occupied space
            updateLED(led, 0)
        else:
            #empty space
            updateLED(led, 1)

        #Light Predicted Move


def convertSensorToLED(num):
    #LED ROWS ARE REVERSED EVERY OTHER ROW IN HARDWARE, THIS IS COMPENSATING FOR THAT
    converted_num = num; #led might be same as sensor
    column = math.floor(num/8) #calculate column index
    XinColumn = num%8 #reduce where in the column the led will be
    if column%2==1: #detect if column is odd
       XinColumn = 7-XinColumn #reverse order if column is odd
       converted_num = (column*8)+XinColumn#recalculate the new LED number with column reversed
    return converted_num

def convertToCoordinate(num):
    rank = (num+1) % 8 #ranks and the horizontal rows which are numbered. 1-8 going up from white rook. 8 is now 0 in code.
    if rank==0: #8 reduced to lowest denominator is 0, which doesnt work for me or my board. Easy correction for that
        rank=8
    
    letter=["a","b","c","d","e","f","g","h"]
    file=math.floor(num/8) #file is the vertical columns which are lettered a-h going from white rook across naturally
    file=7-file
    result = letter[file]+str(rank)

    return result

def convertCoordToSensor(coord):
    #must be formatted letter number ex. d7
    try:
        letter=["a","b","c","d","e","f","g","h"]#alphabet for reference
        letterToFind = str(coord[0]) #isolate the letter at start of string
        idx = letter.index(letterToFind) #search for the isolated letter in the array
        rank = coord[1]
        idx = 7-idx
        sensor = ((idx*8)-1)+int(rank) #calculate the sensor number from the coordinate.

        return sensor
    except ValueError:
        return "letter cant be found"
    
def convertCoordToLED(coord):
    try:
        letter = ["a", "b", "c", "d", "e", "f", "g", "h"]  # alphabet for reference
        letter_to_find = coord[0]  # isolate the letter at the start of the string
        idx = letter.index(letter_to_find)  # search for the isolated letter in the array
        rank = int(coord[1]) #isolate the number in coordinate
        idx = 7 - idx #reverse index because the coordinate system is backwards from sensors.

        # LED ROWS ARE REVERSED EVERY OTHER ROW IN HARDWARE, THIS IS COMPENSATING FOR THAT
        led = idx * 8 + rank - 1  # calculate the LED number from the coordinate
        column = led // 8  # calculate column index
        XinColumn = led % 8  # reduce where in the column the LED will be
        if column % 2 == 1:  # detect if column is odd
            XinColumn = 7 - XinColumn  # reverse order if column is odd
        led = column * 8 + XinColumn  # recalculate the new LED number with column reversed

        return led
    except ValueError:
        return "Letter not found"


def split_string(string, length):
    return [string[i:i+length] for i in range(0, len(string), length)]


def get_possible_moves(coord):
    posi_moves = []
    piecePickedUp = chess.parse_square(coord) # Convert the square string to the square value
    legalMoves = gameBoard.legal_moves # Get the legal moves for the specific square
    moves_for_square = [move for move in legalMoves if move.from_square == piecePickedUp] # Filter legal moves for the specific square
    for move in moves_for_square: #iterate the moves array.
        move_str = move.uci()
        posi_moves.append(move_str)
    
    
    print("possible moves:", posi_moves)
    return posi_moves

def updateLED(led, state):

    if state==0: #square is occupied
        pixels[led] = (51, 51, 191)
    elif state==1: #square is empty
        pixels[led] = (255, 0, 102)
    elif state==2: #square is a possible move
        pixels[led] = 186, 235, 52
    elif state==3: #square is a possible take
        pixels[led] = (255, 0, 0)


current_move = []
def updateBoard(boardArr, updatedBoardArr):
    differences = []
    differences = whats_the_dif(boardArr, updatedBoardArr)
    for i in range(len(differences)):
        sensorThatisDifferent = differences[i]
        coord = convertToCoordinate(sensorThatisDifferent)

        print("Chess Coord of Manipulated Piece: ", coord, "state:",updatedBoardArr[sensorThatisDifferent])
        print("we converted the coord above back to the sensor: ", convertCoordToSensor(coord))
        possible_moves = []
        if updatedBoardArr[sensorThatisDifferent]== 1:
            #piece is picked up check moves
            possible_moves = get_possible_moves(coord)
            piecesActivelyPickedUp.append(coord)
            for move in possible_moves:
                led = split_string(move, 2)
                print("possible moves v2:", led[1])
                led = convertCoordToLED(led[1])
                updateLED(led,2)
                

        if updatedBoardArr[sensorThatisDifferent] == 0:
            #piece is put down
            if coord in piecesActivelyPickedUp:
                idx = piecesActivelyPickedUp.index(coord) #search for coord of piece put down in actively picked up
                piecesActivelyPickedUp.pop(idx)
                for move in possible_moves:
                    led = split_string(move, 2)
                    print("possible moves v2:", led[1])
                    led = convertCoordToLED(led[1])
                    updateLED(led,1)

            else:
                # Item not found in the list
                for pieces in piecesActivelyPickedUp:
                    possible_moves = get_possible_moves(pieces)
                    print(pieces+"picked up")
                    for move in possible_moves:
                        fen = pieces+coord
                        print("fen")
                        print(move)
                        if move == fen:
                            current_move.append(fen)
                            idx = piecesActivelyPickedUp.index(pieces) #search for coord of piece put down in actively picked up
                            piecesActivelyPickedUp.pop(idx)
                            print(current_move)
                
                
                
                print(coord," not found in actively raised pieces? maybe this is a take? ")
        
        updateLED(convertSensorToLED(sensorThatisDifferent), updatedBoardArr[sensorThatisDifferent])    


    #gameBoard = make2D(updatedBoardArr)



def handleButtons(button):
    if button == 0:
        #whites turn end button
        print("White turn End!")
        if gameBoard.turn:
            move = chess.Move.from_uci("e2e4")  # Example move: Pawn from e2 to e4
            gameBoard.push(move) # Push the move to the board

            piecesActivelyPickedUp = [] #clear pieces array if turn successful

    if button == 2:
        #blacks turn end button
        print("Black turn End!")
        if not gameBoard.turn:
            move = chess.Move.from_uci("e7e6")  # Example move: Pawn from e2 to e4
            gameBoard.push(move) # Push the move to the board

            piecesActivelyPickedUp = [] #clear pieces array if turn successful
    
    
    if button == 1:
        print("White Hint Button!")
       # engine = chess.engine.SimpleEngine.popen_uci("path/to/stockfish")

        # Assume 'board' is the current chess board object
        #result = engine.play(gameBoard, chess.engine.Limit(time=2.0))
        #suggested_move = result.move

        #print("Suggested move:", gameBoard.san(suggested_move))

        #engine.quit()
    
    if button == 3:
        print("Black Hint Button!")
        #engine = chess.engine.SimpleEngine.popen_uci("path/to/stockfish")

        # Assume 'board' is the current chess board object
        #result = engine.play(gameBoard, chess.engine.Limit(time=2.0))
        #suggested_move = result.move

        #print("Suggested move:", gameBoard.san(suggested_move))

        #engine.quit()



if __name__ == '__main__':
    # Use GPIO numbering:
    GPIO.setmode(GPIO.BCM)
    #init game board shift registers
    shiftr = SN74LS165(clock=11, latch=7, data=9, clock_enable=8, num_chips=8)
    # Set up the GPIO touch pins as inputs
    touch_pins = [17, 27, 22, 23]
    for pin in touch_pins:
        GPIO.setup(pin, GPIO.IN)

    preBoard = shiftr.read_shift_regs()
    #STARTGAME
    if gameState == False:
        startNewGame()
        gameState = True
        possible_moves = []
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

            # Read the touch inputs and perform actions based on pin state
            for i, pin in enumerate(touch_pins):
                if GPIO.input(pin) == GPIO.LOW:
                    handleButtons(i)
                    
            



            time.sleep(0.05)
    except KeyboardInterrupt:
        GPIO.cleanup()


