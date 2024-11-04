
from app_code.pboard import PhysicalBoard
from app_code.util import arrays_equal, whats_the_dif

class Game:
    def __init__(self, game_type):
        self.is_running = False
        self.game_started = False
        self.game_board = []

        self.game_type = game_type  

        self.physical_board = PhysicalBoard(self.game_type, button_callback=self.on_button_press, board_callback=self.on_board_change)

    def start(self):
        self.is_running = True
        self.game_started = False
        self.game_board = []
        print("Game started in", "Single Player" if self.game_type == 1 else "Multiplayer", "mode!")

    def stop(self):
        self.is_running = False
        print("Game stopped!")

    def update(self):
        if self.is_running:
            #print("Game is updating in", "Single Player" if self.game_type == 1 else "Multiplayer", "mode")
            #if self.game_type == 2:
            if self.game_started == False:
                self.game_board = self.physical_board.current_board[:]
                if self.check_initial_setup(self.game_board):
                    print("Board Ready")
                else:
                    print("Pieces not set properly")




    def check_initial_setup(self, board):
        initial = [0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,1,1,1,1,0,0]
        if arrays_equal(initial, board):
            return True
        return False
        




    def on_board_change(self, differences):
        """Handle board update events."""
        print("Game received board update:", differences)
        # Implement logic based on the detected differences in the board state

    def on_button_press(self, button):
        """Handle button press events."""
        if button == 0:
            print("Game received Black turn end button")
            # Additional logic for ending Black's turn
        elif button == 1:
            print("Game received White Hint Button")
            # Additional logic for providing a hint to White
        elif button == 2:
            print("Game received White turn end button")
            # Additional logic for ending White's turn
        elif button == 3:
            print("Game received Black Hint Button")
            # Additional logic for providing a hint to Black





