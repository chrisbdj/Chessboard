import tkinter as tk
from tkinter import messagebox

class GUI:
    def __init__(self, master, on_start_game, on_end_game):
        # Callback function from main.py
        self.on_start_game = on_start_game
        self.on_end_game = on_end_game

        background_color = "#010101"

        self.master = master
        self.master.title("Smart Chess Board")
        

        # Create a Frame
        self.frame = tk.Frame(self.master)
        self.frame.pack()
        self.frame.place(relx=0.5, rely=0.5, anchor="c")

        # Set the background color to black
        self.master.configure(bg=background_color)
        self.frame.configure(bg=background_color)

        # Load an image
        self.image = tk.PhotoImage(file="img/chess.png")

        # Create a canvas and set its background color to transparent
        self.canvas = tk.Canvas(
            self.frame, width=self.image.width(), height=self.image.height(), bd=0, highlightthickness=0, bg=background_color
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Create a label with the image
        self.label = tk.Label(self.canvas, image=self.image, bg=background_color)
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.label_main = tk.Label(
            self.frame,
            text="Smart Chess Board!",
            font=("Helvetica", 16),
            foreground="#fff",  # Text color
            background=background_color,
            padx=10,
            pady=10,
        )
        self.label_main.grid(row=1, column=0, pady=10)

        # Create buttons
        self.insert_button("Single Player", self.single_player, row=2)
        self.insert_button("Multiplayer", self.multiplayer, row=3)

        # Set the initial size of the window to match the frame size
        self.master.geometry("500x500")




    def insert_button(self, text, action, row):
        hover_button = tk.Button(
            self.frame,
            text=text,
            command=action,
            bg="green",
            relief=tk.FLAT, 
            borderwidth=3,
            pady=10,
            padx=20
        )
        hover_button.grid(row=row, column=0, pady=10)  
        hover_button.bind("<Enter>", lambda event, btn=hover_button: self.on_enter(btn))
        hover_button.bind("<Leave>", lambda event, btn=hover_button: self.on_leave(btn))

    def on_enter(self, button):
        button.configure(bg="darkgreen")

    def on_leave(self, button):
        button.configure(bg="green")

    def single_player(self):
        self.start_game(1)

    def multiplayer(self):
        self.start_game(2)

    def start_game(self, game_type):
        if game_type == 1:
            print("Single Player Selected")
        elif game_type == 2:
            print("Multiplayer Selected")

        # Destroy existing widgets
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Create a back button
        self.insert_button("Back", self.main_menu, row=0)

        # Call the callback function from main.py
        if self.on_start_game:
            self.on_start_game(game_type)
            

    def main_menu(self):
        # Destroy existing widgets
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Call the callback function from main.py
        if self.on_end_game:
            self.on_end_game()

        # Recreate the main menu
        self.__init__(self.master, self.on_start_game, self.on_end_game)
