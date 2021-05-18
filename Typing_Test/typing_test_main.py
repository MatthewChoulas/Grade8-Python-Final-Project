import pygame
import sys 
import os
import time
import random
import time


def main():
    # Adds the current directory to the list of directories that the program uses to check for modules
    sys.path.append('.')
    sys.path.append('..')
    from project_main import main_func
    from buttonClass import Button,Text,pygame_exit
    from Typing_Test.typing_test_engine import Word, Display_Text, Text_Box

    # Sets the current working directory to the directory that the minesweeper_main.py file is in
    # This fixes some problems that occur when trying to load images
    if os.getcwd().split("\\")[-1] != "Typing_Test ":
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath) 
        os.chdir(dname)
        
    # updates the color of the overlay on the current word by checking to see if what the user typed could possibly match the current word
    def update_word_overlay():
        if text_box.word_match(text_display):
            text_display.current_word.overlay = Word.GRAY
        else:
            text_display.current_word.overlay = Word.RED


    # Defines the screen
    global screen, screen_width, screen_height
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_color = (135, 206, 235)
    
    # Sets caption at top of window to "Typing Test"
    pygame.display.set_caption('Typing Test')

    # Defines header
    header = Text("Typing Test", (255, 255, 255), "comicsans", 75)

    # Defines the menu button
    button_width =  0.8 * (screen_width - screen_height)
    button_height = 50
    menu_button = Button((50,50,255), screen_width - button_width - 20, screen_height-button_height-20, button_width, button_height, main_func, "MENU", 0, None, 'comicsans', 30, (255,255,255), (40,40,150))
    stats_button = Button((	255, 191, 0), screen_width - button_width - 20, 20, button_width, button_height, stats_page, "STATS", 0, None, 'comicsans', 30, (255,255,255), (191,143,0))
    button_list = [menu_button, stats_button]

    global game_state, game_start_time, game_time_passed, game_time_left, text_display, text_box, timer_text, wpm_text
    # Defines the text display and textbox for displaying text to the user and for the user to enter text
    text_display = Display_Text(600, 120, "comicsans", 40, (255,255,255), (25,25,25), 2, 15, 10, 5)
    text_box =  Text_Box((200, 300), 400, 48, "comicsans", 40, (255,255,255), (0,0,0), (255,255,0), 2, 10)
    text_box_background_rect = pygame.Rect(100, 290, 600, 68)

    # Timer setup code
    timer_background_rect = pygame.Rect(110, 300, 80, 48)
    timer_text = Text("1:00", (255,255,255), "comicsans", 50)
    game_state = "not_started"
    game_start_time = None
    game_time_passed = 0
    game_time_left = 60
    wpm_text = Text("0 WPM", (255,255,255), "comicsans", 80)

    scores_text = Text("", (255,255,255), "comicsans", 40)


    def reset_game():
        global game_state, game_start_time, game_time_passed, game_time_left, text_display, text_box, timer_text, wpm_text
        game_state = "not_started"
        game_start_time = None
        game_time_passed = 0
        game_time_left = 60

        text_display = Display_Text(600, 120, "comicsans", 40, (255,255,255), (25,25,25), 2, 15, 10, 5)
        text_box =  Text_Box((200, 300), 400, 48, "comicsans", 40, (255,255,255), (0,0,0), (255,255,0), 2, 10)

        timer_text = Text("1:00", (255,255,255), "comicsans", 50)
        wpm_text = Text("0 WPM", (255,255,255), "comicsans", 80)
        scores_text = Text("", (255,255,255), "comicsans", 40)




    # Define reset button
    reset_button = Button((31, 109, 204), 625, 300, 48, 48, reset_game, hover_color=(51, 91, 156))
    button_list.append(reset_button)
    reset_icon = pygame.image.load("typing_test_image_assets/reload.png")

    # saves the games start time
    # Used to calculate wpm
    start_time = time.time()
    # Game loop
    running = True
    while running:
        # Updates the current time
        current_time = time.time() - start_time

        # Clears the screen
        screen.fill(background_color)

        # Starts looping through all events
        for event in pygame.event.get():
            # Checks if the game was closed
            if event.type == pygame.QUIT:
                running = False
                break
            
            # Checks if the mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if the left mouse button was clicked
                if pygame.mouse.get_pressed()[0]:
                    # Iterates through all of the buttons and checks if they were clicked
                    for button in button_list:
                        # Checks if the button was clicke and if so it calls the buttons action function
                        if button.isOver((pygame.mouse.get_pos())):
                            button.action()
                    # Tells the program that the text_box was selected if the click was over the text box
                    # Otherwise it deselects the text box
                    text_box.is_selected = text_box.click_in_box((pygame.mouse.get_pos()))
                    
            # Checks if a key was pressed own
            if event.type == pygame.KEYDOWN and game_state != "game over":
                # Checks if the text box was selected
                # Key board input only matters when the text box is selected so othwise the program does nothing      
                if text_box.is_selected:
                    # Starts the game if any key is pressed
                    if game_state == "not_started":
                        game_state = "started"
                        game_start_time = time.time()
                    # Checks if the backspace key was pressed and if so it deletes the last character typed
                    if event.key == pygame.K_BACKSPACE:
                        text_box.text = text_box.text[:-1]
                    # Checks if the space key was pressed and if so it enters the word which includes logging the word, updating the current word, and clearing the text box
                    elif event.key == pygame.K_SPACE:
                        text_box.log_word(text_display)
                        text_display.next_word(text_display.current_word.string == text_box.text)
                        text_box.clear_text()
                    # Adds the key pressed to text box as long as it is one character long and is not the return key
                    # Prints the wpm for debugging(making sure the program is working correctly) purposes
                    elif len(event.unicode) == 1 and event.key != pygame.K_RETURN:
                        text_box.text += event.unicode
                        text_box.log_stroke(text_display) 
        # Animates the flashing cursor if the text box is selected but is empty
        if text_box.text == "":
            current_time = time.time() - start_time
            # Uses the current time to make the cursor invisible if time's tenths digit is greater than 0.25
            if abs(round(current_time, 1) - round(current_time)) > 0.25:
                text_box.cursor_color = text_box.background_color
            # Otherwise the cursor is black
            else:
                text_box.cursor_color = (0,0,0)
        else:
            # Sets the cursor color back to black incase the textbox becomes not empty while the cursor color is set to white
            text_box.cursor_color = (0,0,0)

        #Stops the game from updating or checking any other conditions if the window is quit
        if not running:
            break

        # Draws header
        header.display_text(screen, screen_width/2 - header.text.get_width()/2, 50)

        # Updates the word overlay color in the text display
        update_word_overlay()

        # Display text
        text_display.display_text_display(screen, (100,150))

        # Display textbox
        pygame.draw.rect(screen, (118, 160, 245), text_box_background_rect)
        text_box.display_text_box(screen)
        # Display timer
        pygame.draw.rect(screen, (38, 54, 94), timer_background_rect)
        if game_state == "started":
            time.sleep(0.0000000001)
            game_time_passed = time.time() - game_start_time
            game_time_left = 60 - game_time_passed
            if game_time_left <= 0:
                with open('user_typing_data.txt', 'a') as data:
                    data.write(
                            str(round(text_box.calc_wpm(game_time_passed))) + " " +
                            str(strokes) + " " +
                            str(correct_strokes) + " " +
                            str(wrong_strokes) + " " +
                            str(accuracy) + " " +
                            str(correct_words) + " " +
                            str(wrong_words) + "\n"
                        )
                game_state = "game over"
            seconds_left = str(round(game_time_left) % 60)
            if int(seconds_left) == 0:
                seconds_left += "0"
            elif int(seconds_left) < 10:
                seconds_left = "0" + seconds_left
            timer_text.update_text(str(round(game_time_left)//60) + ":" + str(seconds_left))
        timer_text.display_text(screen, 115, 307)

        # Update current wpm if the game is being played and displays it to the screen
        if game_state == "started":
            wpm_text.update_text(str(round(text_box.calc_wpm(game_time_passed))) + " WPM")
        wpm_text.display_text(screen, 450, 450)
        
        # Display the users stats
        strokes = text_box.get_stroke_counts()['total']
        correct_strokes = text_box.get_stroke_counts()['correct']
        wrong_strokes = text_box.get_stroke_counts()['wrong']
        accuracy = int(text_box.calc_accuracy() * 100)
        correct_words = text_box.get_word_counts()['correct']
        wrong_words = text_box.get_word_counts()['wrong']
        scores_text.update_text(
            "Keystrokes:           " + str(strokes) + "(C: " + str(correct_strokes) + " | W: " + str(wrong_strokes) + ")" +
            "\nAccuracy:            " + str(accuracy) + "%" +
            "\nCorrect Words:      " + str(correct_words) +
            "\nWrong Words:       " + str(wrong_words) 
            )
        scores_text.display_text(screen, 100, 400)

        # Draws the buttons
        for button in button_list:
            button.draw(screen)

        # Display image
        screen.blit(reset_icon, (633, 308))

        # Saves the visual changes to the screen
        pygame.display.update()


    # Closes the game if the exit button is pressed
    pygame_exit()

def stats_page():

    global screen, screen_width, screen_height
    # Adds the current directory to the list of directories that the program uses to check for modules
    sys.path.append('.')
    sys.path.append('..')
    from project_main import main_func
    from buttonClass import Button,Text,pygame_exit
    from Typing_Test.typing_test_engine import Word, Display_Text, Text_Box, Test_Data
    background_color = (135, 206, 235)
    

    header = Text("Avg User Stats", (255, 255, 255), "comicsans", 75)

    # Defines buttons
    button_width =  0.8 * (screen_width - screen_height)
    button_height = 50
    menu_button = Button((50,50,255), screen_width - button_width - 20, screen_height-button_height-20, button_width, button_height, main_func, "MENU", 0, None, 'comicsans', 30, (255,255,255), (40,40,150))
    back_button = Button((	255, 191, 0), screen_width - button_width - 20, 20, button_width, button_height, None, "BACK", 0, None, 'comicsans', 30, (255,255,255), (191,143,0))
    button_list = [menu_button, back_button]

    stats_text = Text("", (255,255,255), "comicsans", 50)

    avg_data = {'wpm': 0, "strokes": 0, "correct_strokes": 0, "wrong_strokes": 0, "accuracy" : 0, "correct_words":0, "wrong_words" :0}

    with open('user_typing_data.txt', 'r') as data:
        text_lines = data.readlines()
        score_data = []
        for line in text_lines:
            line = line.replace('\n', '')
            score_data.append(Test_Data(*list(map(int, line.split(' ')))))
        
        for data_type in avg_data.keys():
            for test_data in score_data:
                avg_data[data_type] += getattr(test_data, data_type)
            avg_data[data_type] = round(avg_data[data_type]/len(score_data))

    avg_wpm = avg_data['wpm']
    wpm_text = Text("WPM: " + str(avg_wpm), (255, 255, 255), "comicsans", 75)

    avg_strokes = avg_data['strokes']
    avg_correct_strokes = avg_data['correct_strokes']
    avg_wrong_strokes = avg_data['wrong_strokes']
    avg_accuracy = avg_data['accuracy']
    avg_correct_words = avg_data['correct_words']
    avg_wrong_words = avg_data['wrong_words']
    stats_text.update_text(
        "Keystrokes:           " + str(avg_strokes) + "(C: " + str(avg_correct_strokes) + " | W: " + str(avg_wrong_strokes) + ")" +
        "\nAccuracy:            " + str(avg_accuracy) + "%" +
        "\nCorrect Words:      " + str(avg_correct_words) +
        "\nWrong Words:       " + str(avg_wrong_words) 
        )

    running = True
    while running:

        # Clears the screen
        screen.fill(background_color)

        # Starts looping through all events
        for event in pygame.event.get():
            # Checks if the game was closed
            if event.type == pygame.QUIT:
                pygame_exit()

            # Checks if the mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Checks if the left mouse button was clicked
                if pygame.mouse.get_pressed()[0]:
                    # Iterates through all of the buttons and checks if they were clicked
                    for button in button_list:
                        # Checks if the button was clicke and if so it calls the buttons action function
                        if button.isOver((pygame.mouse.get_pos())):
                            if button == back_button:
                                running = False
                            else:
                                button.action()

        # Draws header
        header.display_text(screen, screen_width/2 - header.text.get_width()/2, 50)


        # Draws the buttons
        for button in button_list:
            button.draw(screen)

        wpm_text.display_text(screen, screen_width/2 - wpm_text.text.get_width()/2, 150)
        
        stats_text.display_text(screen, screen_width/2 - stats_text.text.get_width()/2/4, screen_height/2 - stats_text.text.get_height()/2*4)

        

        pygame.display.update()
    
    


# Makes sure that pygame is initialized if the file isn't called from the main menu
if __name__ == "__main__":
    pygame.init()
    main()
