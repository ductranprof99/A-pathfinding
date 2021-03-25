import pygame 
import math


from queue import PriorityQueue

WIDTH = 1000
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* pathfinding algorithm")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
YELLOW = (255,255,0)
WHITE = (255,255,255)

class Spot():
    def __init__(self,row,col,width,total_row):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE  
        self.neighbors = []
        self.width  = width
        self.total_row = total_row

    def get_pos(self):
        return self.row,self.col
        
    def is_closed(self):
        return self.color == YELLOW
    def is_barrier(self):
        return self.color == BLACK
    def is_end(self):
        return self.color == GREEN
    def is_start(self):
        return self.color == BLUE
    def is_path(self):
        return self.color == RED
    def make_closed(self):
        self.color = YELLOW
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = GREEN
    def make_start(self):
        self.color = BLUE
    def make_path(self):
        self.color = RED
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def updateNeighbor(self):
        pass
    def __lt__(self,other):
        return False


#heuristic
def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 -x2) + abs(y1 - y2)

def make_and_draw_grid(win,rows,width):
    grid  = []
    gap = width // rows
    for i in range(0,rows):
        pygame.draw.line(win,PURPLE,(0,i*gap),(width,i*gap))
        grid += [[Spot(i,j,gap,rows) for j in range(0,rows)]]
        for j in range(rows):
            pygame.draw.line(win,PURPLE,(j*gap,0),(j*gap,width))
    return grid

def draw(win,grid,rows,width):
    win.fill(WHITE)
    for i in grid:
        for spot in rows:
            spot.draw(win)
    make_and_draw_grid(win,rows,width)
    pygame.display.update()

def getMouse_inPos(pos,rows,width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row,col

def execute():
    GRID = 70
    grid = make_and_draw_grid()
    start = None
    end = None
    run = True
    started = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if started: continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_B: 1
                if event.key == pygame.K_S: 2
                if event.key == pygame.K_E: 3
                
        
    pygame.quit()




