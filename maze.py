class MazeError(Exception):
    pass

class Maze():

    EMPTY = "empty"
    WALL = "wall"
    START = "start"
    END = "end"

    def __init__(self, width, height):
        self._maze = [[self.EMPTY for _ in range(width)] for _ in range(height)]
        self._width = width
        self._height = height
        self._start_pos = None
        self._end_pos = None
        self._shortest_path = []

    def get_values(self):
        return [self.EMPTY, self.WALL, self.START, self.END]
    
    def get_width(self):
        return self._width
    
    def get_height(self):
        return self._height
    
    def get_start_pos(self):
        return self._start_pos
    
    def get_end_pos(self):
        return self._end_pos
    
    def in_bounds(self, x, y):
        return x in range(self.get_width()) and y in range(self.get_height())

    def set_cell(self, x, y, value):
        
        if not self.in_bounds(x, y):
            raise MazeError(f"x={x} and y={y} is invalid for maze of width={self.get_width()} and height={self.get_height()}")
        if value not in self.get_values():
            raise MazeError(f"value={value} is invalid")
        
        self._maze[y][x] = value

        if (x, y) == self._start_pos:
            self._start_pos = None
        elif (x, y) == self._end_pos:
            self._end_pos = None

        if value == self.START:
            if self._start_pos != None:
                self.set_cell(*self._start_pos, self.EMPTY)
            self._start_pos = (x, y)
        elif value == self.END:
            if self._end_pos != None:
                self.set_cell(*self._end_pos, self.EMPTY)
            self._end_pos = (x, y)

    def get_adjacent_cells(self, x, y):
        cells = []

        for test_y in [y - 1, y + 1]:
            if self.in_bounds(x, test_y):
                cells.append((x, test_y))
        for test_x in [x - 1, x + 1]:
            if self.in_bounds(test_x, y):
                cells.append((test_x, y))

        return cells
    
    def get_cell_type(self, x, y):
        return self._maze[y][x]
    
    def bfs(self):
        visited = {self._start_pos: None}
        queue = [self._start_pos]
        
        while queue:
            x, y = queue.pop(0)
            adjacent_cells = self.get_adjacent_cells(x, y)
            adjacent_cells = list(filter(lambda pos: self.get_cell_type(*pos) != self.WALL, adjacent_cells))
            adjacent_cells = list(filter(lambda pos: pos not in visited, adjacent_cells))
            for cell in adjacent_cells:
                visited[cell] = (x, y)
                queue.append(cell)
            
        
        if self._end_pos in visited:
            self._shortest_path.append(self._end_pos)
            prev = self._end_pos
            while pos := visited[prev]:
                self._shortest_path.append(pos)
                prev = pos
    
    def bfs_iter(self):
        visited = {self._start_pos: None}
        queue = [self._start_pos]
        
        while queue:
            x, y = queue.pop(0)
            adjacent_cells = self.get_adjacent_cells(x, y)
            adjacent_cells = list(filter(lambda pos: self.get_cell_type(*pos) != self.WALL, adjacent_cells))
            adjacent_cells = list(filter(lambda pos: pos not in visited, adjacent_cells))
            
            found_end = False
            for cell in adjacent_cells:
                visited[cell] = (x, y)
                queue.append(cell)
                if cell == self._end_pos:
                    found_end = True
            
            yield (x, y)
            if found_end:
                yield self._end_pos
                break
            
        if self._end_pos in visited:
            self._shortest_path.append(self._end_pos)
            prev = self._end_pos
            while pos := visited[prev]:
                self._shortest_path.append(pos)
                prev = pos

    def print_shortest_path(self):
        path = self._shortest_path[::-1]
        print(path)
    
    def get_path(self):
        return self._shortest_path[::]

    def print_maze(self):
        for row in self._maze:
            for val in row:
                print(f"{val:5} ", end='')
            print()

def main():
    maze = Maze(10, 10)
    maze.print_maze()
    maze.set_cell(5, 5, Maze.WALL)
    maze.set_cell(1, 1, Maze.START)
    maze.set_cell(7, 7, Maze.END)
    maze.set_cell(0, 3, Maze.WALL)
    maze.print_maze()
    for pos in maze.bfs_iter():
        print(pos)

if __name__ == "__main__":
    main()
