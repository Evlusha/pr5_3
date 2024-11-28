import tkinter as tk #создаюtkinter — библиотека для создания графических интерфейсов.
from tkinter import messagebox #messagebox — модуль для отображения всплывающих окон с сообщениями.
import random #random — модуль для генерации случайных чисел, который используется для случайного размещения мин.

class Minesweeper:
    def __init__(self, master, width=10, height=10, mines=10): # дефолтное занчения при открытие окна 
        self.master = master
        self.width = width
        self.height = height
        self.mines = mines
        self.buttons = {}
        self.revealed = set()
        self.flags = set()
        self.mine_positions = set()

        self.create_widgets()
        self.place_mines()

    def create_widgets(self): # создаю виджеты 
        for y in range(self.height):
            for x in range(self.width):
                button = tk.Button(self.master, width=2, height=1, command=lambda x=x, y=y: self.reveal(x, y))
                button.bind('<Button-3>', lambda event, x=x, y=y: self.toggle_flag(x, y))
                button.grid(row=y, column=x)
                self.buttons[(x, y)] = button

    def place_mines(self):
        while len(self.mine_positions) < self.mines:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self.mine_positions.add((x, y))

    def reveal(self, x, y):
        if (x, y) in self.flags:
            return
        if (x, y) in self.mine_positions:
            self.buttons[(x, y)]['text'] = '*'
            self.buttons[(x, y)]['bg'] = 'red'
            self.game_over(False)
        else:
            self.expose(x, y)

        if len(self.revealed) == self.width * self.height - self.mines:
            self.game_over(True)

    def expose(self, x, y):
        if (x, y) in self.revealed or not self.in_bounds(x, y):
            return

        self.revealed.add((x, y))
        adjacent_mines = self.count_adjacent_mines(x, y)

        self.buttons[(x, y)]['text'] = str(adjacent_mines) if adjacent_mines > 0 else ''
        self.buttons[(x, y)]['bg'] = 'grey'

        if adjacent_mines == 0:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx != 0 or dy != 0:
                        self.expose(x + dx, y + dy)

    def toggle_flag(self, x, y):
        if (x, y) in self.revealed:
            return

        if (x, y) in self.flags:
            self.buttons[(x, y)]['text'] = ''
            self.flags.remove((x, y))
        else:
            self.buttons[(x, y)]['text'] = '¶'
            self.flags.add((x, y))

    def count_adjacent_mines(self, x, y):
        return sum((nx, ny) in self.mine_positions for nx in range(x-1, x+2) for ny in range(y-1, y+2) if self.in_bounds(nx, ny))

    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def game_over(self, won):
        for (x, y) in self.mine_positions:
            self.buttons[(x, y)]['text'] = '*'
            self.buttons[(x, y)]['bg'] = 'red'
        message = "Вы просто великолепны! Ты выиграл красавчик!" if won else "Проигрышь! Вы наступили на мину"
        messagebox.showinfo("Game Over", message)
        self.master.after(2000, self.master.quit)

def start_game(width, height, mines):
    root = tk.Tk()
    root.title("Minesweeper")
    app = Minesweeper(root, width, height, mines)
    root.mainloop()

def main_menu():
    menu_root = tk.Tk()
    menu_root.title("Minesweeper - Menu")

    tk.Label(menu_root, text="Choose the grid size and the number of mines").pack(pady=10)
    
    tk.Label(menu_root, text="Width:").pack()
    width_entry = tk.Entry(menu_root)
    width_entry.pack()
    width_entry.insert(0, '10')

    tk.Label(menu_root, text="Height:").pack()
    height_entry = tk.Entry(menu_root)
    height_entry.pack()
    height_entry.insert(0, '10')

    tk.Label(menu_root, text="Mines:").pack()
    mines_entry = tk.Entry(menu_root)
    mines_entry.pack()
    mines_entry.insert(0, '10')

    def start_from_menu():
        width = int(width_entry.get())
        height = int(height_entry.get())
        mines = int(mines_entry.get())
        menu_root.destroy()
        start_game(width, height, mines)

    start_button = tk.Button(menu_root, text="Start Game", command=start_from_menu)
    start_button.pack(pady=20)

    menu_root.mainloop()

if __name__ == "__main__":
    main_menu()
