#This is the main
import pygame
import random 
SIZE = 5


class View:
    def __init__(self):
        self.pos_x=0
        self.pos_y=0
        self.zoom=20
    def move_right(self):
        self.pos_x+=1
    def move_left(self):
        self.pos_x-=1
    def move_up(self):
        self.pos_y-=1
    def move_down(self):
        self.pos_y+=1
    def zoom_in(self):
        self.zoom-=1
    def zoom_out(self):
        self.zoom+=1

class Game:
    def __init__(self,n):
        self.board = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    def print(self):
        print(self.board)
    
    def tick(self):
        n = len(self.board)
        new_board = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(0,len(self.board)):
            for j in range(0,len(self.board)):
                count = self.count_neighbors(i,j)
                if self.board[i][j] == 1 and (count == 2 or count == 3):
                    new_board[i][j] = 1
                elif self.board[i][j] == 0 and count == 3:
                    new_board[i][j] = 1
                else:
                    new_board[i][j] = 0

        self.board = new_board
    def get_board(self):
        return self.board

    def count_neighbors(self,i,y):
        count = 0
        ic = i-1
        yc = y-1
        for _ in range(3):
            for z in range(3):
                if ic>=0 and yc>=0 and ic<len(self.board) and yc<len(self.board) and (ic!=i or yc!=y):
                    count+=self.board[ic][yc]
                yc+=1
            yc-=3
            ic+=1
        return count

def main():
    game = Game(SIZE)

if __name__ == "__main__":
    main()