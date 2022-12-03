from select import select
# from symbol import dotted_as_name
import turtle
import math
import random
import progressbar as pb
from time import sleep
import copy as cp

NOT_FOUND = -1
INF = 1024
HURISTIC_ONLY_BASED_ON_GAME_OVER = False
SORT_CHECKINGS = True
GUI_SLEEP_TIME = 1

dot_color = 'dark gray'

class State:

    def __init__(self, red :list, blue :list, available_moves :list, turn :str, parent = None) -> None:
        self.red_moves = red
        self.blue_moves = blue
        self.available_moves = available_moves
        self.turn = turn
        self.parent = parent
        self.value = NOT_FOUND
    
    def __lt__(self, other) -> bool:
        return self.cal_huristic() < other.cal_huristic()

    def get_value(self):
        if self.value == NOT_FOUND:
            return self.cal_huristic()
        return self.value

    def _get_number_of_repeative_dots(self, lines):
        dots = []
        for line in lines:
            dots.append(line[0])
            dots.append(line[1])

        return len(dots) - len(list(dict.fromkeys(dots)))

    def cal_huristic(self) -> int:
        if HURISTIC_ONLY_BASED_ON_GAME_OVER:
            h = 200
            g = self._gameover(self.red_moves, self.blue_moves)
            if  g == "blue":
                h -= 50
            elif g == "red":
                h += 50
            self.value = h
            return h

        blue_repeative_dots = self._get_number_of_repeative_dots(self.blue_moves)
        red_repeative_dots = self._get_number_of_repeative_dots(self.red_moves)

        h = (blue_repeative_dots - (6 * red_repeative_dots)) + 1000

        g = self._gameover(self.red_moves, self.blue_moves)
        if  g == "blue":
            h -= 50
        elif g == "red":
            h += 50

        self.value = h
        return h

    def get_successors(self):
        successors = []
        for move in self.available_moves:
            red = cp.deepcopy(self.red_moves)
            blue = cp.deepcopy(self.blue_moves)
            available = cp.deepcopy(self.available_moves)
            available.remove(move)
            if self.turn == "red":
                red.append(move)
                successors.append(State(red, blue, available, "blue", self))
            else:
                blue.append(move)
                successors.append(State(red, blue, available, "red", self))

            # if SORT_CHECKINGS:
            #     successors.sort(reverse = True)

        return successors

    def _gameover(self, r, b):
        if len(r) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        if len(b) < 3: return 0
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0

    def is_over(self) -> bool:
        if self._gameover(self.red_moves, self.blue_moves) != 0:
            return True
        return False
    
class Sim:
    
    GUI = False
    screen = None
    selection = []
    turn = ''
    dots = []
    red = []
    blue = []
    available_moves = []
    minimax_depth = 0
    prune = False

    def __init__(self, minimax_depth, prune, gui) -> None:
        self.GUI = gui
        self.prune = prune
        self.minimax_depth = minimax_depth

        if prune:SORT_CHECKINGS = True
        else: SORT_CHECKINGS = False

        if self.GUI:
            self.setup_screen()

    def setup_screen(self):
        self.screen = turtle.Screen()
        self.screen.setup(800, 800)
        self.screen.title("Game of SIM")
        self.screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
        self.screen.tracer(0, 0)
        turtle.hideturtle()

    def draw_dot(self, x, y, color):
        turtle.up()
        turtle.goto(x, y)
        turtle.color(color)
        turtle.dot(15)

    def gen_dots(self):
        r = []
        for angle in range(0, 360, 60):
            r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
        return r

    def initialize(self):
        self.selection = []
        self.available_moves = []
        for i in range(0, 6):
            for j in range(i, 6):
                if i != j:
                    self.available_moves.append((i, j))
        if random.randint(0, 2) == 1:
            self.turn = 'red'
        else:
            self.turn = 'blue'
        self.dots = self.gen_dots()
        self.red = []
        self.blue = []
        if self.GUI: turtle.clear()
        self.draw()

    def draw_line(self, p1, p2, color):
        turtle.up()
        turtle.pensize(3)
        turtle.goto(p1)
        turtle.down()
        turtle.color(color)
        turtle.goto(p2)

    def draw_board(self):
        for i in range(len(self.dots)):
            if i in self.selection:
                self.draw_dot(self.dots[i][0], self.dots[i][1], self.turn)
            else:
                self.draw_dot(self.dots[i][0], self.dots[i][1], dot_color)

    def draw(self):
        if not self.GUI: return 0
        self.draw_board()
        for i in range(len(self.red)):
            self.draw_line((math.cos(math.radians(self.red[i][0] * 60)), math.sin(math.radians(self.red[i][0] * 60))),
                           (math.cos(math.radians(self.red[i][1] * 60)), math.sin(math.radians(self.red[i][1] * 60))),
                           'red')
        for i in range(len(self.blue)):
            self.draw_line((math.cos(math.radians(self.blue[i][0] * 60)), math.sin(math.radians(self.blue[i][0] * 60))),
                           (math.cos(math.radians(self.blue[i][1] * 60)), math.sin(math.radians(self.blue[i][1] * 60))),
                           'blue')
        self.screen.update()
        sleep(GUI_SLEEP_TIME)
    
    def find_next_best_possible_move(self, depth, player_turn):
        initial_state = State(self.red, self.blue, self.available_moves, "red")
        s = self._max_value(initial_state)
        while s.parent.parent != None:
            s = s.parent

        for move in reversed(s.red_moves):
            if move not in self.red:
                return move

    def _max_value(self, state :State, height = 0 ,alpha = -INF, beta = INF) -> State:
        if height == self.minimax_depth or state.is_over():
            state.cal_huristic()
            return state

        v = -INF;result :State = state;i = 0

        successors = state.get_successors()
        if SORT_CHECKINGS: successors.sort(reverse = True)

        for s in successors:
            i += 1
            candidate = self._min_value(s, height + 1, alpha, beta)
            if v < candidate.get_value() or (v == candidate.get_value() and candidate.cal_huristic() > result.cal_huristic()):
                v = candidate.get_value()
                result = candidate
            if self.prune:
                if v >= beta: return candidate
                alpha = max(alpha, v)

        if i == 0: result.cal_huristic()
        return result        

    def _min_value(self, state :State, height = 0 ,alpha = -INF, beta = INF) -> State:
        if height == self.minimax_depth or state.is_over():
            state.cal_huristic()
            return state

        v = INF;result :State = state;i = 0

        successors = state.get_successors()
        if SORT_CHECKINGS: successors.sort()

        for s in successors:
            i += 1
            candidate = self._max_value(s, height + 1, alpha, beta)
            if v > candidate.get_value() or (v == candidate.get_value() and candidate.cal_huristic() > result.cal_huristic()):
                v = candidate.get_value()
                result = candidate
            if self.prune:
                if v <= alpha: return candidate
                beta = min(beta, v)

        if i == 0: result.cal_huristic()
        return result
    
    def enemy(self):
        return random.choice(self.available_moves)

    def _swap_turn(self, turn):
        if turn == "red": 
            return "blue"
        return "red"

    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                selection = self.find_next_best_possible_move(self.minimax_depth, self.turn)
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            else:
                selection = self.enemy()
                if selection[1] < selection[0]:
                    selection = (selection[1], selection[0])
            if selection in self.red or selection in self.blue:
                raise Exception("Duplicate Move!!!")
            if self.turn == 'red':
                self.red.append(selection)
            else:
                self.blue.append(selection)

            self.available_moves.remove(selection)
            self.turn = self._swap_turn(self.turn)
            self.draw()
            r = self.gameover(self.red, self.blue)
            if r != 0:
                return r

    def gameover(self, r, b):
        if len(r) < 3:
            return 0
        r.sort()
        for i in range(len(r) - 2):
            for j in range(i + 1, len(r) - 1):
                for k in range(j + 1, len(r)):
                    if r[i][0] == r[j][0] and r[i][1] == r[k][0] and r[j][1] == r[k][1]:
                        return 'blue'
        if len(b) < 3: return 0
        b.sort()
        for i in range(len(b) - 2):
            for j in range(i + 1, len(b) - 1):
                for k in range(j + 1, len(b)):
                    if b[i][0] == b[j][0] and b[i][1] == b[k][0] and b[j][1] == b[k][1]:
                        return 'red'
        return 0


if __name__=="__main__":

    minimax_depth = 5
    prune = False
    gui = False
    plays = 20

    game = Sim(minimax_depth, prune, gui)
    results = {"red": 0, "blue": 0}

    print("\033[94m")
    bar = pb.ProgressBar(maxval=plays, widgets=[pb.Bar('=', '[', ']'), ' ', pb.Percentage()])
    bar.start()

    for i in range(plays):
        winner = game.play()
        results[winner] += 1
        dot_color = winner
        bar.update(i)

    bar.finish()
    print(f"\033[0m Result:\n{results}")
    