'''
Created on 2015/08/25

@author: fuke
'''
import pygame,os,sys
from pygame.locals import *
from threading import Thread
from network import * 


pygame.font.init()
screen = pygame.display.set_mode((400,400))

none, black, white, effect = 0,1,2,3

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

class Effect(Thread):
    def __init__(self):
        self.X = 0
        self.Y = 0
        self.Left = 0
        self.Top = 0

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
        self.arr = [-1 for x in range(65)]
        self.item = Grid()
        self.buffer = [Grid() for x in range(61)]
        self.turn_number = 0
        self.turn_index = 0
        self.active = True
        self.list = []        
        self.effect_stone = none
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
        self.buffer[0].Assign(self.item)
        
    def CalScore(self,stone,x,y):
        def Normal():
            for x in range(8):
                for y in range(8):
                    if self.CanSetStone(stone, x, y, False) == True:
                        self.score += 1
                                           
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
                if s == effect:
                    s = self.effect_stone
                if s == none:
                    break
                elif s == stone:                                
                    if i > 1:
                        if (p[1] == False)and(reverse == True):
                            self.item.grid[x][y] = stone
                            p[1] = True
                        if reverse == True:                            
                            j = 1
                            while j <= i-1:
                                self.item.grid[x+m*j][y+n*j] = stone
                                j += 1
                            break
                        else:
                            p[0],p[1] = False,True
                            break
                    else:
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
                            
    def NextStone(self,stone,pos):
        result = False
        n = 0
        self.score = 0    
        self.arr[0] = stone    
        for i in range(8):
            for j in range(8):
                if self.CalScore(stone, i, j) == True:
                    if result == False:
                        result = True
                    self.arr[1+(j-1)*8+i] = self.score
                    if self.score > n:
                        n = self.score
                    pos[0],pos[1] = i,j
        for i in range(1,len(self.arr)):
            if self.arr[i] != -1:
                self.arr[i] = (n-self.arr[i])/n
        return result
    
    def Start(self):       
        global index 
        index = player1
        self.Clear()
        self.active = True
        self.gameover = False
        
    def ReStart(self):
        self.active = True
        self.gameover = False
        self.turn_index = self.turn_number
        
    def Pause(self):
        self.active = False
        
    def ListExecute(self):
        while True:
            i = 0            
            for x in self.list:                
                if x.X < index_x-1:
                    x.X += 1
                elif x.Y < index_y-1:
                    x.X = 0
                    x.Y += 1
                else:
                    self.item.grid[x.Left][x.Top] = self.effect_stone
                    self.list.remove(x)
                pygame.time.wait(5)                
                i += 1              
                self.Paint() 
                pygame.display.update()            
            if len(self.list) == 0:                              
                if self.turn_index < 60:                               
                    self.turn_index += 1
                    self.turn_number += 1  
                    self.buffer[self.turn_index].Assign(self.item)        
                    self.buffer[self.turn_index].stone = self.effect_stone                                                    
                    Paint()
                    ChangePlayer()       
                    if self.gameover == False:             
                        self.active = True
                else:
                    self.gameover = True
                break                   
       
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
            elif s == effect:
                continue
            else:
                screen.blit(img,r,pygame.Rect(0,0,size,size))
    if stone_grid.gameover == True:
        screen.blit(stone_grid.text,pygame.Rect(0,0,800,50))
    pygame.display.update()
       
def ChangePlayer():  
    def Main():
        global index        
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
    else:
        pygame.display.set_caption(s)
        
def CompStone():
    pos = [0,0]
    stone_grid.active = False
    if stone_grid.NextStone(index.stone, pos) == True:
        pos = compstone(pos[0],pos[1])                                  
        stone_grid.CanSetStone(index.stone, pos[0], pos[1], True) 
    else:
        ChangePlayer()
                 
player1 = Player()
player2 = Player()
index = player1
player1.stone = black
player1.auto = True
player2.auto = True
player2.stone = white
stone_grid = StoneGrid()
stone_grid.Start()
pygame.event.get()
temp = pygame.time.get_ticks()
Paint()
while True:    
    if pygame.time.get_ticks()-temp > 300:
        if (stone_grid.active == True)and(index.auto == True):        
            CompStone()
            #stone_grid.th.join()                                          
        temp = pygame.time.get_ticks()
    pygame.time.wait(150)
    for x in pygame.event.get():
        if x.type == QUIT:
            if len(stone_grid.list) > 0:
                stone_grid.th.join()
            sys.exit()    
    t = pygame.mouse.get_pressed()[0]
    if (stone_grid.gameover == True)and(t == True):
        stone_grid.Start()
    if (index.auto == False)and(stone_grid.active == True)and(t == True):            
        stone_grid.active = False
        s = pygame.mouse.get_pos()
        stone_grid.CanSetStone(index.stone,s[0]//50,s[1]//50,True,True)        
        stone_grid.th.join()    
        stone_grid.active = True    
        