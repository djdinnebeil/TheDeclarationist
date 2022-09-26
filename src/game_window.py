# A Python text adventure with a graphical user interface
# This program containers the main driver for the game

from tkinter import *
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
audio = False
try:
    import pygame
    audio = True
except:
    pass
from story import *     # imports class Progress and object story are imported
import pickle           # for saving the game

# The save file. Only one file is created per individual copy of the game
FILE_NAME = "declarationist.dat"

# Creates a progress object to keep track of the player's progress
progress = Progress()

# The color and font theme
background_color = "navy"
selected_text_color = "sea green"
text_color = "white"
selected_text_font = "Arial 25 underline"
text_font = "Arial 25"

# A class for the game engine
# Create an instance of this class and
# call the "run" function to run the game
class GameWindow:
    def __init__(self):

        # Set up the window
        self.window = Tk(className=" The Declarationist")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        self.window.configure(bg=background_color)

        # Create a frame to display the story
        self.storyFrame = Frame(self.window)

        # Create the start screen
        self.story = Message(self.storyFrame, text=story[progress.scene].frames[0], justify="center",
                             width=700, fg=text_color, bg=background_color, font=text_font)
        self.choice1 = Message(self.window, text=story[progress.scene].choices[0], fg=selected_text_color,
                               bg=background_color, justify="center", font=selected_text_font, width=700)
        self.choice2 = Message(self.window, text=story[progress.scene].choices[1], fg=text_color,
                               bg=background_color, font=text_font, width=700)

        # Setup the layout
        self.storyFrame.grid(row=0)
        self.story.pack()
        self.choice1.grid(row=2)
        self.choice2.grid(row=3)
        self.window.grid_rowconfigure(0, weight=6)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_rowconfigure(4, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # Create a blank object to balance the layout
        self.blank = Message(self.window, text="", bg=background_color)
        self.blank.grid(row=4)

        if audio:
            self.play_audio()

        # Setup the keyboard
        self.window.bind("<Up>", self.change_color_up)
        self.window.bind("<Down>", self.change_color_down)
        self.window.bind("<Return>", self.confirm)
        self.window.bind("s", self.save_game)

    # Runs the game
    def run(self):
        self.window.mainloop()

    # If the user presses 'enter' or 'return,' this function is called
    # This function confirms a choice or acknowledges text
    def confirm(self, event):


        # Checks if the scene has alternate options
        alternate_options = (progress.scene in progress.scene_status)

        # If the player selects load, a game loads
        # This option is only available if there is a saved game
        if progress.choice == "load":
            self.load_game()

            # The last scene the player was at is displayed
            self.display_scene()
        elif progress.choice == "new_game":
            progress.scene_status = {}
            self.display_next_scene()


        # If the current scene has alternate choices, this updates the progress object to reflect
        # which choice was made and then displays the next scene
        elif progress.choice and alternate_options:

            # If choice one was selected, set a boolean for that stored in the dictionary scene_status
            if (self.selected_choice == 1):
                progress.scene_status[progress.scene]["selected_choice1"] = True

            # If choice two was selected, set a boolean for that stored in the dictionary scene_status
            elif (self.selected_choice == 2):
                progress.scene_status[progress.scene]["selected_choice2"] = True

            # If this scene is revisited, the story starts at the next frame within the scene
            progress.scene_status[progress.scene]["scene_number"] = progress.scene_number + 1

            # Displasy the next scene
            self.display_next_scene()

        # If a choice is selected, this displays the next scene
        elif progress.choice:
            self.display_next_scene()

        # If the scene number is equal to the alternate scene end number for a particular visit,
        # display the choices. The first choice is selected by default
        elif alternate_options \
                and (progress.scene_number ==
                     story[progress.scene].alternate_scene_end[progress.scene_status[progress.scene]["visit_number"]]):

            # If this is the first visit of a scene, then display both choices
            if progress.scene_status[progress.scene]["visit_number"] == 0:
                self.display_choices(0, 1, True)

            # If both choices were previously selected, then display only the alternate choice
            elif progress.scene_status[progress.scene]["selected_choice1"] \
                    and progress.scene_status[progress.scene]["selected_choice2"]:
                self.display_choices(2, -1)

            # If the first choice was previously selected, then display the second choice first
            # and the alternate choice third
            elif progress.scene_status[progress.scene]["selected_choice1"]:
                self.display_choices(1, 2, True)

            # If the second choice was previously selected, then display the first choice
            # and alternate choice
            elif progress.scene_status[progress.scene]["selected_choice2"]:
                self.display_choices(0, 2, True)

            # Displays that the first choice is selected
            self.highlight_first_choice()

        # If the scene number is at the last frame, then display the choices
        # The first choice is selected by default
        elif (progress.scene_number == len(story[progress.scene].frames) - 1):
            self.display_choices(0, 1)
            # Displays that the first choice is selected
            self.highlight_first_choice()

        # If the last frame has not been reached, then display the next frame
        else:
            progress.scene_number += 1
            self.story.configure(text=story[progress.scene].frames[progress.scene_number])


    # Displays the choices
    def display_choices(self, first_choice, second_choice, selected_choice=False):
        self.choice1.configure(text=story[progress.scene].choices[first_choice])
        if (second_choice == -1):
            self.choice2.configure(text="")
        else:
            self.choice2.configure(text=story[progress.scene].choices[second_choice])

        progress.choice = story[progress.scene].keys[first_choice]
        if (selected_choice):
            self.selected_choice = first_choice + 1

    # Selects a choice
    def select_choice(self, key, selected_choice=False):
        progress.choice = story[progress.scene].keys[key]
        if (selected_choice):
            self.selected_choice = key + 1

    # Changes the color of the text if the up arrow is pressed
    def change_color_up(self, event):
        if progress.choice and  (progress.scene in progress.scene_status) and (progress.scene_status[progress.scene]["visit_number"] == 0):
            self.select_choice(0, True)
        elif progress.choice and (progress.scene in progress.scene_status) and (progress.scene_status[progress.scene]["selected_choice1"] and progress.scene_status[progress.scene]["selected_choice2"]):
            self.select_choice(2)
        elif progress.choice and (progress.scene in progress.scene_status) and progress.scene_status[progress.scene]["selected_choice1"]:
            self.select_choice(1, True)
        elif progress.choice:
            self.select_choice(0, True)
        self.highlight_first_choice()

    # Changes the color of the text if the down arrow is pressed
    def change_color_down(self, event):
        if progress.choice and (progress.scene in progress.scene_status) and (progress.scene_status[progress.scene]["visit_number"] == 0):
            self.select_choice(1, True)
        elif progress.choice and (progress.scene in progress.scene_status) and (progress.scene_status[progress.scene]["selected_choice1"] and progress.scene_status[progress.scene]["selected_choice2"]):
            pass
        elif progress.choice and (progress.scene in progress.scene_status) and progress.scene_status[progress.scene]["selected_choice1"]:
            self.select_choice(2)
        elif progress.choice and (progress.scene in progress.scene_status) and progress.scene_status[progress.scene]["selected_choice2"]:
            self.select_choice(2)
        elif progress.choice and story[progress.scene].keys[1]:
            self.select_choice(1, True)
        self.highlight_second_choice()

    # Changes the color of the first choice
    def highlight_first_choice(self):
        self.choice1.config(fg=selected_text_color, font=selected_text_font)
        self.choice2.config(fg=text_color, font=text_font)

    # Changes the color of the second choice
    def highlight_second_choice(self):
        self.choice1.config(fg=text_color, font=text_font)
        self.choice2.config(fg=selected_text_color, font=selected_text_font)

    # Saves the game
    def save_game(self, event):
        try:
            output_file = open(FILE_NAME, "wb")
            pickle.dump(progress, output_file)
            output_file.close()
            self.story.configure(text="Saved")
            self.window.after(1000, self.save_confirmation)
        except:
            self.story.configure(text="Error: game did not save")
            self.window.after(3000, self.save_confirmation)

    # Loads the game
    def load_game(self):
        try:
            input_file = open(FILE_NAME, "rb")
            global progress
            progress = pickle.load(input_file)
            input_file.close()
        except:
            pass

    # Returns the screen back to the story after a save confirmation displays
    # (or error message if file did not save)
    def save_confirmation(self):
        self.story.configure(text=story[progress.scene].frames[progress.scene_number])

    # Displays the next scene
    def display_next_scene(self):
        progress.scene = progress.choice
        # If the scene has already been visited
        if (progress.scene in progress.scene_status):
            progress.scene_number = progress.scene_status[progress.scene]["scene_number"]
            progress.scene_status[progress.scene]["visit_number"] += 1
            if (progress.scene_status[progress.scene]["visit_number"] >= 2):
                story[progress.scene].alternate_scene_end.append(len(story[progress.scene].frames) - 1)
        # If the scene has not been visited and has an alternate branch
        elif story[progress.scene].alternate:
            progress.scene_status[progress.scene] = {"visit_number": 0,
                                                     "selected_choice1": False,
                                                     "selected_choice2": False, }
            progress.scene_number = 0
        else:
            progress.scene_number = 0
        self.display_scene()

    # Displays the scene
    def display_scene(self):
        self.choice1.configure(text="")
        self.choice2.configure(text="")
        progress.choice = None
        self.story.configure(text=story[progress.scene].frames[progress.scene_number])

    def play_audio(self):
        pygame.init()
        global audio
        try:
            pygame.mixer.music.load("music/theme.mp3")
            pygame.mixer.music.play()
            audio = False
        except:
            audio = False



# Runs the game
GameWindow().run()