#This is the main
import pygame
import random 
import sys
SIZE = 100
pygame.init()

# Konstanten
WIDTH, HEIGHT = 800, 600
FPS_UPDATE = 60
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
BLACK = (0,0,0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game_of_life")
clock = pygame.time.Clock()

class View:
    def __init__(self):
        self.pos_x=0
        self.pos_y=0
        self.zoom=20 # size of squares
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
    def get_zoom(self):
        return self.zoom
    def get_x(self):
        return self.pos_x
    def get_y(self):
        return self.pos_y

class Game:
    def __init__(self,n):
        self.board = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        self.n = n
        self.s = 5
    def print(self):
        print(self.board)
    def size(self):
        return self.n
    def speed(self):
        return self.s
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

def draw_elements(v: View,board: Game):
    """Hier passiert alles, was mit der Grafik zu tun hat."""
    # Hintergrund füllen (löscht das Bild vom vorherigen Frame)
    screen.fill(BLACK)
    size = v.get_zoom()
    posx = v.get_x()
    posy = v.get_y()
    startindex_x= int(posx/size)
    startindex_y= int(posy/size)
    endindex_x= startindex_x+int(WIDTH/size) +2
    endindex_y= startindex_y+int(HEIGHT/size) +2

    for i in range(startindex_x, endindex_x+1):
        for y in range(startindex_y, endindex_y+1):
            if i>=0 and y>=0 and i<(board.size()) and y<(board.size()) and board.get_board()[i][y]==1:
                pygame.draw.rect(screen, WHITE, (i*size-posx, y*size-posy, size, size))



    # Ein einfaches Rechteck zeichnen
    # Syntax: pygame.draw.rect(Oberfläche, Farbe, (x, y, breite, höhe))
    #pygame.draw.rect(screen, BLUE, (-25, HEIGHT//2 - 25, 50, 50))
    
    # Das Gezeichnete auf dem Bildschirm sichtbar machen
    pygame.display.flip()



def main():
    game = Game(SIZE)
    viewer = View()
    running = True
    counter = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            viewer.move_up()
        if keys[pygame.K_s]:
            viewer.move_down()
        if keys[pygame.K_a]:
            viewer.move_left()
        if keys[pygame.K_d]:
            viewer.move_right()
        counter+=1
        if(counter/FPS_UPDATE ==game.speed()):
            counter=0
            game.tick()
        draw_elements(viewer,game)
        clock.tick(FPS_UPDATE)


    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()