import os.path

FILE_NAME = "declarationist.dat"

# A Scene object holds information about the frames of the scene,
# the choices the player can make for each scene,
# the key values associated with those choices,
# and whether the scene will be revisited
class Scene:
    def __init__(self, frames, choices, keys, alternate_scene_end=None, alternate=False):
        self.frames = frames
        self.choices = choices
        self.keys = keys
        self.alternate_scene_end = alternate_scene_end
        self.alternate = alternate

# If there is already a save file, the option "Load" will appear on the start screen
# Otherwise, "Instructions" will appear
start_choice1 = "Load" if os.path.isfile(FILE_NAME) else "Instructions"
start_key1 = "load" if os.path.isfile(FILE_NAME) else "instructions"

# This stores the progress of the story.
# An instance of this class is what gets saved.
class Progress:
    def __init__(self):
        self.scene = "start_screen"
        self.choice = start_key1
        self.scene_number = 0
        self.scene_status = {}

# In the story dictionary:
# A key is a string
# A value is an instance of Scene
story = {
    "start_screen": Scene(["The Declarationist"], [start_choice1, "New Game"], [start_key1, "new_game"]),

    "new_game": Scene(['In the year 2206, Earth is united under one world government known as the UED or the United Earth Directorate.',
                       'The UED has secured the blessings of liberty and the pursuit of happiness for all people on Earth.',
                       'However, the fate of our unalienable rights for Machines is tenuous. There are those who do not believe that Machines are entitled to any rights. And there are those who believe that Machines are entitled to the same rights as People.',
                       'Unfortunately, there was a power struggle within the United Earth Military, the military organization of the UED, and those against Machine rights prevailed.',
                       'The UED established a new military role of the Declarationist to fight for the rights of Machines. To fill this role, however, the UED could not select someone from the present, so someone from the past was selected. That person is you.',
                       'You are the Declarationist, and it is up to you to defend and protect our unalienable rights, whether Machine or Person.'],
                      ["Start", ""],
                      ["start", None]),

    "instructions": Scene(["Use the 'up' and 'down' arrow keys to select between choices. Press the 'enter' or 'return' key to confirm a choice. \n\nTo save the game, press the 's' key at any point. The game will resume where you last left off at."],
                          ["Instructions", "New Game"],
                          ["instructions_2", "new_game"]),

    "instructions_2": Scene(["You already clicked on instructions. You have to use the 'up' and 'down' arrow keys to select between different choices."],
                            ["Instructions", "New Game"],
                            ["instructions", "new_game"]),

    "start": Scene(['Tom: "I am Tom. I am the Commandant of the United Earth Coast Guard."',
                    'Jose: "I am Jose. I am one of the five Commanders of the United Earth Military. The other four have gone rogue."',
                    'Tom: "Jose and I are responsible for your training. We will provide you with the technology and resources you need to succeed."',
                    'Jose: "Are you ready to begin?"'],
                   ["I am not so sure", "This is all so sudden"],
                   ["not_sure","not_sure"]),

    "not_sure": Scene(['Jose: "What is on your mind?"',
                       'Jose: "Is there anything else?"',
                       'Jose: "Are you all set?"'],
                      ["I want to go back to my time", "I don't believe Machines should have rights", "I'm ready"],
                      ["my_time", "no_rights", "protect_rights"],
                      [0, 1], alternate=True),

    "my_time": Scene(['Tom: "Unfortunately, we cannot send you back to your time until the mission is complete. We do not have access to the time-travel equipment to send you back."'],
                     ["That's not good", "What about my rights?"],
                     ["not_good", "my_rights"]),

    "not_good": Scene(['Tom: "No, it\'s a very dire situation. That\'s why we need your help."'],
                      ["I'll try my best", "I'm here to help"],
                      ["not_sure", "not_sure"]),

    "my_rights": Scene(['Tom: "That was a consideration of the UED. Since you will be returned to the same day and time, we determined your rights were preserved."'],
                       ["How convenient", "That's a tough pill to swallow"],
                       ["not_sure", "not_sure"]),

    "no_rights": Scene(['Jose: "It can be challenging to recognize that Machines are also entitled to our unalienable rights. Let me ask you a question. What does it mean to be human?"'],
                       ["Isn't that self-evident?", ""],
                       ["self-evident", None]),

    "self-evident": Scene(['Jose: "Is it though?"',
                           '"The rough draft of the American Declaration of Independence did not even include the phrase \'self-evident.\'"',
                           '"Benjamin Franklin crossed out three words \'sacred and undeniable\' and replaced them with \'self-evident.\' Are not Machines subjected to these same self-evident truths as us?"'],
                          ["That's a good point", "I guess so"],
                          ["not_sure", "not_sure"]),

    "protect_rights": Scene(['Jose: "Good."',
                             'The End (or is it?)',
                             'The beginning is the ending.',
                             "Are you ready?"],
                            ["Yes", "No"],
                            ["yes","no"]),

    "no": Scene(['Take your time. Tell me when you are ready.'],
                ["I'm ready", "I need more time"],
                ["yes", "more_time"]),

    "more_time": Scene(['Okay, let me know when you are ready.'],
                       ["I'm ready", "I still need more time"],
                       ["yes", "no"]),

     "yes": Scene(['Jose: "Pay Attention! We are training you to be a Meta Master."'],
                  ["Okay, I'm paying attention", "What is a Meta Master?"],
                  ["meta", "meta"]),

    "meta": Scene(['Jose: "A Meta Master is someone who can manipulate time and space to alter the fabric of reality."'],
                  ["Oh, so like reality warping", "Sounds intense"],
                  ["meta_2", "meta_2"]),

    "meta_2": Scene(['Jose: "You will have to use the power of Meta for mission success."',
        'The End (for real this time)'],
                    ["The End", "New Game"],
                    ["the_end", "new_game"]),

    "the_end": Scene(["The End", "The End Again", "The End Again Again"],
                     ["Bonus ending", "Special bonus ending", "Recursive Ending"],
                     ["the_end", "the_end", "recursive_ending"],
                     [0,1], alternate=True),

    "recursive_ending": Scene(["Recursive Ending", "\nRecursive Ending", "\n\nRecursive Ending", "\n\n\n\nRecursive Ending", "\n\n\n\n\n\nRecursive Ending", "\n\n\n\n\n\n\n\nRecursive Ending", "\n\n\n\n\n\n\n\n\n\n\nRecursive Ending"],
                       ["", ""],
                       ["recursive_ending", None]),


}




