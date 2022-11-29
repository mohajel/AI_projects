from select import select
# from symbol import dotted_as_name
import turtle
import math
import random
from time import sleep
from sys import argv
import copy as cp

NOT_FOUND = -1

class State:

    def __init__(self, red :list, blue :list, available_moves :list, turn :str, parent = None) -> None:
        self.red_moves = red
        self.blue_moves = blue
        self.avavailable_moves = available_moves
        self.turn = turn
        self.parent = parent
        self.value = NOT_FOUND

    def get_value(self):
        if self.value == NOT_FOUND:
            print("ERROR VALUE NOT FOUND")
        return self.value

    def _get_number_of_repeative_dots(self, lines):
        dots = []
        for line in lines:
            dots.append(line[0])
            dots.append(line[1])

        return len(dots) - len(list(dict.fromkeys(dots)))

    def get_huristic(self) -> int:
        blue_repeative_dots = self._get_number_of_repeative_dots(self.blue)
        red_repeative_dots = self._get_number_of_repeative_dots(self.red)

        self.value = ((blue_repeative_dots - (3 * red_repeative_dots)) + 100)
        return self.value

    def get_successors(self):
        successors = []
        for move in self.available_moves:
            red = cp.deepcopy(self.red_moves)
            blue = cp.deepcopy(self.blue_moves)
            available = cp.deepcopy(self.avavailable_moves)
            available.remove(move)
            if self.turn == "red":
                red.append(move)
                successors.append(State(red, blue, available, "blue", self))
            else:
                blue.append(move)
                successors.append(State(red, blue, available, "red", self))
        return successors

            
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
                self.draw_dot(self.dots[i][0], self.dots[i][1], 'dark gray')

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
        sleep(1)
    
    def find_next_best_possible_move(self, depth, player_turn):
        if self.prune == True:
            return self.alpha_beta_tree(depth, player_turn)
        return self.minimax_tree(depth, player_turn)

    def enemy(self):
        return random.choice(self.available_moves)

    def _swap_turn(turn):
        if turn == "red": 
            return "blue"
        return "red"

    def play(self):
        self.initialize()
        while True:
            if self.turn == 'red':
                selection = self.find_next_best_possible_move(self.minimax_depth, self.turn)#must return a tupel
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
            selection = [] #actually not necessary at all
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

    minimax_depth = 3
    prune = False
    gui = True

    game = Sim(minimax_depth, prune, gui)
    # game = Sim(minimax_depth=int(argv[1]), prune=True, gui=bool(int(argv[2])))

    results = {"red": 0, "blue": 0}
    for i in range(10):
        print(i)
        results[game.play()] += 1
        
    print(results)
    