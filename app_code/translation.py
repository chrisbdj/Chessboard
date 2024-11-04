import math

def convert_sensor_to_LED(num):
    #LED ROWS ARE REVERSED EVERY OTHER ROW IN HARDWARE, THIS IS COMPENSATING FOR THAT
    converted_num = num; #led might be same as sensor
    column = math.floor(num/8) #calculate column index
    XinColumn = num%8 #reduce where in the column the led will be
    if column%2==1: #detect if column is odd
       XinColumn = 7-XinColumn #reverse order if column is odd
       converted_num = (column*8)+XinColumn#recalculate the new LED number with column reversed
    return converted_num





def convert_to_square(num):
    rank = (num+1) % 8 #ranks and the horizontal rows which are numbered. 1-8 going up from white rook. 8 is now 0 in code.
    if rank==0: #8 reduced to lowest denominator is 0, which doesnt work for me or my board. Easy correction for that
        rank=8
    
    letter=["a","b","c","d","e","f","g","h"]
    file=math.floor(num/8) #file is the vertical columns which are lettered a-h going from white rook across naturally
    file=7-file
    result = letter[file]+str(rank)

    return result






def convert_coord_to_sensor(coord):
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
    




def convert_square_to_LED(coord):
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


