import pygame, sys, os
import random
import time
from sprite import *
from settings import *
from bfs import *
from astar import *


class MainGame:
    def __init__(self):
        pygame.init()
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.display.set_caption("Eight Puzzle")
        self.show_solution = False
        self.start_shuffle = False
        self.previous_choice = ""
        self.shuffle_time = 0
        self.move_len = 0
        self.move_count = False
        self.text_solve = False
        self.screen = pygame.display.set_mode((width, height))
        self.fpsClock = pygame.time.Clock()


    def puzzleGame(self):
        grid = [[x - 1 + y * grid_size for x in range(1, grid_size + 1)] for y in range(grid_size)]
        grid[0][0] = 0
        print(grid)
        return grid

    def shuffle(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.initial_tiles[row][col], self.initial_tiles[row][col + 1] = self.initial_tiles[row][col + 1], self.initial_tiles[row][col]

        elif choice == "left":
            self.initial_tiles[row][col], self.initial_tiles[row][col - 1] = self.initial_tiles[row][col - 1], self.initial_tiles[row][col]

        elif choice == "up":
            self.initial_tiles[row][col], self.initial_tiles[row - 1][col] = self.initial_tiles[row - 1][col], self.initial_tiles[row][col]

        elif choice == "down":
            self.initial_tiles[row][col], self.initial_tiles[row + 1][col] = self.initial_tiles[row + 1][col], self.initial_tiles[row][col]

    def bfs(self):
        initial_board = []
        for line in self.initial_tiles:
            for num in line:
                initial_board.append(num)

        solution_path = startBFS(initial_board)

        self.num_to_move = []
        print(solution_path)
        countindex = 0

        for path in solution_path:
            if countindex != (len(solution_path) - 1):
                temp_path = solution_path[countindex + 1]
                print(f"{path} == {temp_path}")

                for (fp, sp) in zip(path, temp_path):
                    print(f"{fp} = {sp}")
                    if fp != sp and fp != 0:
                        self.num_to_move.append(fp)
                        break
            countindex += 1

        print(self.num_to_move)
        print("Done Breadth First Search Path")

    def astar(self):
        astar_sol = initial_board(self.initial_tiles)
        astar_sol.reverse()
        print(astar_sol)

        self.num_to_move = []
        countindex = 0

        for path in astar_sol:
            if countindex != (len(astar_sol) - 1):
                temp_path = astar_sol[countindex + 1]
                print(f"{path} == {temp_path}")

                for (fp, sp) in zip(path, temp_path):
                    print(f"{fp} = {sp}")
                    if fp != sp and fp != 0:
                        self.num_to_move.append(fp)
                        break
            countindex += 1

        print(self.num_to_move)
        print("Done A-star Path")

    def solutionMove(self, num):
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right() and self.initial_tiles[row][col + 1] == num:
                        self.initial_tiles[row][col], self.initial_tiles[row][col + 1] = self.initial_tiles[row][col + 1], self.initial_tiles[row][col]

                    if tile.left() and self.initial_tiles[row][col - 1] == num:
                        self.initial_tiles[row][col], self.initial_tiles[row][col - 1] = self.initial_tiles[row][col - 1], self.initial_tiles[row][col]

                    if tile.up() and self.initial_tiles[row - 1][col] == num:
                        self.initial_tiles[row][col], self.initial_tiles[row - 1][col] = self.initial_tiles[row - 1][col], self.initial_tiles[row][col]

                    if tile.down() and self.initial_tiles[row + 1][col] == num:
                        self.initial_tiles[row][col], self.initial_tiles[row + 1][col] = self.initial_tiles[row + 1][col], self.initial_tiles[row][col]
                    break
        
                        

    def draw_tiles(self):
        self.tiles = []

        for row, x in enumerate(self.initial_tiles):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0:
                    self.tiles[row].append(Tile(self, col, row, str(tile)))
                else:
                    self.tiles[row].append(Tile(self, col, row, "empty"))

    def new(self):
        self.show_solution = False
        self.shuffle_time = 0
        self.all_sprites = pygame.sprite.Group()
        self.initial_tiles = self.puzzleGame()
        self.goal_tiles = self.puzzleGame()
        self.draw_tiles()
        self.test = UIElement(530, 20, "Eight Puzzle - BFS", 20)
        self.puzzleSolved = UIElement(100, 200, "Puzzle Solved!", 30)
        self.text_solve =  False
        self.move_len = 0

        self.buttons_list = []
        self.buttons_list.append(Button(550, 80, 160, 50, "Reset", white, num_color))
        self.buttons_list.append(Button(550, 160, 160, 50, "Shuffle", white, num_color))
        self.buttons_list.append(Button(550, 240, 160, 50, "BFS", white, num_color))
        self.buttons_list.append(Button(550, 320, 160, 50, "A-star", white, num_color))
        self.buttons_list.append(Button(550, 400, 160, 50, "Show Solution", white, num_color))
        

    def run(self):
        self.playing = True
        while self.playing:
            self.fpsClock.tick(60)
            self.events()
            self.update()
            self.draw()

    def update(self):
        if self.show_solution:
            if self.initial_tiles ==  self.goal_tiles:
                print("--PUZZLE SOLVED--")
                self.text_solve = True
                self.show_solution = False

        if self.start_shuffle:
            self.shuffle()
            self.draw_tiles()
            self.shuffle_time += 1
            if self.shuffle_time > 10:
                self.start_shuffle = False
                self.shuffle_time = 0
                print(self.initial_tiles)
        
        if self.move_count:
            self.solutionMove(self.num_to_move[self.move_len])
            self.draw_tiles()
            self.move_len += 1
            time.sleep(0.3)
            #print(len(self.num_to_move))
            if self.move_len == len(self.num_to_move):
                self.move_count = False
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(background)
        self.all_sprites.draw(self.screen)
        self.draw_grid()
        self.test.draw(self.screen)

        if self.text_solve:
            self.puzzleSolved.draw(self.screen)

        for button in self.buttons_list:
            button.draw(self.screen)

        pygame.display.flip()

    def draw_grid(self):
        for row in range(-1, grid_size * tiles_size, tiles_size):
            pygame.draw.line(self.screen, grid_color, (row, 0), (row, grid_size * tiles_size))

        for column in range(-1, grid_size * tiles_size, tiles_size):
            pygame.draw.line(self.screen, grid_color, (0, column), (grid_size * tiles_size, column))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):

                            if tile.right() and self.initial_tiles[row][col + 1] == 0:
                                self.initial_tiles[row][col], self.initial_tiles[row][col + 1] = self.initial_tiles[row][col + 1], self.initial_tiles[row][col]

                            if tile.left() and self.initial_tiles[row][col - 1] == 0:
                                self.initial_tiles[row][col], self.initial_tiles[row][col - 1] = self.initial_tiles[row][col - 1], self.initial_tiles[row][col]

                            if tile.up() and self.initial_tiles[row - 1][col] == 0:
                                self.initial_tiles[row][col], self.initial_tiles[row - 1][col] = self.initial_tiles[row - 1][col], self.initial_tiles[row][col]

                            if tile.down() and self.initial_tiles[row + 1][col] == 0:
                                self.initial_tiles[row][col], self.initial_tiles[row + 1][col]= self.initial_tiles[row + 1][col], self.initial_tiles[row][col]

                            self.draw_tiles()

                for button in self.buttons_list:
                    if button.click(mouse_x, mouse_y):
                        if button.text == "Shuffle":
                            self.start_shuffle = True
                        if button.text == "Reset":
                            self.new()
                        if button.text == "BFS":
                            print("--Breadth First Search--")
                            self.bfs()
                        if button.text == "A-star":
                            print("--A-star--")
                            self.astar()
                        if button.text == "Show Solution":
                            print("--Showing Solution--")
                            self.move_count =  True
                            self.show_solution = True

game = MainGame()
while True:
    game.new()
    game.run()
