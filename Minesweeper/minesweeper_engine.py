"""
- Contains all the classes for storing the game data
- Cell class stores data about each cell and Grid class stores data about the entire grid
"""

import pygame
from random import randint, choice
from time import sleep

# Class used to store information about each individual cell
# The grid is made up of cell objects
# It also contains the code to draw each cell which is used to draw the entire grid
class Cell:
    # Initializes the cell object given the position, whether it contains a mine, the size of each cell, the font size, and wether it is an even cell or not
    # It also defines other attributes such as hover color which are used to draw the cell later
    def __init__(self, pos, mine, cell_size, font_size, is_even_cell):
        self.mine = mine
        color_options = [(255,0,0),(255,127,0),(255,255,0),(127,255,0),(0,255,0),(0,255,127),(0,255,255),(0,127,255),(0,0,255),(127,0,255),(255,0,255),(255,0,127)]
        self.mine_color = choice(color_options)
        self.pos = pos
        self.mine_count = 0
        self.visible = False
        self.size = cell_size
        self.marked = False
        self.show_text = False
        self.show_mine = False
        # Changes the cell color if it is an even cell, creating a checkerboard pattern
        if is_even_cell:
            self.color = (63,199,48)
            self.visible_color = (172,131,103)
        else:
            self.color = (86,255,67)
            self.visible_color = (226,173,137)
        self.font_color = (255,0,0)
        self.font_size = font_size
        self.hover_color = (213, 255, 169)
    
    # Counts the number of adjacently and diagonally touching mines given the list of cell instances that make up the grid and the position of the current cell in the list
    def count_mines(self, cells, pos):
        count = 0
        for v in range(-1, 2, 1):
            for h in range(-1, 2, 1):
                if v != 0 or h != 0:
                    # Prevents the program from using negative indexes and therefore counting mines on the other side of the grid when the current cell is on top or left boarder
                    if pos[0]+v > -1 and pos[1]+h > -1:
                        # The try statement prevents the program from throwing an error when the index exceeds the grid size
                        try:
                            if cells[pos[0]+v][pos[1]+h].mine:
                                count += 1
                        except IndexError:
                            pass
        return count
    
    # Draws the cell based on its color and whether it is flagged, is visible, and/or contains a mine
    def draw(self, surface, grid):
        mouse_pos = grid.mouse_to_index(pygame.mouse.get_pos())
        # Sets the color of the cell to the hover color if the mouse is above the cell
        if mouse_pos == (self.pos[1]/self.size, self.pos[0]/self.size):
            draw_color = self.hover_color
        else:
            draw_color = self.color
        
        # Checks if the cell is visible and if so, itdraws it with it's visible color
        if self.visible:
            self.show_text = True
            pygame.draw.rect(surface, self.visible_color, (self.pos[0], self.pos[1], self.size, self.size))
            # Checks if the cell contains a mine and if so, it draws that mine ontop of the cell
            if self.mine:
                self.show_text = False
                pygame.draw.rect(surface, self.mine_color, (self.pos[0], self.pos[1], self.size, self.size))
                center_color = tuple(map(lambda x: x/2, self.mine_color))
                pygame.draw.circle(surface, center_color, (int(self.pos[0]+self.size/2), int(self.pos[1]+self.size/2)), int(self.size/4))
        # Checks if the cell is marked and draws the flag ontop of the cell if it is
        elif self.marked:
            pygame.draw.rect(surface, draw_color, (self.pos[0], self.pos[1], self.size, self.size))
            surface.blit(grid.flag, self.pos)
        # Draws the cell normaly if none of the previously mentioned conditions are met
        else:
            pygame.draw.rect(surface, draw_color, (self.pos[0], self.pos[1], self.size, self.size))
            
        # Checks if the text is suposed to be drawn and makes sure that the text is not 0. Then it calls the draw_num method to draw the text ontop of the cell
        if self.show_text and self.mine_count != 0:
            self.draw_num(surface, str(self.mine_count), self.pos)
    
    # Displays centered text ontop of the cell give the text and the position of the cell(upper left corner)
    def draw_num(self, surface, text, pos):
        # Changes the color of the text based on the number
        if text == "1":
            self.font_color = (50,82, 176)
        elif text == "2":
            self.font_color = (0, 128, 0)
        elif text == "3":
            self.font_color = (255, 0, 0)
        elif int(text) > 3:
            self.font_color = (128, 0, 128)

        # Selects, renders, centers, and displays the font/text
        num_font = pygame.font.SysFont("open sans", self.font_size, True)
        rendered_text = num_font.render(text, False, self.font_color)
        surface.blit(rendered_text, (pos[0]+self.size/2-rendered_text.get_width()/2, pos[1]+self.size/2-rendered_text.get_height()/2))

# A class used to store the entire game board 
# Contains methods pertaining to the entire game board
# Revolves around a 2d list of cell instances that represents the game board and all of its attributes/data
class Grid:
    # Defines the grid given the size in pixels and in cells
    # Defines the list of cells and size of each cell
    def __init__(self, mode, grid_size_px):
        modes = {"easy": 10, "medium": 15, "hard": 20}
        grid_size_cells = modes[mode]
        self.mode = mode
        self.grid_size_cells = grid_size_cells
        self.grid_size_px = grid_size_px
        self.cell_size =  grid_size_px/grid_size_cells
        self.board_state = "in_play"

        # Generates the 2d array of cells
        self.cells = []
        for y in range(grid_size_cells):
            self.cells.append([])
            for x in range(grid_size_cells):
                is_even = False
                if (x+y)%2 == 0:
                    is_even = True
                self.cells[y].append(Cell((x*self.cell_size, y*self.cell_size), self.generate_mine_bool(), self.cell_size, int(0.9*self.cell_size), is_even))

        # Calculates and updates the number of adjacent mines for each cell
        for y in range(len(self.cells)):
            for x in range(len(self.cells[0])):
                self.cells[y][x].mine_count = self.cells[y][x].count_mines(self.cells, (y,x))

        # Defines the flag image and resizes it to fit the cell size
        self.flag = pygame.image.load("minesweeper_image_assets/flag_icon.png")
        self.flag = pygame.transform.scale(self.flag, (int(self.cell_size), int(self.cell_size)))

        # Defines a list with the locations of all the mines in the grid
        # Used for revealing the mines when the player loses the game
        self.mine_locations = [[row, col] for row in range(len(self.cells)) for col in range(len(self.cells[row])) if self.cells[row][col].mine]

    
    # A function that uncovers all the necessary cells when the user clicks a square on the board
    def uncover_cell(self, row, col, screen):
        if not self.cells[row][col].mine:
            self.cells[row][col].visible = True
            directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]
            if self.cells[row][col].mine_count == 0:
                for direction in directions:
                    # Prevents the program from using negative indexes and therefore revealing cells on the other side of the grid when the current cell is on top or left boarder
                    if row + direction[0] > -1 and col + direction[1] > -1:
                        # The try statemetn prevents the program from throwing an error when the index exceeds the grid size
                        try:
                            # Stops the program from running the uncover cell method on cells that have already been uncovered. This prevents infinite recursion
                            if not self.cells[row + direction[0]][col + direction[1]].visible:
                                self.uncover_cell(row + direction[0], col + direction[1], screen)
                        except IndexError:
                            pass
        else:
            # Plays the bomb sound effect
            bomb_sound = pygame.mixer.Sound("./minesweeper_sound_effects/ding.wav")
            bomb_sound.play()

            # Updates board state
            self.board_state = "revealing_mines"
            cell = self.cells[row][col]
            if not cell.visible:
                cell.visible = True
                # Code for lightup animation effect when bomb is uncovered
                for brighter in range(200, 0, -5):
                    before_brighter = cell.mine_color
                    cell.mine_color = tuple(map(lambda x: min(255, x+brighter), cell.mine_color))
                    cell.draw(screen, self)
                    pygame.display.update()
                    cell.mine_color = before_brighter
                    sleep(0.01)
        
    # A function that returns true approximately every 1/10 times
    # This is used as the probabilty function for determining whether a cell is a mine
    def generate_mine_bool(self):
        if self.mode == "easy":
            num = randint(0, 9)
            max_num = 9
        elif self.mode == "medium":
            num = randint(0, 9)
            max_num = 9
        elif self.mode == "hard":
            num = randint(0, 9)
            max_num = 9
        if num > max_num-1:
            return True
        else:
            return False
    
    # Draws the grid by calling the draw method on each cell in the array of cells
    def draw(self, surface):
        for row in self.cells:
            for cell in row:
                cell.draw(surface, self)
    
    # Converts the mouse position to the indexes of the cell in the array of cells that the mouse is hovering over
    def mouse_to_index(self, pos):
        if pos[0] <= self.grid_size_px and pos[1] <= self.grid_size_px:
            return (int(pos[1]//self.cell_size), int((pos[0]-1) //self.cell_size))

    # Checks if all the non mine cells have been uncovered
    def win(self):
        for row in self.cells:
            for cell in row:
                if not cell.visible and not cell.mine:
                    return False
        return True