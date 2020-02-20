import copy
import time
import math
import random

class Board:
    def __init__(self, AI_enabled=False):
        self.board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
        self.turn = 0
        self.players = ["X", "O"]
        self.win = False
        self.playing = False
        self.AI = AI_enabled
    
    def play(self):
        for i in range(len(self.board)-1):
            if(len(self.board[0]) != len(self.board[i+1])):
                print("Board is not squared! Invalid row found on index {0}".format(i+1))
                return
        if(len(self.board) < 3 or len(self.board[0]) < 3):
            print("Invalid board size with dims {0}x{1}, lowest must be 3x3".format(len(self.board), len(self.board[0])))
            return
        
        self.playing = True
        while self.playing:
            self.print_board()
            self.print_turn()
            self.await_input()
            if(self.check_win()):
                print("Player {0} won!\n".format(self.players[self.turn]))
                self.print_board()
                break
            self.turn = 1 - self.turn # Flip between 1 and 0
    
    def reinitialize_board(self):
        self.board = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]

    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(" {0} ".format(self.board[i][j]), end="")
                if(j % len(self.board[i]) != len(self.board[i])-1): # Don't draw | at corners
                    print("|", end="")
            print("") # Create newline
            if(i % len(self.board) < len(self.board)-1): # Keep printing ---- lines as long as we don't hit last line
                for j in range(len(self.board[i])*3+2):
                    print("-", end="")
            print("") # Create another newline for style
    
    def print_turn(self):
        pass

    def await_input(self):
        while True:
            if(self.AI and self.turn == 1):
                print("Currently player {0}'s turn\nEnter position: ".format(self.players[self.turn]), end="")
                for i in range(len(self.board)*len(self.board[0])):
                    if(self.check_hypothetical_win(self.turn, i)):
                        number = i
                        break
                    else:
                        number = math.floor(random.uniform(0, len(self.board)*len(self.board[0]))) # Pick a random position if we can't find anything after iterating
                print(number+1)
            else:
                try:
                    number = int(input("Currently player {0}'s turn\nEnter position: ".format(self.players[self.turn])))-1
                except ValueError:
                    print("Invalid input\n")
                    self.print_board()
                    continue
            
            if(number >= len(self.board)*len(self.board[0]) or number < 0):
                print("Index out of range\nMinimum is 1, maximum is {0}".format(len(self.board)*len(self.board[0])))
                self.print_board()
                continue

            edgelength = len(self.board) # We made certain the board should be squared, so calculate the position
            x = number // edgelength
            y = number % edgelength
            if(self.board[x][y] in self.players):
                if(not self.AI):
                    print("Slot is already taken\n")
                    self.print_board()
                continue # Restart the loop
            self.board[x][y] = self.players[self.turn]
            return
    
    def check_win(self):
        self.check_horizontal()
        self.check_vertical()
        self.check_diagonal()
        return self.win
    
    def check_hypothetical_win(self, player=0, position=0):
        hypothetical_board = copy.deepcopy(self.board)
        edgelength = len(hypothetical_board)
        x = position // edgelength
        y = position % edgelength
        if(hypothetical_board[x][y] in self.players):
            return False # Invalid index, ignore this position
        hypothetical_board[x][y] = self.players[self.turn]
        win = False

        for i in range(len(hypothetical_board)): # Horizontal check
            if(hypothetical_board[i][0] == hypothetical_board[i][1] == hypothetical_board[i][2]):
                win = True

        for j in range(len(hypothetical_board[0])): # Vertical check
            for i in range(len(hypothetical_board)-2):
                if(hypothetical_board[i][j] == hypothetical_board[i+1][j] == hypothetical_board[i+2][j]):
                    win = True
    
        for i in range(len(hypothetical_board)):
            for j in range(len(hypothetical_board[i])):
                try:
                    if(hypothetical_board[i][j] == hypothetical_board[i+1][j+1] == hypothetical_board[i+2][j+2]):
                        win = True
                    if(hypothetical_board[i][j+2] == hypothetical_board[i+1][j+1] == hypothetical_board[i+2][j]):
                        win = True
                except IndexError:
                    pass
        
        return win

    def check_horizontal(self):
        for i in range(len(self.board)):
            if(self.board[i][0] == self.board[i][1] == self.board[i][2]):
                self.win = True
    
    def check_vertical(self):
        for j in range(len(self.board[0])):
            for i in range(len(self.board)-2):
                if(self.board[i][j] == self.board[i+1][j] == self.board[i+2][j]):
                    self.win = True
    
    def check_diagonal(self):
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    try:
                        if(self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2]):
                            self.win = True
                        if(self.board[i][j+2] == self.board[i+1][j+1] == self.board[i+2][j]):
                            self.win = True
                    except IndexError:
                        pass

print("")
game = Board(True)
game.play()