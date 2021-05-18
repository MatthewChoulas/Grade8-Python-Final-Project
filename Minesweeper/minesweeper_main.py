import pygame
import sys 
import os
import time

def main():
    
    # Adds the current directory to the list of directories that the program uses to check for modules
    sys.path.append('.')
    sys.path.append('..')
    from project_main import main_func
    from buttonClass import Button,Text,pygame_exit
    from Minesweeper.minesweeper_engine import Grid

    # Sets the current working directory to the directory that the minesweeper_main.py file is in
    # This fixes some problems that occur when trying to load images
    if os.getcwd().split("\\")[-1] != "Minesweeper":
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath) 
        os.chdir(dname)


    # Retrieves the scoreboard data for each mode and saves the list of scores in a dictionary
    with open("user_data_easy.txt", "r") as data_easy, open("user_data_medium.txt", "r") as data_medium, open("user_data_hard.txt", "r") as data_hard:
        scores = {  "easy": list(map(lambda s: int(s.replace("\n","")), data_easy.readlines())),
                    "medium": list(map(lambda s: int(s.replace("\n","")), data_medium.readlines())),
                    "hard": list(map(lambda s: int(s.replace("\n","")), data_hard.readlines()))
                    }
        scores["easy"].sort()
        scores["medium"].sort()
        scores["hard"].sort()

    # Code for loading in sounds
    global music_on 
    music_on = True
    click_sound = pygame.mixer.Sound("./minesweeper_sound_effects/click.wav")
    flag_sound = pygame.mixer.Sound("./minesweeper_sound_effects/flag.wav")
    unflag_sound = pygame.mixer.Sound("./minesweeper_sound_effects/unflag.wav")
    bomb_sound = pygame.mixer.Sound("./minesweeper_sound_effects/ding.wav")
    lose_sound = pygame.mixer.Sound("./minesweeper_sound_effects/gameOver.wav")
    win_sound = pygame.mixer.Sound("./minesweeper_sound_effects/gameWin.wav")
    

    # Calculates the time since start of game and displays it and the timer icon on the screen
    def display_timer(time_passed=0):
        pygame.draw.rect(screen,background_color,(screen_height + 90, 36, timer_text.text.get_width(), timer_text.text.get_height()))
        screen.blit(timer_icon, (screen_height+15, 20))
        timer_text.update_text(str(int(time_passed)))
        timer_text.display_text(screen, screen_height + 90, 36)

    # Turns the music and sound effects on and off
    def toggle_music():
        global music_on
        if music_on:
            pygame.mixer.set_num_channels(0)
            pygame.mixer.music.stop()
            music_on = False
        else:
            pygame.mixer.set_num_channels(8)
            pygame.mixer.music.play()
            music_on = True

    # Draws the speaking image ontop of the button for toggling the music
    def display_speaker():
        global button_x
        if music_on:
            screen.blit(sound_icon, (button_x, 95))    
        else: 
            screen.blit(mute_icon, (button_x, 95))  
    
    # Displays the wining and losing messages to the screen
    def display_message():
        # Draws the message box
        message_box_dimensions = (screen_width*0.5, screen_height*0.4)
        message_box_position = (screen_width/2 - message_box_dimensions[0]/2, screen_height/2 - message_box_dimensions[1]/2)
        rectangle = pygame.Rect(message_box_position,message_box_dimensions)
        message_color = (51, 153, 255)
        pygame.draw.rect(screen, message_color, rectangle)

        # Defines the text if the play lost
        if grid.board_state == "lost":
            message_text = Text("You Lost", (255, 255, 255), "comicsans", 50)
            score_text = Text("0", (255, 255, 255), "comicsans", 50)
        # Defines the text if the play won
        elif grid.board_state == "won":
            message_text = Text("You Won", (255, 255, 255), "comicsans", 50)
            score_text = Text(timer_text.string, (255, 255, 255), "comicsans", 50)

        # Displays the previously defined text
        message_text.display_text(screen, message_box_position[0] + message_box_dimensions[0]/2 - message_text.text.get_width()/2, message_box_position[1] + message_box_dimensions[1]/4 - message_text.text.get_height()/2)

        # Draws the timer icon and score under the text in the message box
        screen.blit(timer_icon, (screen_width/2 - 32, screen_height/2 - 32))
        score_text.display_text(screen, message_box_position[0] + message_box_dimensions[0]/2 - score_text.text.get_width()/2, message_box_position[1] + message_box_dimensions[1]*3/4 - score_text.text.get_height()/2)

    
    # Defines the global mode variable which stores the current game mode
    global mode
    mode = "easy"

    # update mode is a decorator that adds the feature of updating the global mode variable to the set mode function
    # the reason I used a decorator instead of just adding a mode parameter to the set_mode function is because the button class only takes the name of a function to call but not what parameter to call with it.
    # this means that I can only use buttons with functions that don't have parameters so I used a decorator instead of changing the button class
    def update_mode(func, new_mode):
        def set_mode_modified():
            global mode
            mode = new_mode
            func()
        return set_mode_modified
    
    # Original set mode function that resets the grid, timer, and music
    def set_mode():
        global mode, grid, start_time
        grid = Grid(mode,screen_height)
        start_time = None
        pygame.mixer.music.stop()
        pygame.mixer.music.load("./minesweeper_sound_effects/gameMusic.mp3")
        if music_on:
            pygame.mixer.music.play(-1)

    # Functions for changing the mode to easy, medium, and hard
    set_mode_easy = update_mode(set_mode, "easy")
    set_mode_medium = update_mode(set_mode, "medium")
    set_mode_hard = update_mode(set_mode, "hard")

    # Defines the screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_color = (2, 1, 34)
    
    # Sets caption at top of window to "Minsweeper"
    pygame.display.set_caption('Minesweeper')
    
    # Defines the grid with a size of 10 by 10
    global grid
    grid = Grid("easy", screen_height)
    
    # Defines a variable to store the starting time of the game.
    global start_time
    start_time = None

    timer_text = Text("0", (255, 255, 255), "comicsans", 64)

    # Loads and resizes the timer icon
    timer_icon = pygame.image.load("minesweeper_image_assets/timer.png")

    # Loads the speaker images
    sound_icon = pygame.image.load("minesweeper_image_assets/volume.png")
    mute_icon = pygame.image.load("minesweeper_image_assets/mute.png")

    # Defines difficulty buttons, sound button, and menu button
    button_width =  0.8 * (screen_width - screen_height)
    button_height = 50
    global button_x
    button_x  = screen_height + 0.5 * (screen_width - screen_height - button_width)

    sound_button = Button(background_color,button_x, 95, 32, 32, toggle_music, "", 0, None, 'comicsans', 30, None, background_color)

    easy_button = Button((50,255,50),button_x, (button_height + 20) + 75, button_width, button_height, set_mode_easy, "EASY", 0, None, 'comicsans', 30, (255,255,255), (40,150,40))

    medium_button = Button((255,165,0),button_x, (button_height + 20)*2 + 75, button_width, button_height, set_mode_medium, "MEDIUM", 0, None, 'comicsans', 30, (255,255,255), (150,120,0))

    hard_button = Button((255,50,50),button_x, (button_height + 20)*3 + 75, button_width, button_height, set_mode_hard, "HARD", 0, None, 'comicsans', 30, (255,255,255), (150,40,40))

    menu_button = Button((50,50,255),button_x, screen_height-button_height-20, button_width, button_height, main_func, "MENU", 0, None, 'comicsans', 30, (255,255,255), (40,40,150))

    # defines the reset button
    reset_button_width = screen_width*0.5
    reset_button_height = screen_height*0.1
    reset_button_x = screen_width/2 - reset_button_width/2
    reset_button_y = screen_height/2 + screen_height*0.4/2 + reset_button_height
    
    # Uses a dictionary to get the set_mode method that corresponds to the current mode and assigns it to the reset button action attribute
    modes = {"easy": set_mode_easy,"medium": set_mode_medium ,"hard": set_mode_hard}
    reset_button = Button((0, 102, 0), reset_button_x, reset_button_y, reset_button_width, reset_button_height, modes[mode], "Try Again", font_color=(255,255,255), font_size=50)

    # Creates two list of buttons
    # Button list stores all the button that are displayed during the game
    # menu button list stores all the buttons displayed after the game is won/lost
    button_list = [sound_button, easy_button, medium_button, hard_button, menu_button]
    menu_button_list = [sound_button, reset_button, menu_button]
    

    # Plays game music
    pygame.mixer.music.load("./minesweeper_sound_effects/gameMusic.mp3")
    pygame.mixer.music.play(-1)
    


    # Game Loop
    running = True
    screen.fill(background_color)
    while running:
        if grid.board_state != "revealing_mines":
            pygame.draw.rect(screen,background_color,(screen_height, 0, screen_width - screen_height, screen_height))

        for event in pygame.event.get():
            # Ends the game loop if the user tries to close the window
            if event.type == pygame.QUIT:
                running = False
                break
            # Checks if mouse button was pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = grid.mouse_to_index(pygame.mouse.get_pos())
                # Checks if mouse is somewhere above the grid and the grid is in play
                if mouse_pos and grid.board_state == "in_play":
                    if start_time == None:
                        start_time = time.time()
                        if pygame.mouse.get_pressed()[0]:
                            if not grid.cells[mouse_pos[0]][mouse_pos[1]].marked:
                                # keeps regenerating the grid until the first uncovered square is not a mine and is not next to a mine and until the number of mines is at least 10 percent the number of cells
                                while (grid.cells[mouse_pos[0]][mouse_pos[1]].mine or grid.cells[mouse_pos[0]][mouse_pos[1]].mine_count != 0) or len(grid.mine_locations) < 0.1 * len(grid.cells) * len(grid.cells[0]):
                                    for row in grid.cells:
                                        for cell in row:
                                            cell.mine = grid.generate_mine_bool()
                                    for y in range(len(grid.cells)):
                                        for x in range(len(grid.cells[0])):
                                            grid.cells[y][x].mine_count = grid.cells[y][x].count_mines(grid.cells, (y,x))
                                    grid.mine_locations = [[row, col] for row in range(len(grid.cells)) for col in range(len(grid.cells[row])) if grid.cells[row][col].mine]

                    # Checks if the left mouse button was pressed
                    if pygame.mouse.get_pressed()[0]:
                        # Checks if the cells that the mouse is over is not marked and if so it makes that cell visible
                        if not grid.cells[mouse_pos[0]][mouse_pos[1]].marked and not grid.cells[mouse_pos[0]][mouse_pos[1]].visible:
                            click_sound.play()
                            grid.uncover_cell(mouse_pos[0], mouse_pos[1], screen)
                    # Checks if the right mouse button was pressed and if so it togles whether the cell is marked
                    if pygame.mouse.get_pressed()[2]:
                        if not grid.cells[mouse_pos[0]][mouse_pos[1]].marked:
                            flag_sound.play()
                        else:
                            unflag_sound.play()
                        grid.cells[mouse_pos[0]][mouse_pos[1]].marked = not grid.cells[mouse_pos[0]][mouse_pos[1]].marked
                # Checks if the left mous button was pressed off of the grid and checks if the user is clicking a button
                elif pygame.mouse.get_pressed()[0]: 
                    if grid.board_state == "lost" or grid.board_state == "won":
                        # Updates what mode the reset button sets the game to
                        reset_button.action = modes[mode]
                        #Checks if the mouse is clicking one of the menu button
                        for button in menu_button_list:
                            button.draw(screen)
                            if button.isOver((pygame.mouse.get_pos())):
                                pygame.mixer.music.stop()
                                button.action()
                    else:
                        # Checks if the mouse is clicking one of the button
                        for button in button_list:
                            if button.isOver((pygame.mouse.get_pos())):
                                pygame.mixer.music.stop()
                                button.action()
                        


        # stops the rest of the game loop if the running variable is false meaning exit button was pressed
        if not running:
            break
        

        # Draws the difficulty buttons if the game in play
        if grid.board_state != "lost" and grid.board_state != "won":
            for button in button_list:
                button.draw(screen)

        # draws the speaker image
        display_speaker()

        # Defines Scoreboard text object
        top_scores = ""
        for i in range(5):
            top_scores += str(i + 1) + ". "
            try:
                top_scores += str(scores[mode][i])
            except IndexError:
                pass
            top_scores += "\n"


        # Displays the scoreboard text on the screen
        # The text is enlarged on the menu screen
        if grid.board_state == "won" or grid.board_state == "lost":
            score_text = Text("SCORE\nBOARD\n\n" + top_scores, (255,255,255), "comicsans", 40)
            score_text.display_text(screen, button_x, 150)
        else:
            score_text = Text("SCORE BOARD\n\n" + top_scores, (255,255,255), "comicsans", 30)
            score_text.display_text(screen, button_x, (button_height + 20)*3 + 150)

        # Draws the grid
        if grid.board_state == "in_play":
            grid.draw(screen)

            # Displays the image and text for the timer
            if start_time:
                display_timer(time.time() - start_time)
            else:
                display_timer()

        # Reveals one mine at a time from the grid's list of mine locations
        elif grid.board_state == "revealing_mines" and len(grid.mine_locations) > 0:
            pygame.mixer.music.stop()
            bomb_sound.play()
            grid.uncover_cell(grid.mine_locations[0][0],  grid.mine_locations[0][1], screen)
            grid.mine_locations.pop(0)
        
        # Ends the game once all of the mines have been revealed
        elif grid.board_state == "revealing_mines" and len(grid.mine_locations) == 0:
            time.sleep(1)
            grid.board_state = "lost"
            screen.fill(background_color)
            lose_sound.play()
            time.sleep(3)
            pygame.mixer.music.load("./minesweeper_sound_effects/menuMusic.mp3")
            if music_on:
                pygame.mixer.music.play(-1)
        
        
        # Displays the won or lost message
        if grid.board_state == "lost" :
            display_message()
            reset_button.draw(screen)
            menu_button.draw(screen)
        elif grid.board_state == "won":
            display_message()
            reset_button.draw(screen)
            menu_button.draw(screen)


        # Updates screen
        pygame.display.update()


        # Checks if the game is won
        if grid.board_state == "in_play" and grid.win():
            # Updates the scoreboard data file with the players score
            with open("user_data_" + mode + ".txt", "a") as data:
                if scores[mode] == []:
                    data.write(timer_text.string)
                else:
                    data.write("\n" + timer_text.string)
                
                scores[mode].append(int(timer_text.string))
                scores[mode].sort()
            pygame.mixer.music.stop()
            time.sleep(1)
            grid.board_state = "won"
            screen.fill(background_color)
            win_sound.play()
            time.sleep(3)
            pygame.mixer.music.load("./minesweeper_sound_effects/menuMusic.mp3")
            if music_on:
                pygame.mixer.music.play(-1)
    
    # Closes the window when the game loop ends
    pygame_exit()


# calls the main function if the file is run from itself not imported as a module
if __name__ == "__main__":
    pygame.init()
    main()
