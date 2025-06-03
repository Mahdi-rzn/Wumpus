# Wumpus

import random
import tkinter as tk

class Game:
    def __init__(self, size):
        self.size = size
        self.environment, self.wumpus_position = self.create_environment(size)
        self.position = (0, 0)  # Starting position

    def create_environment(self, size):
        environment = [['E' for _ in range(size)] for _ in range(size)]
        wumpus_position = (random.randint(0, size-1), random.randint(0, size-1))
        environment[wumpus_position[0]][wumpus_position[1]] = 'W'

        pit_count = 3
        while pit_count > 0:
            pit_position = (random.randint(0, size-1), random.randint(0, size-1))
            if environment[pit_position[0]][pit_position[1]] == 'E' and pit_position != wumpus_position:
                environment[pit_position[0]][pit_position[1]] = 'P'
                pit_count -= 1

        for i in range(max(0, wumpus_position[0]-1), min(size, wumpus_position[0]+2)):
            for j in range(max(0, wumpus_position[1]-1), min(size, wumpus_position[1]+2)):
                if environment[i][j] == 'E':
                    environment[i][j] = 'S'  # Smell

        return environment, wumpus_position

    def draw_environment(self):
        # Initialize the window
        self.window = tk.Tk()
        self.window.title("Wumpus Game")
        self.canvas = tk.Canvas(self.window, width=300, height=300)
        self.canvas.pack()

        # Draw the grid
        for i in range(self.size):
            for j in range(self.size):
                x1, y1 = j * 60, i * 60
                x2, y2 = x1 + 60, y1 + 60
                if self.environment[i][j] == 'W':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='red')
                elif self.environment[i][j] == 'P':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='brown')
                elif self.environment[i][j] == 'S':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='yellow')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='green')

        # Draw the player position
        self.draw_player()

    def draw_player(self):
        x, y = self.position
        x1, y1 = y * 60 + 10, x * 60 + 10
        x2, y2 = x1 + 40, y1 + 40
        self.canvas.create_oval(x1, y1, x2, y2, fill='blue')

    def move(self, direction):
        x, y = self.position
        if direction == 'up':
            self.position = (max(0, x - 1), y)
        elif direction == 'down':
            self.position = (min(self.size - 1, x + 1), y)
        elif direction == 'left':
            self.position = (x, max(0, y - 1))
        elif direction == 'right':
            self.position = (x, min(self.size - 1, y + 1))
        self.update_display()

    def update_display(self):
        self.canvas.delete("all")
        self.draw_environment()
        self.draw_player()

    def smell(self):
        x, y = self.position
        return (
            (x > 0 and self.environment[x-1][y] == 'W') or
            (x < self.size-1 and self.environment[x+1][y] == 'W') or
            (y > 0 and self.environment[x][y-1] == 'W') or
            (y < self.size-1 and self.environment[x][y+1] == 'W')
        )

    def breeze(self):
        x, y = self.position
        return (
            (x > 0 and self.environment[x-1][y] == 'P') or
            (x < self.size-1 and self.environment[x+1][y] == 'P') or
            (y > 0 and self.environment[x][y-1] == 'P') or
            (y < self.size-1 and self.environment[x][y+1] == 'P')
        )

    def decide_move(self):
        smell_detected = self.smell()
        breeze_detected = self.breeze()

        if smell_detected and breeze_detected:
            print("Danger! Wumpus and multiple pits nearby! Move carefully.")
            self.move('left')
        elif smell_detected:
            print("Wumpus nearby! Move away from it.")
            self.move('down')
        elif breeze_detected:
            print("Multiple pits detected! Move away from them.")
            self.move('up')
        else:
            print("Safe to explore.")
            self.move('right')

    def run(self):
        self.draw_environment()
        self.window.mainloop()

# Example usage
size = 5
game = Game(size)
game.run()