import pygame 
import os
import re
import random
if os.getcwd().split("\\")[-1] != "Typing_Test":
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath) 
        os.chdir(dname)


class Word:
    '''Word class used to represent and display each word in the text display'''
    # Constance colors used in the word class  the font-color and the word-overlay-color
    RED = (255,0,0)
    GRAY = (225,225,225)
    BLACK = (0,0,0)
    GREEN = (0,128,0)
    def __init__(self, string, font, size):
        '''Initializes the word class with attributes for storing data such as the word string, font, font-size, font-color, rendered-text, width, and overlay color(none by default)'''
        self.string = string
        self.font = pygame.font.SysFont(font, size)
        self.size = size
        self.color = Word.BLACK
        self.text = self.font.render(string, True, self.color)
        self.width = self.text.get_width()
        self.overlay = None

    def update_text_color(self, new_color):
        '''Updates the text color by updating the color attribute and rerendering the text'''
        self.color = new_color
        self.text = self.font.render(self.string, True, new_color)

    def display_word(self, surface, pos):
        '''display the word and word overlay if there is one to the screen'''
        if self.overlay:
            self.draw_overlay(pos, 5, 5, self.overlay, surface)
        surface.blit(self.text, pos)

    def draw_overlay(self, pos, paddingH, paddingV, color, surface):
        '''draws of rectangle that will be used for the word overlay given the specified padding, color, and position of the word'''
        pygame.draw.rect(surface, color, pygame.Rect(pos[0] - paddingH, pos[1] - paddingV, self.text.get_width() + 2*paddingH, self.text.get_height() + 2*paddingV))

class Display_Text:
    '''Class for displaying text comprised of random compiled words to the screen'''
    # Retreives the words from the word_list.txt text file and using regex to get only the word strings
    numbers = re.compile(r"\d+ ")
    with open("word_list.txt", "r") as word_file:
        word_list = word_file.readlines()
        for i in range(len(word_list)):
            word_list[i] = re.sub(numbers, "", word_list[i])
            word_list[i] = word_list[i].replace("\n", "")

    def __init__(self, width, height, font, font_size, background_color, border_color, border_width, padding, word_spacing, line_spacing):
        '''Defines the text display width attributes to store data such as the width, height, font, font-size, background-color, border-color and width, word/line spacing, and the list of words using the custome Word datatype/class'''
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size
        self.background_color = background_color
        self.border_color = border_color
        self.border_width = border_width
        self.padding = padding
        self.word_spacing = word_spacing
        self.line_spacing = line_spacing
        self.words = []
        self.num_lines = 1 + (height-2*padding-font_size)//(font_size)

        # Generates the initial words
        self.generate_words(self.num_lines)

        # Prints the starting words to the screen for debugging(varifying that the programs runs correctly) purposes
        for row in self.words:
            for word in row:
                print(word.string, end=" ")
            print("")

        # Keepes track of the currect word that the user must type
        self.current_word = self.words[0][0]
        self.current_word_index = 0
        self.current_word.overlay = Word.GRAY

    def generate_words(self, lines):
        '''a method that uses the demensions of the given text display to layout random words from the wordlist into rows such that they fit within the bounds of the text display'''
        for i in range(lines):
            row = []
            total_length = 2*self.padding
            next_word = Word(random.choice(Display_Text.word_list), self.font, self.font_size)
            while total_length + self.word_spacing + next_word.width < self.width:
                row.append(next_word)
                total_length += row[-1].width
                total_length += self.word_spacing
                next_word = Word(random.choice(Display_Text.word_list), self.font, self.font_size)
            self.words.append(row)

    def display_text_display(self, surface, pos):
        '''a method used to draw the textbox onto the screen including the boarder, the textbox itself, and the words contained inside it'''

        # Display the textbox background and border using rectangles, given the measurements of the textbox
        pygame.draw.rect(surface, self.border_color, pygame.Rect(pos[0]-self.border_width, pos[1]-self.border_width, self.width + 2*self.border_width, self.height + 2*self.border_width))
        pygame.draw.rect(surface, self.background_color, pygame.Rect(pos[0], pos[1], self.width, self.height))
        
        # Displays the word in the text box using the precalculated rows and columns and the predefined padding, wordspacing, and linespacing
        y = self.padding
        for row in self.words:
            x = self.padding
            for word in row:
                word.display_word(surface, (pos[0] + x, pos[1] + y))
                x += word.width
                x += self.word_spacing
            y += self.font_size
            y += self.line_spacing

    def next_word(self, correct):
        '''Updates the current word'''
        self.current_word.overlay = None
        #sets the previous word's font-color to green if the word was typed correctly
        if correct:
            self.current_word.update_text_color(Word.GREEN)
        # otherwise the font-color is set to red
        else:
            self.current_word.update_text_color(Word.RED)

        # Updates the current word index and current word attributes by setting it to the next word in the text display
        if self.current_word_index < len(self.words[0]) - 1:
            self.current_word_index += 1
            self.current_word = self.words[0][self.current_word_index]
        # If the word is the last word in the text display a new word list is generated and the current word is set back to the first word in the text display
        else:
            self.words.pop(0)
            self.generate_words(1)
            self.current_word_index = 0
            self.current_word = self.words[0][0]

        # sets the new current word's overlay to gray which indicates to the user that it is now the current word
        self.current_word.overlay = Word.GRAY



        
class Text_Box:
    '''Class that accepts text data from the user and display it to the screen'''
    def __init__(self, pos, width, height, font, font_size, background_color, border_color, selected_color, border_width, padding):
        '''Defines a text box with many physical display attributes'''
        self.pos = pos
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(font, font_size)
        self.font_size = font_size
        self.background_color = background_color
        self.border_color = border_color
        self.selected_color = selected_color
        self.border_width = border_width
        self.padding = padding
        self.is_selected = False
        self.text = ""
        self.cursor_color = (0,0,0)
        self.stroke_list = []
        self.word_list = []

    def display_text_box(self, surface):
        '''Displays the text box to the screen'''
        rendered_text = self.font.render(self.text, True, (0,0,0))
        # Subtracts letters from the end of the text until it fits within the bounds of the text box
        while rendered_text.get_width() > self.width - 2*self.padding:
            self.text = self.text[:-1] 
            rendered_text = self.font.render(self.text, True, (0,0,0))
        # Changes the border color if the text box is selected
        if self.is_selected:
            border_color = self.selected_color
        # Otherwise resets the boarder color to the default border color
        else:
            border_color = self.border_color

        # Uses pygame rectangles to display the textbox background and border
        pygame.draw.rect(surface, border_color, pygame.Rect(self.pos[0]-self.border_width, self.pos[1]-self.border_width, self.width + 2*self.border_width, self.height + 2*self.border_width))
        pygame.draw.rect(surface, self.background_color, pygame.Rect(self.pos[0], self.pos[1], self.width, self.height))

        # Displays the text box text to the screen
        surface.blit(rendered_text, (self.pos[0] + self.padding, self.pos[1] + self.padding))

        # Uses pygame lines to display the cursor
        cursor_x = self.pos[0] + rendered_text.get_width() + 10
        cursor_top = self.pos[1] + self.padding
        cursor_bottom = cursor_top + self.height - 2*self.padding
        if self.is_selected:
            pygame.draw.line(surface, self.cursor_color, (cursor_x, cursor_top), (cursor_x, cursor_bottom), 1)

    def click_in_box(self, click_pos):
        '''method that returns a boolean whcih represents weather a given position is inside the bounds of the text box'''
        return click_pos[0] > self.pos[0] and click_pos[0] < self.pos[0] + self.width and click_pos[1] > self.pos[1] and click_pos[1] < self.pos[1] + self.height

    def clear_text(self):
        '''clears the text from the screen'''
        self.text = ""

    def log_stroke(self, text_display):
        '''appends the most reccent key stroke to the list of keystrokes using the word data class to store the key stroke data'''
        self.stroke_list.append(Word_Data(self.text[-1], self.word_match(text_display)))

    def log_word(self, text_display):
        '''same as log stroke but it logs an entire owrd to the word list'''
        self.word_list.append(Word_Data(self.text, self.full_word_match(text_display)))

    def word_match(self, text_display):
        '''returns a boolean which represents weather the text in the text box could match with the current word'''
        return re.match(r"^" + self.text, text_display.current_word.string)

    def full_word_match(self, text_display):
        '''checks if the text in the text box is exactly the same as the current word'''
        return self.text == text_display.current_word.string

    def calc_wpm(self, time):
        '''calculates the words per minute using the amount of word typed correctly and the time passed'''
        if time:
            return self.get_word_counts()["correct"] * 60/time
        else:
            return 0

    def calc_accuracy(self):
        '''calculates the accuracy based on the amount of correct strokes over the amount of total strokes'''
        total_strokes = self.get_stroke_counts()["total"]
        if total_strokes:
            return self.get_stroke_counts()["correct"]/total_strokes
        else:
            return 1

    def get_word_counts(self):
        '''returns a dictionary with the number of total, correnct, and wrong words'''
        return {"total": len(self.stroke_list), 
                "correct": len(list(filter(lambda word: word.correct, self.word_list))), 
                "wrong": len(list(filter(lambda word: not word.correct, self.word_list)))}

    def get_stroke_counts(self):
        '''returns a dictionary with the number of total, correnct, and wrong keystrokes'''
        return {"total": len(self.stroke_list), 
                "correct": len(list(filter(lambda word: word.correct, self.stroke_list))), 
                "wrong": len(list(filter(lambda word: not word.correct, self.stroke_list)))}

    

class Word_Data:
    '''A class used to store data related to allready typed words/keystrokes'''
    def __init__(self, text, correct):
        '''Stores the text of the word and weather it was correct off not in attributes called text and correct'''
        self.text = text
        self.correct = correct 

class Test_Data:
    '''A class used to store the users test data '''
    def __init__(self, wpm, strokes, correct_strokes, wrong_strokes, accuracy, correct_words, wrong_words):
        self.wpm = wpm 
        self.strokes = strokes
        self.correct_strokes = correct_strokes
        self.wrong_strokes = wrong_strokes
        self.accuracy = accuracy
        self.correct_words = correct_words
        self.wrong_words = wrong_words
