import pygame, time, math, cProfile, operator
from pygame import gfxdraw
from random import randint


class Game:
    def __init__(self, n):
        self.n = n
        self.size = 41
        self.info_width = 200
        self.width = n * self.size + 1 + self.info_width
        self.height = n * self.size + 1
        self.block_size = self.size - 1
        self.window = pygame.display.set_mode((self.width, self.height))
        self.move = 0
        self.leaves = 0
        self.color_p_1 = (50, 50, 255)
        self.color_p_2 = (255, 25, 25)
        self.board = []
        for col in range(0, n):
            self.board.append([])
            for row in range(0, n):
                self.board[col].append(0)
        self.points_1 = 0
        self.points_2 = 0

    def print_state(self):
        for row in range(0, self.n):
            row_to_prnt = []
            for col in range(0, self.n):
                row_to_prnt.append(self.board[col][row])
            print(row_to_prnt)
        print()

    def print_board(self):
        background_color = (0, 0, 0)
        self.window.fill(background_color)
        for x in range(n):
            for y in range(n):
                rect = pygame.Rect(x * (self.block_size + 1) + 1, y * (self.block_size + 1) + 1, self.block_size, self.block_size)
                pygame.draw.rect(self.window, (255, 255, 255), rect)

        self.print_points()
        pygame.gfxdraw.filled_circle(self.window, (n + 4) * (self.block_size + 1) - 20, 21, 16, (50, 50, 255))
        pygame.gfxdraw.aacircle(self.window, (n + 4) * (self.block_size + 1) - 20, 21, 16, (0, 0, 0))

        pygame.display.flip()

    def do_move(self, x, y):
        if x < self.n and y < self.n and self.board[x][y] == 0:
            if self.move % 2 == 0:
                color = self.color_p_1
                next = self.color_p_2
                self.board[x][y] = 1
                points = self.calculate_points(x, y)
                self.points_1 += points
                self.print_points()
            else:
                color = self.color_p_2
                next = self.color_p_1
                self.board[x][y] = 2
                points = self.calculate_points(x, y)
                self.points_2 += points
                self.print_points()

            pygame.gfxdraw.filled_circle(self.window, (x + 1) * (self.block_size + 1) - 20, (y + 1) * (self.block_size + 1) - 20, 16, color)
            pygame.gfxdraw.aacircle(self.window, (x + 1) * (self.block_size + 1) - 20, (y + 1) * (self.block_size + 1) - 20, 16, (0, 0, 0))
            pygame.gfxdraw.filled_circle(self.window, (n + 4) * (self.block_size + 1) - 20, 21, 16, next)
            pygame.gfxdraw.aacircle(self.window, (n + 4) * (self.block_size + 1) - 20, 21, 16, (0, 0, 0))

            pygame.display.update()
            self.move += 1

        self.print_state()

    def calculate_points(self, x, y):
        row = self.n
        col = self.n
        diar = 1
        dial = 1
        diar_size = 0
        dial_size = 0
        for i in range(0, self.n):
            for j in range (0, self.n):
                if i == x and j != y: # kolumna
                    if self.board[i][j] == 0:
                        row = 0
                if j == y and i != x: # wiersz
                    if self.board[i][j] == 0:
                        col = 0
                if i - j == x - y: # przekatna prawo
                    diar_size += 1
                    if self.board[i][j] == 0 and (i != x or j != y):
                        diar = 0
                if j + i == y + x: # przekatna lewo
                    dial_size += 1
                    if self.board[i][j] == 0 and (i != x or j != y):
                        dial = 0
                if row == 0 and col == 0 and diar == 0 and dial == 0:
                    return 0

        if diar == 0 or diar_size == 1:
            diar_size = 0
        if dial == 0 or dial_size == 1:
            dial_size = 0

        points = row + col + diar_size + dial_size
        return points

    def print_points(self):
        rect = pygame.Rect(n * (self.block_size + 1) + 1, 0, self.info_width, self.height - 1)  # info
        pygame.draw.rect(self.window, (255, 255, 255), rect)
        pygame.font.init()
        myfont = pygame.font.SysFont('Calibri', 16, True)
        text_next_move = myfont.render('Następny ruch:', False, (0, 0, 0))
        self.window.blit(text_next_move, (n * (self.block_size + 1) + 12, 8))
        text_score_1 = myfont.render('Niebieski:   ' + str(self.points_1), False, (0, 0, 0))
        self.window.blit(text_score_1, (n * (self.block_size + 1) + 12, 50))
        text_score_2 = myfont.render('Czerwony:  ' + str(self.points_2), False, (0, 0, 0))
        self.window.blit(text_score_2, (n * (self.block_size + 1) + 12, 84))

    def calculate_state_score(self):
        points = 0
        for col in range(0, self.n):
            for row in range(0, self.n):
                if self.board[col][row] == 0:
                    if points < self.calculate_points(col, row):
                        points = self.calculate_points(col, row)
        return points

    def min(self):
        min_moves = []
        lowest_score = self.n*self.n*self.n
        for col in range(0, self.n):
            for row in range(0, self.n):
                if self.board[col][row] == 0:
                    self.board[col][row] = 3
                    score_after = self.calculate_state_score()
                    if score_after == lowest_score:
                        min_moves.append((col, row))
                    if score_after < lowest_score:
                        min_moves.clear()
                        min_moves.append((col, row))
                        lowest_score = score_after

                    self.board[col][row] = 0
        return min_moves

    def possible_moves(self):
        for col in range(0, self.n):
            for row in range(0, self.n):
                if self.board[col][row] == 0:
                    return True
        return False

    def max(self):
        moves = self.min()
        score = 0
        best_move = moves[0]
        for move in moves:
            x, y = move
            if self.calculate_points(x, y) > score:
                score = self.calculate_points(x, y)
                best_move = (x, y)
        return best_move

    def minimax_decision(self, depth):
        move = (n, n)
        value = -math.inf
        for col in range(0, self.n):
            for row in range(0, self.n):
                if self.board[col][row] == 0:
                    self.board[col][row] = 3
                    new_val = self.minimax(depth - 1, False, self.calculate_points(col, row), 0)
                    if new_val > value:
                        value = new_val
                        move = (col, row)
                    self.board[col][row] = 0
        return move

    def minimax(self, depth, maximizing_player, points_1, points_2):
        if depth == 0 or not self.possible_moves():
            self.leaves += 1;
            return points_1 - points_2
        if maximizing_player:
            value = -math.inf
            for col in range(0, self.n):
                for row in range(0, self.n):
                    if self.board[col][row] == 0:
                        self.board[col][row] = 5
                        value = max(value, self.minimax(depth - 1, False, points_1 + self.calculate_points(col, row), points_2))
                        self.board[col][row] = 0

            return value
        else:
            value = math.inf
            for col in range(0, self.n):
                for row in range(0, self.n):
                    if self.board[col][row] == 0:
                        self.board[col][row] = 4
                        value = min(value, self.minimax(depth - 1, True, points_1, points_2 + self.calculate_points(col, row)))
                        self.board[col][row] = 0

            return value

    def get_possible_moves(self):
        moves = []
        for col in range(0, self.n):
            for row in range(0, self.n):
                if self.board[col][row] == 0:
                    moves.append([0, (col, row)])
        return moves

    def score_moves_filled_on_stretches(self, moves):
        for move in moves:
            move[0] = self.score_move_filled_on_stretches(move[1])
        return moves

    def score_move_filled_on_stretches(self, move):
        x, y = move
        row = 0
        col = 0
        diar = 0
        dial = 0
        for i in range(0, self.n):
            for j in range (0, self.n):
                if i == x and j != y: # wiersz
                    if self.board[i][j] != 0:
                        row += 1
                if j == y and i != x: # kolumna
                    if self.board[i][j] != 0:
                        col += 1
                if i - j == x - y: # przekatna prawo
                    if self.board[i][j] != 0 and (i != x or j != y):
                        diar += 1
                if j + i == y + x: # przekatna lewo
                    if self.board[i][j] != 0 and (i != x or j != y):
                        dial += 1
        score = row + col + diar + dial
        return score

    def score_moves_filled_neighbours(self, moves):
        for move in moves:
            move[0] = self.score_move_filled_neighbours(move[1])
        return moves

    def score_move_filled_neighbours(self, move):
        x, y = move
        neighbours = 0
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i > -1 and i < self.n and j > -1 and j < self.n:
                    if self.board[i][j] != 0:
                        neighbours += 1
        score = neighbours
        return score

    def sort_moves(self, moves):
        moves.sort(key=operator.itemgetter(0), reverse=True)
        return moves

    def minimax_alphabeta_decision(self, depth):
        optimal_move = (n, n)
        value = -math.inf
        moves = self.get_possible_moves()
        moves = self.score_moves_filled_neighbours(moves)
        moves = self.sort_moves(moves)
        for move in moves:
            col, row = move[1]
            self.board[col][row] = 3
            new_val = self.minimax_alphabeta(depth - 1, False, self.calculate_points(col, row), 0, value, math.inf)
            if new_val > value:
                value = new_val
                optimal_move = (col, row)
            self.board[col][row] = 0
        return optimal_move#s[nr]

    def minimax_alphabeta(self, depth, maximizing_player, points_1, points_2, alpha, beta):
        if depth == 0 or not self.possible_moves():
            self.leaves +=1;
            return points_1 - points_2
        if maximizing_player:
            value = -math.inf
            moves = self.get_possible_moves()
            moves = self.score_moves_filled_neighbours(moves)
            moves = self.sort_moves(moves)
            for move in moves:
                col, row = move[1]
                self.board[col][row] = 5
                value = max(value, self.minimax_alphabeta(depth - 1, False, points_1 + self.calculate_points(col, row), points_2, alpha, beta))
                self.board[col][row] = 0
                alpha = max(alpha, value)
                if beta <= alpha:
                    return beta
            return alpha
        else:
            value = math.inf
            moves = self.get_possible_moves()
            moves = self.score_moves_filled_neighbours(moves)
            moves = self.sort_moves(moves)
            for move in moves:
                col, row = move[1]
                self.board[col][row] = 4
                value = min(value, self.minimax_alphabeta(depth - 1, True, points_1, points_2 + self.calculate_points(col, row), alpha, beta))
                self.board[col][row] = 0
                beta = min(beta, value)
                if beta <= alpha:
                    return alpha
            return beta


def game(n):
    game = Game(n)
    game.print_board()

    running = True
    while running:
        if game.possible_moves() and game.move % 2 == 0:
            time.sleep(0)
            coords = game.minimax_decision(4)
            #coords = game.minimax_alphabeta_decision(1)
            x, y = coords
            game.do_move(x, y)
        elif game.possible_moves() and game.move % 2 == 1:
            time.sleep(0)
            coords = game.minimax_decision(4)
            #coords = game.minimax_alphabeta_decision(1)
            x, y = coords
            game.do_move(x, y)
        elif game.possible_moves() and game.move % 2 == 3:
            move = game.max()
            x, y = move
            game.do_move(x, y)
        else:
            running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    x = mx // 41
                    y = my // 41
                    game.do_move(x, y)


if __name__ == "__main__":
    n = 5

    # cProfile.run('game(n)', sort='tottime')
    game(n)
