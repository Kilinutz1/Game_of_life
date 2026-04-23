#This is the main
import threading
import time
import pygame
import random 
import sys
SIZE = 600
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
ZOOMSPEED = 5


button_start = pygame.Rect(300, 250, 200, 50)
font = pygame.font.SysFont("Arial", 24)
text_surf = font.render("Start Game", True, (0, 0, 0))
text_rect = text_surf.get_rect(center=button_start.center)

button_adjust = pygame.Rect(300, 350, 200, 50)
text_surf_a = font.render("Customize Game", True, (0, 0, 0))
text_rect_a = text_surf_a.get_rect(center=button_adjust.center)
font2 = pygame.font.SysFont("Arial", 15)

button_newrandom = pygame.Rect(WIDTH-80, HEIGHT-120, 50, 50)
text_surf_rand = font2.render("re-gen", True, (0, 0, 0))
text_rect_rand = text_surf_rand.get_rect(center=button_newrandom.center)

button_newboard = pygame.Rect(WIDTH-80, HEIGHT-60, 50, 50)
text_surf_newboard = font2.render("clear", True, (0, 0, 0))
text_rect_newboard = text_surf_newboard.get_rect(center=button_newboard.center)


button_textfield = pygame.Rect(100, 90, 200, 30)




button_inc_speed  = pygame.Rect(10, HEIGHT-50, 30, 30)
button_dec_speed  = pygame.Rect(50, HEIGHT-50, 30, 30)
text_surf_inc_speed = font2.render("+", True, (0, 0, 0))
text_surf_dec_speed = font2.render("-", True, (0, 0, 0))
text_rect_inc_speed = text_surf_inc_speed.get_rect(center=button_inc_speed.center)
text_rect_dec_speed = text_surf_dec_speed.get_rect(center=button_dec_speed.center)

button_inc_dens  = pygame.Rect(10, HEIGHT-90, 30, 30)
button_dec_dens  = pygame.Rect(50, HEIGHT-90, 30, 30)
text_surf_inc_dens = font2.render("+", True, (0, 0, 0))
text_surf_dec_dens = font2.render("-", True, (0, 0, 0))
text_rect_inc_dens = text_surf_inc_dens.get_rect(center=button_inc_dens.center)
text_rect_dec_dens = text_surf_dec_dens.get_rect(center=button_dec_dens.center)

button_save  = pygame.Rect(10, 90, 30, 30)
button_load  = pygame.Rect(50, 90, 30, 30)
text_surf_load = font2.render("load", True, (0, 0, 0))
text_surf_save = font2.render("save", True, (0, 0, 0))
text_rect_save = text_surf_save.get_rect(center=button_save.center)
text_rect_load = text_surf_load.get_rect(center=button_load.center)




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
        self.zoom+=0.2
    def zoom_out(self):
        if self.zoom>1.1:
            self.zoom-=0.2
    def get_zoom(self):
        return self.zoom
    def get_x(self):
        return self.pos_x
    def get_y(self):
        return self.pos_y

class Game:
    def __init__(self,n,v):
        self.board = [[1 if random.randint(0, 15)==10 else 0 for _ in range(n)] for _ in range(n)]
        self.n = n
        self.s = 0.5
        self.nextboard =[[0 for _ in range(n)] for _ in range(n)]
        self.calcing =False
        self.view = v
        self.density = 15
        self.copyboard_to_nextboard()

    def print(self):
        print(self.board)
    def size(self):
        return self.n
    def inc_speed(self):
        if self.s>0.22:
            self.s-=0.05
    def dec_speed(self):
        self.s+=0.05
    def speed(self):
        return self.s
    def reset_rand(self):
        while self.calcing:
            pass
        self.board = [[1 if random.randint(0, self.density)==0 else 0 for _ in range(self.n)] for _ in range(self.n)]
        self.copyboard_to_nextboard()

    def reset(self):
        while self.calcing:
            pass
        self.board =[[0 for _ in range(self.n)] for _ in range(self.n)]
        self.copyboard_to_nextboard()
    def copyboard_to_nextboard(self):
        while(self.calcing):
            pass
        for i in range(self.n):
            for y in range (self.n):
                self.nextboard[i][y]=self.board[i][y]
    
    def increase_density(self):
        if self.density>0:
            self.density-=1
    def decrease_density(self):
        self.density+=1
    def get_density(self):
        return self.density
    def update(self,x,y):
        if(self.board[x][y]==0):
            self.board[x][y]=1
            return
        self.board[x][y]=0
    def tick(self):
        if self.calcing:
            return
        x = self.board
        self.board = self.nextboard
        self.nextboard = x
        self.calcing = True
        thread = threading.Thread(target=self.calc_nextboard,daemon=True)
        thread.start()
        
    def calc_nextboard(self):
        for i in range(0,len(self.board)):
            for j in range(0,self.n):
                count = self.count_neighbors(i,j)
                if self.board[i][j] == 1 and (count == 2 or count == 3):
                    self.nextboard[i][j] = 1
                elif self.board[i][j] == 0 and count == 3:
                    self.nextboard[i][j] = 1
                else:
                    self.nextboard[i][j] = 0
        self.calcing = False
        
    def save_board(self,name):
        try:
            with open(name, "w", encoding="utf-8") as f:
                o = ""+str(self.n)+"\n"
                for i in range(self.n):
                    for y in range(self.n):
                        o= o+str(self.board[i][y])
                    o=o+"\n"
                f.write(o)
        except:
            pass
    def load_board(self,name):
        try:
            with open(name, "r", encoding="utf-8") as file:
                content = file.read()
        except:
            return
        lines = content.split("\n")
        length = int(lines[0])
        b = [[0 for _ in range(length)] for _ in range(length)]          

        for i in range (length):
            line=lines[1+i]
            if len(line)!=length:
                return
            for y in range (length):
                if(line[y]==0 or [y==1]):
                    b[i][y] = int(line[y])                    
                else:
                    return
            
        self.board=b
        self.copyboard_to_nextboard()
        

        
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
    # """Hier passiert alles, was mit der Grafik zu tun hat."""
    # # Hintergrund füllen (löscht das Bild vom vorherigen Frame)
    screen.fill(BLACK)
    size = v.get_zoom()
    posx = v.get_x()
    posy = v.get_y()
    startindex_x= max(0,int(posx/size))
    startindex_y= max(0,int(posy/size))
    endindex_x= min(startindex_x+int(WIDTH/size) +2,board.size()-1)
    endindex_y= min(startindex_y+int(HEIGHT/size) +2,board.size()-1)

    for i in range(startindex_x, endindex_x+1):
        for y in range(startindex_y, endindex_y+1):
            if i>=0 and y>=0 and i<(board.size()) and y<(board.size()) and board.get_board()[i][y]==1:
                pygame.draw.rect(screen, WHITE, (i*size-posx, y*size-posy, size, size))



    # Ein einfaches Rechteck zeichnen
    # Syntax: pygame.draw.rect(Oberfläche, Farbe, (x, y, breite, höhe))
    #pygame.draw.rect(screen, BLUE, (-25, HEIGHT//2 - 25, 50, 50))
    
    # Das Gezeichnete auf dem Bildschirm sichtbar machen
    pygame.display.flip()


def draw_main_menu(g: Game,text: str):
    text_surf_current_speed = font2.render(f"Speed: {round(g.speed(), 2)}", True,BLUE)
    text_surf_current_dens = font2.render(f"Density: {g.get_density()}", True, BLUE)

    screen.fill(BLACK)
    pygame.draw.rect(screen, (BLUE), button_start, border_radius=12)
    screen.blit(text_surf, text_rect)
    pygame.draw.rect(screen, (BLUE), button_adjust, border_radius=12)
    screen.blit(text_surf_a, text_rect_a)

    pygame.draw.rect(screen, (BLUE), button_newboard, border_radius=12)
    screen.blit(text_surf_newboard, text_rect_newboard)
    pygame.draw.rect(screen, (BLUE), button_newrandom, border_radius=12)
    screen.blit(text_surf_rand, text_rect_rand)

    pygame.draw.rect(screen, (BLUE), button_inc_speed, border_radius=12)
    screen.blit(text_surf_inc_speed, text_rect_inc_speed)
    pygame.draw.rect(screen, (BLUE), button_dec_speed, border_radius=12)
    screen.blit(text_surf_dec_speed, text_rect_dec_speed)

    pygame.draw.rect(screen, (BLUE), button_inc_dens, border_radius=12)
    screen.blit(text_surf_inc_dens, text_rect_inc_dens)
    pygame.draw.rect(screen, (BLUE), button_dec_dens, border_radius=12)
    screen.blit(text_surf_dec_dens, text_rect_dec_dens)
    screen.blit(text_surf_current_dens, (100, HEIGHT-85))
    screen.blit(text_surf_current_speed, (100, HEIGHT-45))

    pygame.draw.rect(screen, (BLUE), button_load, border_radius=12)
    screen.blit(text_surf_load, text_rect_load)
    pygame.draw.rect(screen, (BLUE), button_save, border_radius=12)
    screen.blit(text_surf_save, text_rect_save)

    text_surf_textfield = font2.render(text, True, (0, 0, 0))
    text_rect_textfield = text_surf_textfield.get_rect(center=button_textfield.center)
    pygame.draw.rect(screen, (BLUE), button_textfield, border_radius=12)
    screen.blit(text_surf_textfield, text_rect_textfield)

    pygame.display.flip()



def main():
    viewer = View()

    game = Game(SIZE,viewer)
    running = True
    counter = 0
    simulating = True
    changes = True
    zoomincounter=0
    zoomoutcounter=0
    mode = 1
    text = "Input here"
    while running:
        
        if mode == 0:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        simulating = not simulating
                    
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                viewer.move_up()
                changes = True
            if keys[pygame.K_s]:
                viewer.move_down()
                changes = True

            if keys[pygame.K_a]:
                viewer.move_left()
                changes = True

            if keys[pygame.K_d]:
                
                viewer.move_right()
                changes = True

            if keys[pygame.K_r]:
                zoomincounter +=1
                if zoomincounter>= ZOOMSPEED:
                    viewer.zoom_in()
                    changes = True
                    zoomincounter = 0

            if keys[pygame.K_t]:
                zoomoutcounter+=1
                if zoomoutcounter>=ZOOMSPEED:
                    viewer.zoom_out()    
                    changes = True
                    zoomoutcounter = 0
            if keys[pygame.K_ESCAPE]:
                mode = 1
                simulating = True
                continue

            counter+=1
            if(counter/FPS_UPDATE >game.speed()):
                counter=0
                if simulating:
                    game.tick()
                    changes = True
            if changes: 
                draw_elements(viewer,game)
            changes =False

        elif mode == 1:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_start.collidepoint(event.pos):
                        mode = 0
                        
                    if button_adjust.collidepoint(event.pos):
                        mode = 2
                    if button_newboard.collidepoint(event.pos):
                        game.reset()
                    if button_newrandom.collidepoint(event.pos):
                        game.reset_rand()
                    if button_inc_dens.collidepoint(event.pos):
                        game.decrease_density()
                    if button_textfield.collidepoint(event.pos):
                        mode = 3

                    if button_dec_dens.collidepoint(event.pos):
                        game.increase_density()
                    if button_inc_speed.collidepoint(event.pos):
                        game.dec_speed()
                    if button_dec_speed.collidepoint(event.pos):
                        game.inc_speed()
                    if button_save.collidepoint(event.pos):
                        game.save_board(text)
                    if button_load.collidepoint(event.pos):
                        game.load_board(text)
                if event.type == pygame.QUIT:
                    running = False
            draw_main_menu(game,text)

        elif mode == 2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = event.pos
                    truex = x + viewer.get_x()
                    truey = y + viewer.get_y()
                    if truex<0 or truey < 0:
                        pass
                    else:
                        xposarray = int(truex/viewer.get_zoom())
                        yposarray = int(truey/viewer.get_zoom())
                        if xposarray<game.size() and yposarray<game.size():
                            game.update(xposarray,yposarray)


            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                viewer.move_up()
            if keys[pygame.K_s]:
                viewer.move_down()

            if keys[pygame.K_a]:
                viewer.move_left()

            if keys[pygame.K_d]:
                
                viewer.move_right()

            if keys[pygame.K_r]:
                zoomincounter +=1
                if zoomincounter>= ZOOMSPEED:
                    viewer.zoom_in()
                    zoomincounter = 0

            if keys[pygame.K_t]:
                zoomoutcounter+=1
                if zoomoutcounter>=ZOOMSPEED:
                    viewer.zoom_out()    
                    zoomoutcounter = 0
            if keys[pygame.K_ESCAPE]:
                mode = 1
                game.copyboard_to_nextboard()
            draw_elements(viewer,game)
        elif mode == 3:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not button_textfield.collidepoint(event.pos):
                        mode = 1
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if text !="Input here":
                            if len(text)==1:
                                text = "Input here"
                            else:
                                text = text[:-1]
                    elif event.unicode.isalpha() or event.unicode in "._0123456789":
                        if text == "Input here":
                            text= ""
                        if len(text)<50:
                            text += event.unicode


            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                mode = 1
            

            draw_main_menu(game,text)
            


        
        clock.tick(FPS_UPDATE)
        


    pygame.quit()
    sys.exit()
    

if __name__ == "__main__":
    main()