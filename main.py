import tkinter as tk # библиотека для создания графических интерфейсов.
from tkinter import messagebox # модуль для отображения всплывающих окон с сообщениями
import random 

class Minesweeper:
    def __init__(self, master, width=10, height=10, mines=10, random_after_first_click=True):
        self.master = master
        self.width = width
        self.height = height
        self.mines = mines
        self.random_after_first_click = random_after_first_click

        self.buttons = {} #словарь для хранения кнопок
        self.revealed = set()#множество для хранения открытых ячеек.
        self.flags = set() #множество для хранения ячеек с флагами.
        self.mine_positions = set() #ножество для хранения позиций мин.
        self.first_click = True #флаг для отслеживания первого клика.

        self.create_widgets() #для создания интерфейса.

    def create_widgets(self):
        for y in range(self.height):
            for x in range(self.width):
                button = tk.Button(
                    self.master,
                    width=2,
                    height=1,
                    command=lambda x=x, y=y: self.reveal(x, y)
                )
                button.bind('<Button-3>', lambda event, x=x, y=y: self.toggle_flag(x, y))
                button.grid(row=y, column=x)
                self.buttons[(x, y)] = button

    def place_mines(self, first_click_x=None, first_click_y=None): #случайным образом размещает мины на поле, избегая позиции первого клика.
        while len(self.mine_positions) < self.mines:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if (x, y) != (first_click_x, first_click_y):
                self.mine_positions.add((x, y))

    def reveal(self, x, y): #oткрытие ячейки
        if self.first_click and self.random_after_first_click: #eсли это первый клик, размещает мины.
            self.place_mines(x, y)
            self.first_click = False

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

    def expose(self, x, y): #открывает ячейку и отображает количество соседних мин.
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

    def toggle_flag(self, x, y): #устанавливает или убирает флаг на ячейке.
        if (x, y) in self.revealed:
            return

        if (x, y) in self.flags:
            self.buttons[(x, y)]['text'] = ''
            self.flags.remove((x, y))
        else:
            self.buttons[(x, y)]['text'] = '¶'
            self.flags.add((x, y))

    def count_adjacent_mines(self, x, y):
        return sum((nx, ny) in self.mine_positions 
                   for nx in range(x-1, x+2) 
                   for ny in range(y-1, y+2) 
                   if self.in_bounds(nx, ny))

    def in_bounds(self, x, y): # проверка границ поля
        return 0 <= x < self.width and 0 <= y < self.height

    def game_over(self, won):
        for (x, y) in self.mine_positions:
            self.buttons[(x, y)]['text'] = '*'
            self.buttons[(x, y)]['bg'] = 'red'

        found_mines = len(self.flags & self.mine_positions)
        msg = ("Вы выиграли! Вы нашли мин: {} из {}."
               .format(found_mines, self.mines)
               if won else 
               "Вы проиграли! Вы нашли мин: {} из {}."
               .format(found_mines, self.mines))
        
        messagebox.showinfo("Игра окончена", msg)
        self.master.after(2000, self.master.quit)

def start_game(width, height, mines, random_after_first_click):
    root = tk.Tk()
    root.title("Minesweeper")
    app = Minesweeper(root, width, height, mines, random_after_first_click)
    root.mainloop()

def main_menu():
    # менюшка 
    menu_root = tk.Tk()
    menu_root.title("Сапер - Меню")

    tk.Label(menu_root, text="Выберите размер сетки и количество мин").pack(pady=10)

    tk.Label(menu_root, text="Ширина:").pack()
    width_entry = tk.Entry(menu_root)
    width_entry.pack()
    width_entry.insert(0, '10')

    tk.Label(menu_root, text="Высота:").pack()
    height_entry = tk.Entry(menu_root)
    height_entry.pack()
    height_entry.insert(0, '10')

    tk.Label(menu_root, text="Мина:").pack()
    mines_entry = tk.Entry(menu_root)
    mines_entry.pack()
    mines_entry.insert(0, '10')

    random_check = tk.BooleanVar()
    random_check.set(True)

    def start_from_menu():
        width = int(width_entry.get())
        height = int(height_entry.get())
        mines = int(mines_entry.get())
        random_after_first_click = random_check.get()
        menu_root.destroy()
        start_game(width, height, mines, random_after_first_click)

    start_button = tk.Button(menu_root, text="Начать", command=start_from_menu)
    start_button.pack(pady=20)

    menu_root.mainloop()

if __name__ == "__main__":
    main_menu()
