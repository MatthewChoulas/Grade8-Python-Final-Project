"""
- This File contains code for the button object,text object, and the pygame_exit function
- Text: used for adding text to screen
- Button: used for creating a button
- Pygame_exit: used to end the game
"""

import sys
import pygame

# Calls multiple function that end the game
def pygame_exit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()

# Class that contains all the code/functions to make text appear on screen
class Text():

    # defines text object with the specified text, text color, font type, and fontsize
    # attributes font and text store the corresponding pygame font object and rendered text respectively
    def __init__(self, text, color, font, size):
        self.color = color
        self.string = text
        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, color)

    def update_text(self, new_text):
        self.string = new_text
        self.text = self.font.render(new_text, True, self.color)
    
    # Displays the text word by word to the screen at specified (x,y) position
    # This means that the display_text function can blit multiline text to the screen
    def display_text(self, surface, *pos):
        words = [word.split(' ') for word in self.string.splitlines()]  # 2D array where each row is a list of words.
        space = self.font.size(' ')[0]  # The width of a space.
        max_width, max_height = surface.get_size()
        x, y = pos
        for line in words:
            for word in line:
                word_surface = self.font.render(word, 0, self.color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                surface.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.

# Class used to make a button with color, size, position, text, border, hover, and an action
class Button():
    # Action is a function that is called when the button is clicked
    def __init__(self, color, x, y, width, height,  action, text='', border_width=0, border_color=None, font='freesansbold', font_size=60, font_color=(0,0,0),hover_color=None):
        self.color = color 
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.action = action
        if text != "":
            self.button_text = Text(text, font_color, font, font_size)
        else:
            self.button_text = None 
        self.border_width = border_width
        self.border_color = border_color

        # Sets the hover color to the normal color if it isn't given
        if hover_color:
            self.hover_color = hover_color
        else:
            self.hover_color = color
    # Call this method to draw the button on the screen
    def draw(self,win):
        # Draws a centered border behind the button
        if self.border_color and self.border_width:
            pygame.draw.rect(win, self.border_color, (self.x-self.border_width/2,self.y-self.border_width/2,self.width+self.border_width,self.height+self.border_width),0)

        # Draws the rectangle of the button using the color attribute or hover color attribute if the mouse is ontop of the button
        draw_color = self.color
        if self.isOver(pygame.mouse.get_pos()):
            draw_color = self.hover_color
        pygame.draw.rect(win, draw_color, (self.x,self.y,self.width,self.height),0)
        
        # Adds centered text to the button
        if self.button_text:
            self.button_text.display_text(win, self.x + (self.width/2 - self.button_text.text.get_width()/2), self.y + (self.height/2 - self.button_text.text.get_height()/2))

    
    # Checks if the mouse is over the button by comparing the mouse coordinates to the position and size of the button
    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

