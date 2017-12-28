'''
Created on 2015/08/25

@author: fuke
'''
import pygame,os,sys
from pygame.locals import *
from network import Comp


pygame.font.init()
comp = Comp()
screen = pygame.display.set_mode((400,400))

none, black, white = 0,1,2

def Path():
    for name in sys.argv:
        if os.path.exists(name) == True:
            return os.path.dirname(name)
       
img = pygame.image.load(os.path.join(Path(),'png','tips.png')).convert()
bkblack = pygame.image.load(os.path.join(Path(),'png','min_black.png')).convert()
bkwhite = pygame.image.load(os.path.join(Path(),'png','min_white.png')).convert()

index_x = 6
index_y = 5
size = 50
   
class Player():
    auto = False
    stone = none

class Grid():       
    def __init__(self):        
        self.grid = [[none for y in range(8)] for x in range(8)]
        self.stone = none   
         
    def Assign(self,item):
        for x in range(8):
            for y in range(8):
                self.grid[x][y] = item.grid[x][y]
    
class StoneGrid():
    def __init__(self):    
        self.item = Grid()
        self.buffer = Grid()
        self.arr = Grid()
        self.turn_index = 0
        self.active = True
        self.gameover = False
        self.text = pygame.font.SysFont(pygame.font.get_fonts()[0], 25, True).render('reversi',False,(0,0,255)).convert()        
    
    def Clear(self):
        for x in range(8):
            for y in range(8):
                self.item.grid[x][y] = none
        self.item.grid[3][3] = black
        self.item.grid[4][4] = black
        self.item.grid[4][3] = white 
        self.item.grid[3][4] = white 
        self.turn_index = 0
        self.turn_number = 0
        
    def CalScore(self,stone,x,y):
        self.buffer.Assign(self.item)
        if self.CanSetStone(stone, x, y, True) == True:
            self.score = 0.5
            for i in range(8):
                for j in range(8):
                    if self.CanSetStone(stone, i, j, False) == True:
                        self.score += 1
            self.item.Assign(self.buffer)
        else:
            self.score = 0
                                           
    def CanSetStone(self,stone,x,y,reverse):
        p = [True,False]        
        def Method(m,n):            
            if p[0] == False:
                return
            i = 1
            while True:
                d = x+m*i
                e = y+n*i
                if not ((0 <= d)and(d < 8)and(0 <= e)and(e < 8)):
                    break
                s = self.item.grid[d][e]
                if s == none:
                    break
                elif s == stone:                                
                    if i > 1:
                        if reverse == True:   
                            if p[1] == False:
                                self.item.grid[x][y] = stone
                                p[1] = True                         
                            j = 1
                            while j <= i-1:
                                self.item.grid[x+m*j][y+n*j] = stone
                                j += 1
                        else:
                            p[0],p[1] = False,True
                    break
                else:
                    i += 1
                   
        if self.item.grid[x][y] == none:            
            Method(-1,-1)
            Method(-1, 0)
            Method(-1, 1)
            Method(0, -1)
            Method(0, 1)
            Method(1, -1)
            Method(1, 0)
            Method(1, 1)
        return p[1]
                            
    def T_Data(self,stone):
        x = False
        n = 0
        for i in range(8):
            for j in range(8):
                self.CalScore(stone, i, j)
                if self.score > 0:
                    if x == False:
                        x = True
                    self.arr.grid[i][j] = self.score
                    if self.score > n:
                        n = self.score
                else:
                    self.arr.grid[i][j] = 0
        if n > 0:
            for i in range(8):
                for j in range(8):
                    k = self.arr.grid[i][j]
                    if k > 0:
                        self.arr.grid[i][j] = (n - k + 0.5) / n
    
    def Start(self):       
        global index 
        index = player1
        self.Clear()
        self.active = True
        self.gameover = False
        Paint()
        
    def ReStart(self):
        self.active = True
        self.gameover = False
        self.turn_index = self.turn_number
        
    def Pause(self):
        self.active = False
               
    def Paint(self):
        if self.effect_stone == black:
            s = bkwhite           
        else:
            s = bkblack
        i = 0
        while i < len(self.list):
            p = self.list[i]
            screen.blit(s,(p.Left*50,p.Top*50),(p.X*50,p.Y*50,50,50))
            i += 1
                    
def Paint():
    for x in range(8):
        for y in range(8):
            s = stone_grid.item.grid[x][y]
            r = pygame.Rect(x*size,y*size,(x+1)*size,(y+1)*size)
            if s == white:
                screen.blit(img,r,pygame.Rect(2*size,0,3*size,size))
            elif s == black:
                screen.blit(img,r,pygame.Rect(size,0,2*size,size))
            else:
                screen.blit(img,r,pygame.Rect(0,0,size,size))
    if stone_grid.gameover == True:
        screen.blit(stone_grid.text,pygame.Rect(0,0,800,50))
    pygame.display.update()
       
def ChangePlayer():  
    def Main():
        global index        
        Paint()      
        if index == player1:
            index = player2
            return 'white'
        else:
            index = player1
            return 'black'  
    
    def Execute():
        for x in range(8):
            for y in range(8):
                if stone_grid.CanSetStone(index.stone, x, y, False) == True:
                    return True
        return False
        
    s = Main()+str(stone_grid.turn_index+1)
    if Execute() == False:
        s = Main()+str(stone_grid.turn_index+1)
        if Execute() == False:
            s = 'game over'
            i = 0
            j = 0
            for x in range(8):
                for y in range(8):
                    if stone_grid.item.grid[x][y] == black:
                        i += 1
                    elif stone_grid.item.grid[x][y] == white:
                        j += 1
            pygame.display.set_caption(s+str(stone_grid.turn_index+1))
            if i > j:
                s = 'Player1 Win!'
            elif i < j:
                s = 'Player2 Win!'
            else:
                s = 'Draw'            
            stone_grid.text = pygame.font.SysFont(pygame.font.get_fonts()[0],25,True).render(s+'(Player1){0}(Player2){1}'.format(i,j),False,(0,0,255)).convert()
            stone_grid.gameover = True
            Paint()
        else:
            pygame.display.set_caption(s)
            stone_grid.turn_index += 1
    else:
        pygame.display.set_caption(s)
        stone_grid.turn_index += 1
        
def CompStone():
    stone_grid.active = False
    stone_grid.T_Data(index.stone)
    if index.stone == black:
        pre = comp.sente_stone(stone_grid.item.grid,stone_grid.arr.grid)
    elif index.stone == white:
        pre = comp.gote_stone(stone_grid.item.grid,stone_grid.arr.grid) 
    stone_grid.CanSetStone(index.stone, pre[0], pre[1], True)
    print(pre)
    stone_grid.active = True
                 
player1 = Player()
player2 = Player()
index = player1
player1.stone = black
player1.auto = False
player2.auto = True
player2.stone = white
stone_grid = StoneGrid()
stone_grid.Start()
pygame.event.get()
temp = pygame.time.get_ticks()
Paint()
tt = (player1.auto == True)and(player2.auto == True)
if tt == True:
    k = 10
else:
    k = 150
while True:    
    if (pygame.time.get_ticks()-temp > 2*k)and(stone_grid.gameover == False):
        if (stone_grid.active == True)and(index.auto == True):        
            CompStone()            
            ChangePlayer()                 
        temp = pygame.time.get_ticks()
    pygame.time.wait(k)
    for x in pygame.event.get():
        if x.type == QUIT:
            sys.exit()    
    t = pygame.mouse.get_pressed()[0]
    if (stone_grid.gameover == True)and((t == True)or(tt == True)):
        stone_grid.Start()
    if (index.auto == False)and(stone_grid.active == True)and(t == True):            
        stone_grid.active = False
        s = pygame.mouse.get_pos()
        if stone_grid.CanSetStone(index.stone,s[0]//size,s[1]//size,True) == True:
            stone_grid.turn_index += 1            
            ChangePlayer() 
        stone_grid.active = True        
        