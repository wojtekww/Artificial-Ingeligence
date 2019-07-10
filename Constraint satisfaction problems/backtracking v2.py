import cProfile, pygame, time


class Board:
    def __init__(self, n):
        self.variables = [0] * n
        self.n = n
        self.final_sum = n*(n+1)/2
        self.solutions = 0
        self.calls = 0
        self.returns = 0

    def print_board(self):
        for v in self.variables:
            row = ""
            for di in range(0, v - 1):
                row += "0 "
            if v != 0:
                row += "H "
            for di in range(v, self.n):
                row += "0 "
            print(row)
        print("")

    def print_nicely(self):
        size = 40
        width = self.n * size + 1
        height = self.n * size + 1
        block_size = size - 1
        window = pygame.display.set_mode((width, height))
        background_color = (0, 0, 0)
        window.fill(background_color)
        for y in range(height):
            for x in range(width):
                rect = pygame.Rect(x * (block_size + 1) + 1, y * (block_size + 1) + 1, block_size, block_size)
                pygame.draw.rect(window, (255, 255, 255), rect)
        for v in range(0, self.n):
            if self.variables[v] != 0:
                rect = pygame.Rect((self.variables[v] - 1) * (block_size + 1) + 1, v * (block_size + 1) + 1, block_size, block_size)
                pygame.draw.rect(window, (100, 100, 200), rect)
        pygame.display.flip()

        if(self.n < 8):
            time.sleep(0.3)
        if(self.n < 6):
            time.sleep(0.3)

    def reset(self):
        self.__init__(self.n)

    def place_queen(self, v, di):
        self.variables[v - 1] = di

    def remove_queen(self, v):
        self.variables[v - 1] = 0

    def find_solution(self):
        self.calls += 1
        for v in range(0, self.n):
            if self.variables[v] == 0:
                for di in range(1, self.n + 1):
                    flag = 1
                    for vi in range(0, self.n):
                        if di == self.variables[vi] \
                                or (self.variables[vi] != 0 and di == self.variables[vi] - (vi - v)) \
                                or (self.variables[vi] != 0 and di == self.variables[vi] + (vi - v)):
                            flag = 0
                    if flag == 0:
                        self.returns += 1
                    if flag == 1:
                        self.place_queen(v + 1, di)
                        self.print_nicely()
                        if sum(self.variables) == self.final_sum:
                            self.solutions += 1
                            return True
                        else:
                            if self.find_solution():
                                return True
                            else:
                                self.remove_queen(v + 1)
                                self.print_nicely()
                                self.returns += 1
                return False

    def find_all_solutions(self):
        self.calls += 1
        for v in range(0, self.n):
            if self.variables[v] == 0:
                for di in range(1, self.n + 1):
                    flag = 1
                    for vi in range(0, self.n):
                        if di == self.variables[vi] \
                                or (self.variables[vi] != 0 and di == self.variables[vi] - (vi - v)) \
                                or (self.variables[vi] != 0 and di == self.variables[vi] + (vi - v)):
                            flag = 0
                    if flag == 0:
                        self.returns += 1
                    if flag == 1:
                        self.place_queen(v + 1, di)
                        if sum(self.variables) == self.final_sum:
                            self.solutions += 1
                            #self.print_nicely()
                            self.remove_queen(v + 1)
                            return False
                        else:
                            if self.find_all_solutions():
                                return True
                            else:
                                self.remove_queen(v + 1)
                                self.returns += 1
                return False

    def print_stats(self):
        print("Liczba wywołań:   " + str(self.calls))
        print("Liczba powrotów:  " + str(self.returns))
        print("Liczba rozwiązań: " + str(self.solutions))


def first_solution(b):
    b.reset()
    b.find_solution()
    #board.print_nicely()
    board.print_stats()


def all_solutions(b):
    b.reset()
    b.find_all_solutions()
    board.print_stats()


if __name__ == "__main__":

    problem_size = 7
    board = Board(problem_size)

    first_solution(board)
    #all_solutions(board)
    #cProfile.run('first_solution(board)', sort='tottime')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
