import tkinter as tk
from app_code.gui import GUI
from app_code.game import Game  # Import the Game class

game_instance = None

def gooey():
    global root
    root = tk.Tk()
    gui = GUI(root, on_start_game, on_end_game)

    root.mainloop()


def on_start_game(game_type):
    global game_instance 
    print("Start game function called from main.py with game type:", "Single Player" if game_type == 1 else "Multiplayer")

    game_instance = Game(game_type)  # Pass game_type to the Game class
    game_instance.start()
    run_game()


def on_end_game():
    print("End game function called from main.py")

    if game_instance:
        game_instance.stop()
    root.after_cancel(game)


def run_game():
    if game_instance:
        game_instance.update()

    global game
    game = root.after(500, run_game)


if __name__ == "__main__":
    gooey()
