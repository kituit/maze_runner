import os
import sys

from maze import Maze

os.environ['SDL_AUDIODRIVER'] = 'dsp'
import pygame

# initialize all imported pygame modules
pygame.init()

class GuiError(Exception):
    pass

class Gui():

    COLOUR_EMPTY = (255, 255, 255)
    COLOUR_WALL = (0, 0, 0)
    COLOUR_VISITED = (255, 0, 0)
    COLOUR_PATH = (0, 255, 0)

    CELL_SIZE = 20
    FPS = 10

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = Maze(cols, rows)
        self.win = pygame.display.set_mode(self.calc_display_dimensions())
        pygame.display.set_caption("Maze runner")
        self.clock = pygame.time.Clock()

        self.render()

    def calc_display_dimensions(self):
        return (self.cols * self.CELL_SIZE, self.rows * self.CELL_SIZE)

    def create_maze(self):

        cont = True
        set_start = False
        set_end = False
        while cont:
            self.clock.tick()

            # Get all events
            ev = pygame.event.get()

            # Left mouse click to create walls
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                x, y = pos
                x, y = x // self.CELL_SIZE, y // self.CELL_SIZE
                self.maze.set_cell(x, y, Maze.WALL)
                self.render_cell(x, y, self.get_colour(Maze.WALL))

            # Right mouse click to end maze creation
            if pygame.mouse.get_pressed()[2]:
                cont = False

            for event in ev:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    pos = pygame.mouse.get_pos()
                    x, y = pos
                    x, y = x // self.CELL_SIZE, y // self.CELL_SIZE
                    if event.key == pygame.K_s:
                        if set_start:
                            self.render_cell(*self.maze.get_start_pos(),
                                             self.get_colour(Maze.EMPTY))
                        self.maze.set_cell(x, y, Maze.START)
                        self.render_cell(x, y, self.get_colour(Maze.START))
                        set_start = True
                    elif event.key == pygame.K_e:
                        if set_end:
                            self.render_cell(*self.maze.get_end_pos(), self.get_colour(Maze.EMPTY))
                        self.maze.set_cell(x, y, Maze.END)
                        self.render_cell(x, y, self.get_colour(Maze.END))
                        set_end = True

            pygame.display.update()

        if not set_start:
            self.maze.set_cell(0, 0, Maze.START)
            self.render_cell(0, 0, self.get_colour(Maze.START))
        if not set_end:
            self.maze.set_cell(self.cols - 1, self.rows - 1, Maze.END)
            self.render_cell(self.cols - 1, self.rows - 1, self.get_colour(Maze.END))
        pygame.display.update()

    def run_simulation(self):
        for pos in self.maze.bfs_iter():
            self.clock.tick(60)
            if pos not in [self.maze.get_start_pos(), self.maze.get_end_pos()]:
                self.render_cell(*pos, self.COLOUR_VISITED)
            pygame.display.update()

        for pos in self.maze.get_path():
            self.clock.tick(60)
            self.render_cell(*pos, self.COLOUR_PATH)
            pygame.display.update()

    def epilogue(self):
        while True:
            self.clock.tick(10)
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.QUIT:
                    sys.exit()

    def get_colour(self, value):
        if value not in self.maze.get_values():
            raise GuiError(f"value={value} is invalid")

        if value == Maze.EMPTY:
            return self.COLOUR_EMPTY
        elif value == Maze.WALL:
            return self.COLOUR_WALL
        elif value in [Maze.START, Maze.END]:
            return (0, 255, 0)

    def render_cell(self, x, y, colour):
        pygame.draw.rect(self.win, colour,
                         (x * self.CELL_SIZE, y * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

    def render(self):
        self.win.fill((255, 255, 255))
        for x in range(self.cols):
            for y in range(self.rows):
                value = self.maze.get_cell_type(x, y)
                self.render_cell(x, y, self.get_colour(value))

        pygame.display.update()


if __name__ == "__main__":
    gui = None
    if len(sys.argv) == 3:
        gui = Gui(int(sys.argv[2]), int(sys.argv[1]))
    else:
        gui = Gui(25, 50)
    gui.create_maze()
    gui.run_simulation()
    gui.epilogue()
