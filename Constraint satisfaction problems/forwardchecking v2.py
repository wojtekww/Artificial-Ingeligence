import cProfile, pygame, time


class Variable:
    def __init__(self, n):
        self.v = 0
        self.d = list(range(1, n + 1))
        self.n = n

    def reset_d(self):
        self.d = list(range(1, self.n + 1))

    def __repr__(self):
        return str(self.v)+" "+str(self.d)


class Board:
    def __init__(self, n):
        self.variables = []
        for i in range(0, n):
            self.variables.append(Variable(n))
        self.n = n
        self.final_sum = n * (n + 1) / 2
        self.solutions = 0
        self.calls = 0
        self.returns = 0

    def print_board(self):
        for v in self.variables:
            row = ""
            for j in range(0, v.v - 1):
                row += "0 "
            if v.v != 0:
                row += "H "
            for j in range(v.v, self.n):
                row += "0 "
            print(row)
        print("")

    def print_nicely(self):
        size = 40
        if self.n > 20:
            size = 20
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
                rect = pygame.Rect((self.variables[v].v - 1) * (block_size + 1) + 1, v * (block_size + 1) + 1, block_size, block_size)
                pygame.draw.rect(window, (100, 100, 200), rect)
        pygame.display.flip()

        if(self.n < 8):
            time.sleep(0.3)
        if(self.n < 6):
            time.sleep(0.3)

    def reset(self):
        self.__init__(self.n)

    def place_queen(self, v, di):
        v -= 1
        self.variables[v].v = di
        self.variables[v].d = []
        # self.calculate_domains()
        for vi in range(0, self.n):
            if v != vi:
                to_remove = []
                to_remove.append(di)
                for dj in range(0, len(self.variables[vi].d)):
                    if vi == v + (di - self.variables[vi].d[dj]):
                        to_remove.append(self.variables[vi].d[dj])
                    if vi == v - (di - self.variables[vi].d[dj]):
                        to_remove.append(self.variables[vi].d[dj])
                self.variables[vi].d = [v for v in self.variables[vi].d if v not in to_remove]

    def remove_queen(self, v):
        self.variables[v - 1].v = 0
        self.reset_domains()
        self.calculate_domains()

    def reset_domains(self):
        for v in self.variables:
            v.reset_d()

    def calculate_domains(self):
        for v in range(0, self.n):
            if self.variables[v].v != 0:
                self.variables[v].d = []
                di = self.variables[v].v
                for vi in range(0, self.n):
                    if v != vi:
                        to_remove = []
                        to_remove.append(di)
                        for dj in range(0, len(self.variables[vi].d)):
                            if vi == v + (di - self.variables[vi].d[dj]):
                                to_remove.append(self.variables[vi].d[dj])
                            if vi == v - (di - self.variables[vi].d[dj]):
                                to_remove.append(self.variables[vi].d[dj])
                        self.variables[vi].d = [v for v in self.variables[vi].d if v not in to_remove]

    def find_solution(self):
        self.calls += 1
        for v in range(0, self.n):
            if self.variables[v].v == 0 and len(self.variables[v].d) == 0:
                return False
            if len(self.variables[v].d) > 0:
                for di in range(1, self.n + 1):
                    if di in self.variables[v].d:
                        self.place_queen(v + 1, di)
                        #self.print_nicely()
                        sum = 0
                        for vi in self.variables:
                            sum += vi.v
                        if sum == self.final_sum:
                            self.solutions += 1
                            return True
                        else:
                            if self.find_solution():
                                return True
                            else:
                                self.remove_queen(v + 1)
                                #self.print_nicely()
                                self.returns += 1
                return False

    def find_all_solutions(self):
        self.calls += 1
        for v in range(0, self.n):
            if self.variables[v].v == 0 and len(self.variables[v].d) == 0:
                return False
            if len(self.variables[v].d) > 0:
                for di in range(1, self.n + 1):
                    if di in self.variables[v].d:
                        self.place_queen(v + 1, di)
                        sum = 0
                        for vi in self.variables:
                            sum += vi.v
                        if sum == self.final_sum:
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

    def find_solution_smallest_domain_first(self):
        self.calls += 1
        smallest_domain = 0
        for v in range(0, self.n):
            if self.variables[v].v == 0:
                smallest_domain = v
                break

        for v in range(0, self.n):
            if self.variables[v].v == 0 and len(self.variables[smallest_domain].d) > len(self.variables[v].d):
                smallest_domain = v

        v = smallest_domain
        for di in range(1, self.n + 1):
            if di in self.variables[v].d:
                self.place_queen(v + 1, di)
                self.print_nicely()
                sum = 0
                for vi in self.variables:
                    sum += vi.v
                if sum == self.final_sum:
                    self.solutions += 1
                    return True
                else:
                    if self.find_solution_smallest_domain_first():
                        return True
                    else:
                        self.remove_queen(v + 1)
                        self.print_nicely()
                        self.returns += 1
        return False

    def find_all_solutions_smallest_domain_first(self):
        self.calls += 1
        smallest_domain = 0
        for v in range(0, self.n):
            if self.variables[v].v == 0:
                smallest_domain = v
                break

        for v in range(0, self.n):
            if self.variables[v].v == 0 and len(self.variables[smallest_domain].d) > len(self.variables[v].d):
                smallest_domain = v

        v = smallest_domain
        for di in range(1, self.n + 1):
            if di in self.variables[v].d:
                self.place_queen(v + 1, di)
                sum = 0
                for vi in self.variables:
                    sum += vi.v
                if sum == self.final_sum:
                    self.solutions += 1
                    #self.print_nicely()
                    self.remove_queen(v + 1)
                    return False
                else:
                    if self.find_all_solutions_smallest_domain_first():
                        return True
                    else:
                        self.remove_queen(v + 1)
                        self.returns += 1
        return False

    def find_solution_least_constraining_value_first(self):
        self.calls += 1
        number_of_variables = []
        for i in range(0, self.n):
            number_of_variables.append(0)

        for v in range(0, self.n):
            if self.variables[v].v == 0:
                for i in range(0, len(self.variables[v].d)):
                    number_of_variables[self.variables[v].d[i] - 1] += 1

        least_constraining_v = self.n + 1

        for i in range(0, len(number_of_variables)):
            if least_constraining_v > number_of_variables[i] != 0:
                least_constraining_v = i

        least_constraining_v += 1

        for v in range(0, self.n):
            if len(self.variables[v].d) > 0:
                di = least_constraining_v
                if di in self.variables[v].d:
                    self.place_queen(v + 1, di)
                    self.print_nicely()
                    sum = 0
                    for vi in self.variables:
                        sum += vi.v
                    if sum == self.final_sum:
                        self.solutions += 1
                        return True
                    else:
                        if self.find_solution_least_constraining_value_first():
                            return True
                        else:
                            self.remove_queen(v + 1)
                            self.print_nicely()
                            self.returns += 1
        return False

    def find_all_solutions_least_constraining_value_first(self):
        self.calls += 1
        number_of_variables = []
        for i in range(0, self.n):
            number_of_variables.append(0)

        for v in range(0, self.n):
            if self.variables[v].v == 0:
                for i in range(0, len(self.variables[v].d)):
                    number_of_variables[self.variables[v].d[i] - 1] += 1

        least_constraining_v = self.n + 1

        for i in range(0, len(number_of_variables)):
            if least_constraining_v > number_of_variables[i] != 0:
                least_constraining_v = i

        least_constraining_v += 1

        for v in range(0, self.n):
            if len(self.variables[v].d) > 0:
                di = least_constraining_v
                if di in self.variables[v].d:
                    self.place_queen(v + 1, di)
                    sum = 0
                    for vi in self.variables:
                        sum += vi.v
                    if sum == self.final_sum:
                        self.solutions += 1
                        #self.print_nicely()
                        self.remove_queen(v + 1)
                        return False
                    else:
                        if self.find_all_solutions_least_constraining_value_first():
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
    #b.print_nicely()
    b.print_stats()


def all_solutions(b):
    b.reset()
    b.find_all_solutions()
    b.print_stats()


def first_solution_smallest_domain(b):
    b.reset()
    b.find_solution_smallest_domain_first()
    b.print_nicely()
    b.print_stats()


def all_solutions_smallest_domain(b):
    b.reset()
    b.find_all_solutions_smallest_domain_first()
    b.print_stats()


def first_solution_least_constraining_value(b):
    b.reset()
    b.find_solution_least_constraining_value_first()
    b.print_nicely()
    b.print_stats()


def all_solutions_least_constraining_value(b):
    b.reset()
    b.find_all_solutions_least_constraining_value_first()
    b.print_stats()


if __name__ == "__main__":
    problem_size = 7
    board = Board(problem_size)

    #first_solution(board)
    #all_solutions(board)

    first_solution_smallest_domain(board)
    #all_solutions_smallest_domain(board)
    #first_solution_least_constraining_value(board)
    #all_solutions_least_constraining_value(board)

    #cProfile.run('all_solutions_least_constraining_value(board)', sort='tottime')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False