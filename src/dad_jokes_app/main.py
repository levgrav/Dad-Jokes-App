"""
main.py
~~~~~~~
Displays a simple application that cycles through dad-jokes
Author: Levi Eby
Date Created: 4/4/2023
"""


# --- Imports --- #
import json
import os
import random
from textwrap import fill
from PySimpleGUI import (
    Text, Button, Image,
    Column, Window, theme,
    WIN_CLOSED)


# --- Setup --- #
joke = ""
done_jokes = [joke] # stores all jokes that have already been displayed
layouts_file_path = "data/layouts.json"
SW, SH = Window.get_screen_size() # stores the size of the screen for making it fullscreen


# --- Initialization --- #
window = Window("") # Creates a window with a blank title and no layout


# --- Functions --- #          
def data_to_layout(x):
    """Recursive function that transforms data into their respective PySimpleGUI class instances while keeping it in the same format. That is why Text, Button, Image,
    Column are imported from PySimpleGUI


    Args:
        x (dict, list, tuple): represents the data being transformed into PySimpleGUI objects


    Returns:
        Text, Button, Image, Column, list, tuple: the PySimpleGUI object that was represented by a dict or a list of such objects.
    """
   
    if isinstance(x, (list, tuple)):
        # in the case of a list or a tuple, the function calls itself on its elements
        for i, e in enumerate(x):
            x[i] = data_to_layout(e) # type: ignore
           
    elif isinstance(x, dict):
        # in the case of a dictionary, x represents an object.
        attrs = {} # creates a blank dictionary to store all the attributes of the object that will be created
        Class_Type = globals()[x["instanceof"]] # will set Class_Type to Text, Button, Image, or Column
        for kw, arg in x['attrs'].items():
            attrs[kw] = data_to_layout(arg) # calls itself on all the attributes that the class will take
           
        x = Class_Type(**attrs) # maps attributes to specified PySimpleGUI object
   
    # if x was just a string, int, etc., x is just returned. Otherwise, the transformed x is returned.
    return x


def layout_from_json(layout_name: str):
    """Finds a layout in the layout JSON file and returns it as a 2D list of PySimpleGUI objects


    Args:
        layout_name (str): which layout of the available layouts in the layouts JSON file to use


    Returns:
        list: layout that is interpreted by PySimpleGui to determine what the window looks like
    """
    # load the JSON into a dict
    with open(layouts_file_path, "r") as l:
        layouts_dict = json.load(l)
   
    # find the specified layout in the dictionary of layouts
    for _layout_name, layout_data in layouts_dict.items():
        if layout_name == _layout_name:
            return data_to_layout(layout_data) # transforms the layout_data into list that contains PySimlpleGUI objects
   
    return [] # if there is no match, return an empty layout list
   
def set_layout(layout: str):
    """Changes the global variable window to have a the layout that matches the given string


    Args:
        layout (str): controls which segment of JSON is used as the layout
    """
    global window # sets the scope of the variable "window" to global, so that we can access the predefined variable.
    window = Window(title = layout, layout = layout_from_json(layout), size=(SW, SH), no_titlebar=True) # creates a window


def main():
    """Main function. Contains some setup and the main game loop."""
    global joke
   
    # get the jokes from the jokes file. Credits for the jokes file: Arya Shah, Dad-A-Base Of Jokes, Kaggle.
    with open("data/dad-a-base.csv") as f:
        jokes = f.readlines()
       
   
    # default theme works well with the image, and this theme will not nag me to change it to be something more exciting
    theme('DefaultNoMoreNagging')
   
    # start the window on the Main Menu
    set_layout("Main Menu")
   
    # --- Game Loop --- #
    while True:
        event, values = window.read()  # type: ignore
       
        if event == "Joke Page": # if the "Start" button is clicked on the main menu, it brings you to the joke page. Event is joke page because in the layout, "key" is set to "Joke Page"
            set_layout(event)
       
        elif event == 'Quit' or event == WIN_CLOSED:
            # Leave duh game - obamna
            break
       
        elif event == "Next Joke": # the joke cycle button
           
            # picks a joke that is not in `done_jokes`. This keeps the jokes from repeating
            while joke in done_jokes:
                joke = random.choice(jokes)
            done_jokes.append(joke) # adds the joke to `done jokes`
           
            # sets the joke text to `joke`
            window['-JOKE-'].update(fill(joke, 40)) # type: ignore
           
    # Close the window
    window.close()

# if this is the file being run, run the main function.
if __name__ == "__main__":
    main()