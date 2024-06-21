import random
from enum import Enum
import tkinter as tk
from tkinter import messagebox

class GameStatus(Enum):
    PLAYING = 0
    LOSE = 1
    WIN = 2

class MineBoard(object):

    def __init__(self, w, h, k):
        self.w = w
        self.h = h
        self.board = [[0 for i in range(w)] for j in range(h)]
        self.allocateMines(w, h, k)
        self.status = GameStatus.PLAYING
        self.cellsToOpen = w * h - k

    def allocateMines(self, w, h, numOfMines):
        allocIndexes = self.getRandomPos(w * h, numOfMines)
        for i in allocIndexes:
            self.setMine(int(i / w), i % w)
            self.setAdjacentMines(int(i / w), i % w)

    def click(self, row, col):
        value = self.reveal(row, col)
        if value is not None:
            self.cellsToOpen -= 1
            if self.cellsToOpen == 0:
                self.status = GameStatus.WIN
            if self.hasMine(row, col):
                self.status = GameStatus.LOSE
            elif self.isBlank(row, col):
                for dr in range(row - 1, row + 2):
                    for dc in range(col - 1, col + 2):
                        if self.isValidCell(dr, dc):
                            self.click(dr, dc)

    def flag(self, row, col):
        if self.isValidCell(row, col) and self.isHidden(row, col):
            self.toggleFlag(row, col)

    def isValidCell(self, row, col):
        return row >= 0 and row < self.h and col >= 0 and col < self.w

    def getRandomPos(self, n, k):
        return random.sample(range(n), k)

    def setMine(self, row, col):
        self.board[row][col] = -1

    def setAdjacentMines(self, row, col):
        for dr in range(row - 1, row + 2):
            for dc in range(col - 1, col + 2):
                if self.isValidCell(dr, dc) and not self.hasMine(dr, dc):
                    self.board[dr][dc] += 1

    def toggleFlag(self, row, col):
        if self.isFlagged(row, col):
            self.board[row][col] -= 100
        else:
            self.board[row][col] += 100

    def reveal(self, row, col):
        if not self.isValidCell(row, col) or not self.isHidden(row, col):
            return None
        if self.isFlagged(row, col):
            self.toggleFlag(row, col)
        self.board[row][col] += 10
        return self.board[row][col]

    def isHidden(self, row, col):
        return self.board[row][col] < 9

    def hasMine(self, row, col):
        return self.board[row][col] % 10 == 9

    def isBlank(self, row, col):
        return self.board[row][col] % 10 == 0

    def isOver(self):
        return self.winGame() or self.loseGame()

    def loseGame(self):
        return self.status == GameStatus.LOSE

    def winGame(self):
        return self.status == GameStatus.WIN

    def isFlagged(self, row, col):
        return self.board[row][col] > 90

    def revealAll(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.reveal(i, j)

class MinesweeperGUI:
    def __init__(self, master, width, height, mines):
        self.master = master
        self.master.title("Minesweeper")
        self.width = width
        self.height = height
        self.mines = mines
        self.board = MineBoard(width, height, mines)

        self.buttons = [[None for _ in range(width)] for _ in range(height)]
        self.create_widgets()
        self.update_layout()

    def create_widgets(self):
        for row in range(self.height):
            for col in range(self.width):
                button = tk.Button(self.master, text='', width=3, height=1, command=lambda r=row, c=col: self.on_click(r, c))
                button.bind('<Button-3>', lambda e, r=row, c=col: self.on_right_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def on_click(self, row, col):
        if self.board.isOver():
            return
        self.board.click(row, col)
        self.update_layout()
        if self.board.loseGame():
            messagebox.showinfo("Minesweeper", "You lose!!")
            self.board.revealAll()
            self.update_layout()
        elif self.board.winGame():
            messagebox.showinfo("Minesweeper", "You win!! Congratulations!!")
            self.board.revealAll()
            self.update_layout()

    def on_right_click(self, row, col):
        if self.board.isOver():
            return
        self.board.flag(row, col)
        self.update_layout()

    def update_layout(self):
        for row in range(self.height):
            for col in range(self.width):
                value = self.board.board[row][col]
                if value > 90:
                    self.buttons[row][col].config(text='F', state='disabled')
                elif value == 9:
                    self.buttons[row][col].config(text='*', state='disabled')
                elif value > 10:
                    self.buttons[row][col].config(text=str(value - 10), state='disabled')
                elif value == 10:
                    self.buttons[row][col].config(text='.', state='disabled')
                else:
                    self.buttons[row][col].config(text='', state='normal')

def main():
    root = tk.Tk()
    width = int(input('Enter width of board: '))
    height = int(input('Enter height of board: '))
    mines = int(input('Enter number of mines: '))
    while mines >= width * height - 1:
        mines = int(input('Too many mines. Enter again: '))
    app = MinesweeperGUI(root, width, height, mines)
    root.mainloop()

if __name__ == "__main__":
    main()
