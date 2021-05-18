def tetris_main_function():
    import pygame
    import random
    import os
    if os.getcwd().split("\\")[-1] != "Tetris":
            abspath = os.path.abspath(__file__)
            dname = os.path.dirname(abspath) 
            os.chdir(dname)
    pygame.font.init()
    #Global Variables
    screen_width = 800
    screen_height = 700
    grid_width = 300
    grid_height = 600
    block_size = 30
    grid_top_left_x = (screen_width - grid_width) // 2
    grid_top_left_y = screen_height - grid_height
    pygame.mixer.init()
    pygame.mixer.music.load("Tetris_Song.mp3")
    pygame.mixer.music.set_volume(0.15)
    pygame.mixer.music.play(-1)
    #Shapes
    S = [['.....',
        '.....',
        '..00.',
        '.00..',
        '.....'],
        ['.....',
        '..0..',
        '..00.',
        '...0.',
        '.....']]

    Z = [['.....',
        '.....',
        '.00..',
        '..00.',
        '.....'],
        ['.....',
        '..0..',
        '.00..',
        '.0...',
        '.....']]

    I = [['..0..',
        '..0..',
        '..0..',
        '..0..',
        '.....'],
        ['.....',
        '0000.',
        '.....',
        '.....',
        '.....']]

    O = [['.....',
        '.....',
        '.00..',
        '.00..',
        '.....']]

    J = [['.....',
        '.0...',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..00.',
        '..0..',
        '..0..',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '...0.',
        '.....'],
        ['.....',
        '..0..',
        '..0..',
        '.00..',
        '.....']]

    L = [['.....',
        '...0.',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..0..',
        '..0..',
        '..00.',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '.0...',
        '.....'],
        ['.....',
        '.00..',
        '..0..',
        '..0..',
        '.....']]

    T = [['.....',
        '..0..',
        '.000.',
        '.....',
        '.....'],
        ['.....',
        '..0..',
        '..00.',
        '..0..',
        '.....'],
        ['.....',
        '.....',
        '.000.',
        '..0..',
        '.....'],
        ['.....',
        '..0..',
        '.00..',
        '..0..',
        '.....']]

    shapes_list = [S, Z, I, O, J, L, T]
    shape_colors_list = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
    # index 0 - 6 represent shape

    #Since there are multiple shapes_list, a piece class to store information is very useful.
    class Piece(object):  # *
        def __init__(self, x, y, shape):
            self.x = x
            self.y = y
            self.shape = shape
            self.color = shape_colors_list[shapes_list.index(shape)]
            self.rotation = 0

    #This function will have a multidimensional list that serves as a grid for the game. Each element of the list will represent the color of the piece in that current position.
    def create_grid(locked_pos={}):  # *
        grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (j, i) in locked_pos:
                    c = locked_pos[(j,i)]
                    grid[i][j] = c
        return grid

    #This function rotates the shape whenever the user presses the right, up, down, or left buttons.
    def convert_shape(shape):
        positions = []
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    positions.append((shape.x + j, shape.y + i))

        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

        return positions

    #This function checks whether or not the space the user wants to move to is the edge of the grid or not, and if it isn't the block doesn't move.
    def valid_space(shape, grid):
        accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
        accepted_pos = [j for sub in accepted_pos for j in sub]

        formatted = convert_shape(shape)

        for pos in formatted:
            if pos not in accepted_pos:
                if pos[1] > -1:
                    return False
        return True

    #As the function name states, it checks whether or not the user lost the game.
    def check_lost(positions):
        for pos in positions:
            x, y = pos
            if y < 1:
                return True

        return False

    #This function will help generate a random shape that will drop down the screen after picked.
    def get_shape():
        return Piece(5, 0, random.choice(shapes_list))

    #This function simply centers the text for anything we want to type into the interface of the game.
    def draw_text_middle(surface, text, size, color):
        font = pygame.font.SysFont("comicsans", size, bold=True)
        label = font.render(text, 1, color)

        surface.blit(label, (grid_top_left_x + grid_width /2 - (label.get_width()/2), grid_top_left_y + grid_height/2 - label.get_height()/2))

    #This function will simply draw all of the objects to the screen.
    def draw_grid(surface, grid):
        sx = grid_top_left_x
        sy = grid_top_left_y

        for i in range(len(grid)):
            pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+grid_width, sy+ i*block_size))
            for j in range(len(grid[i])):
                pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + grid_height))

    #This text clears a row, which is used for whenever the user fills in a clear row giving them 10 points.
    def clear_row(grid, locked):

        inc = 0
        for i in range(len(grid)-1, -1, -1):
            row = grid[i]
            if (0,0,0) not in row:
                inc += 1
                ind = i
                for j in range(len(row)):
                    try:
                        del locked[(j,i)]
                    except:
                        continue

        if inc > 0:
            for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
                x, y = key
                if y < ind:
                    newKey = (x, y + inc)
                    locked[newKey] = locked.pop(key)

        return inc

    #This functon draws the next shape box on the left of the screen which shows the next shape the user will have to place.
    def draw_next_shape(shape, surface):
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Next Shape', 1, (255,255,255))

        sx = grid_top_left_x + grid_width + 50
        sy = grid_top_left_y + grid_height/2 - 100
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

        surface.blit(label, (sx + 10, sy - 30))

    #This function updates the score the player has in a text document.
    def update_score(nscore):
        score = max_score()

        with open('scores.txt', 'w') as f:
            if int(score) > nscore:
                f.write(str(score))
            else:
                f.write(str(nscore))

    #This function obtains the max score through the same text document as the update_score function does.
    def max_score():
        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            score = lines[0].strip()

        return score

    #This function draws the window of the game and also draws the score and high score.
    def draw_window_game(surface, grid, score=0, last_score = 0):
        surface.fill((0, 0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Tetris', 1, (255, 255, 255))

        surface.blit(label, (grid_top_left_x + grid_width / 2 - (label.get_width() / 2), 30))

        # current score
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Score: ' + str(score), 1, (255,255,255))

        sx = grid_top_left_x + grid_width + 50
        sy = grid_top_left_y + grid_height/2 - 100

        surface.blit(label, (sx + 20, sy + 160))
        # last score
        label = font.render('High Score: ' + last_score, 1, (255,255,255))

        sx = grid_top_left_x - 200
        sy = grid_top_left_y + 200

        surface.blit(label, (sx + 20, sy + 160))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                pygame.draw.rect(surface, grid[i][j], (grid_top_left_x + j*block_size, grid_top_left_y + i*block_size, block_size, block_size), 0)

        pygame.draw.rect(surface, (255, 0, 0), (grid_top_left_x, grid_top_left_y, grid_width, grid_height), 5)

        draw_grid(surface, grid)
        #pygame.display.update()

    #This is the main function where the pygame loop occurs.
    def main(win):  # *
        

        last_score = max_score()
        locked_positions = {}
        grid = create_grid(locked_positions)
        change_piece = False
        run = True
        current_piece = get_shape()
        next_piece = get_shape()
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        level_time = 0
        score = 0
        screen = pygame.display.set_mode((800,700))
        font = pygame.font.SysFont(None, 32)
        start_time = pygame.time.get_ticks() 

        while run:
            grid = create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            level_time += clock.get_rawtime()
            clock.tick()

            if level_time/1000 > 5:
                level_time = 0
                if level_time > 0.12:
                    level_time -= 0.005

            if fall_time/1000 > fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.display.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.rotation -= 1

            counting_time = pygame.time.get_ticks() - start_time
            counting_minutes = str(int(counting_time/60000)).zfill(2)
            counting_seconds = str(int((counting_time%60000)/1000)).zfill(2)
            counting_millisecond = str(counting_time%1000).zfill(3)        
            counting_string = "%s:%s:%s" % (counting_minutes, counting_seconds, counting_millisecond)
            counting_text = font.render(str(counting_string), 1, (255,255,255))        
            timerText = font.render('Time Passed: ', False, (255, 255, 255))

            shape_pos = convert_shape(current_piece)

            for i in range(len(shape_pos)):
                x, y = shape_pos[i]
                if y > -1:
                    grid[y][x] = current_piece.color

            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = get_shape()
                change_piece = False
                score += clear_row(grid, locked_positions) * 10

            draw_window_game(win, grid, score, last_score)
            draw_next_shape(next_piece, win)
            pygame.display.update()

            if check_lost(locked_positions):
                draw_text_middle(win, "YOU LOST!", 80, (255,255,255))
                pygame.display.update()
                pygame.time.delay(1500)
                run = False
                update_score(score)

            pygame.draw.rect(screen, (0, 0, 0), ( 0, 50, 100, 150))
            screen.blit(timerText, (grid_top_left_x - 200, grid_top_left_y - 40))
            screen.blit(counting_text, (grid_top_left_x - 200, grid_top_left_y - 20))
            pygame.display.update()
            clock.tick(25)
        
    #This function pulls up the main menu where the user will press the enter key to play.
    def main_menu(win):
        run = True
        main
        while run:
            win.fill((0,0,0))
            draw_text_middle(win, 'Press The R Key To Play Again Or Backspace To Go To The Main Menu', 29, (255,255,255))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main(win)
                        pygame.mixer.music.stop()
                    elif event.key == pygame.K_BACKSPACE:
                        from project_main import main_func
                        pygame.mixer.music.stop()
                        main_func()

        pygame.display.quit()

    win = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Tetris')
    main_menu(win)
