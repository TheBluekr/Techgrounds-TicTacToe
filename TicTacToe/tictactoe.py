import copy
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
        for i in range(len(self.board)):
            invalid_board = False
            if(len(self.board) != len(self.board[i])):
                invalid_board = True
                print("Invalid row found on index {0}".format(i+1))
            if(invalid_board):
                print("Board is not squared, returning execution!")
                return
        if(len(self.board) < 3 or len(self.board[0]) < 3):
            print("Invalid board size with dims {0}x{1}, lowest must be 3x3".format(len(self.board), len(self.board[0])))
            return
        
        self.playing = True
        while self.playing:
            self.print_board()
            if(self.check_stalemate()):
                print("Reached stalemate")
                break
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
                    if(self.check_hypothetical_win(self.turn, i)): # Check own win first
                        number = i
                        break
                    if(self.check_hypothetical_win(0, i)): # Check for possible loss
                        number = i
                        break
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
        win = False
        if(self.check_horizontal()):
            win = True
        if(self.check_vertical()):
            win = True
        if(self.check_diagonal()):
            win = True
        return win
    
    def check_stalemate(self):
        stalemate = True
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                try:
                    int(self.board[y][x]) # Assuming there's no numbers left execution won't pass
                    stalemate = False
                except ValueError:
                    pass
        return stalemate
    
    def check_hypothetical_win(self, player=0, position=0):
        hypothetical_board = copy.deepcopy(self.board)
        edgelength = len(hypothetical_board)
        x = position // edgelength
        y = position % edgelength
        if(hypothetical_board[x][y] in self.players):
            return False # Invalid index, ignore this position
        hypothetical_board[x][y] = self.players[player]
        win = False
        if(self.check_horizontal(hypothetical_board)):
            win = True
        if(self.check_vertical(hypothetical_board)):
            win = True
        if(self.check_diagonal(hypothetical_board)):
            win = True
        return win

    def check_horizontal(self, board=None):
        if(not board):
            board = self.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                try:
                    if(board[i][j] == board[i][j+1] == board[i][j+2]):
                        return True
                except IndexError:
                    pass
        return False
    
    def check_vertical(self, board=None):
        if(not board):
            board = self.board
        for j in range(len(board[0])):
            for i in range(len(board)-2):
                if(board[i][j] == board[i+1][j] == board[i+2][j]):
                    return True
        return False
    
    def check_diagonal(self, board=None):
        if(not board):
            board = self.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                try:
                    if(board[i][j] == board[i+1][j+1] == board[i+2][j+2]):
                        return True
                    if(board[i][j+2] == board[i+1][j+1] == board[i+2][j]):
                        return True
                except IndexError:
                    pass
        return False

print("")
game = Board(True)
game.play()