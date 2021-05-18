"""
- Starts the game and displays the home screen
- Contains buttons to navigate to the tetris and minesweeper games
"""

import pygame
import os
import sys
from buttonClass import Button, Text, pygame_exit
from Minesweeper import minesweeper_main
from Tetris import tetris_main
from Typing_Test import typing_test_main


def main_func():
    # Sets the directory name back to python final project
    # This solves file not found errors if you start the code from one of the games rather than this main file
    if os.getcwd().split("\\")[-1] != "Python_Final_Project":
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(os.path.dirname(abspath))
        os.chdir(dname)

    # Starts the game and creates the window 
    display_width = 800
    display_height = 600
    gameDisplay = pygame.display.set_mode((display_width, display_height))

    # Defines welcome text
    title = Text("Welcome to Our Game!", (255, 255, 255), "comicsans", 100)

    # Defines the buttons to navigate to the tetris and minesweeper games
    button_width = display_width/3
    tetris_button = Button((50,50,225), display_width/4 - button_width/2, 250, button_width, 100, tetris_main.tetris_main_function,"Tetris", 0, None, 'comicsans', 60, (255,255,255), (40,40,150))
    minesweeper_button = Button((255,50,50), display_width/4 - button_width/2 + display_width/2, 250, button_width, 100, minesweeper_main.main,"Minesweeper", 0, None, 'comicsans', 60, (255,255,255), (150,40,40))
    typing_button = Button((255,193,69), display_width/2 - button_width/2, 400, button_width, 100, typing_test_main.main,"Typing Test", 0, None, 'comicsans', 60, (255,255,255), (128,95,35))
    button_list = [tetris_button, minesweeper_button, typing_button]

    # Game Loop
    gameExit = False
    while not gameExit:
        # Ends the game loop if the user tries to closes the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                break
            # Calls each buttons action function if they have been clicked
            elif pygame.mouse.get_pressed()[0]:
                for button in button_list:
                    if button.isOver((pygame.mouse.get_pos())):
                        button.action()
        
        # Draws background
        pygame.draw.rect(gameDisplay, (255,50,50), (pygame.Rect(0,0,display_width/2,display_height)))
        pygame.draw.rect(gameDisplay, (50,50,225), (pygame.Rect(display_width/2,0,display_width/2,display_height)))

        # Draws buttons
        for button in button_list:
            button.draw(gameDisplay)

        # Displays welcome text
        title.display_text(gameDisplay, display_width/2 - title.text.get_width()/2, 50)

        #updates the window
        pygame.display.update()

    # closes the window when the game loop ends
    pygame_exit()

if __name__ == "__main__":
    pygame.init()
    main_func()