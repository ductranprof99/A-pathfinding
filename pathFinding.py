import pygame 
import math


from queue import PriorityQueue

WIDTH = 980
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* pathfinding algorithm")

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
YELLOW = (255,255,0)
WHITE = (255,255,255)
ORANGE = (255,69,0)
HAZE = (133, 185, 213)

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
    def is_open(self):
        return self.color == ORANGE
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
    def make_open(self):
        self.color = ORANGE
    def make_barrier(self):
        self.color = BLACK
    def make_end(self):
        self.color = GREEN
    def make_start(self):
        self.color = BLUE
    def make_path(self):
        self.color = HAZE
    def reset(self):
        self.color = WHITE
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def updateNeighbor(self,grid):
        if self.row < self.total_row - 1 and not grid[self.row+1][self.col].is_barrier():
            self.neighbors.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():
            self.neighbors.append(grid[self.row-1][self.col])
        if self.col < self.total_row - 1 and not grid[self.row][self.col+1].is_barrier():
            self.neighbors.append(grid[self.row][self.col+1])
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier():
            self.neighbors.append(grid[self.row][self.col-1])
    def __lt__(self,other):
        return self.color == other.color


#heuristic
def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 -x2) + abs(y1 - y2)

def makePath(dict,currentNode,draw):
    while currentNode in dict:
        currentNode = dict[currentNode]
        currentNode.make_path()
        draw()

def aStar(draw,grid,start,end):
    open_set = PriorityQueue()
    count = 0
    checking_list = {start}
    g_score = {spot: float('inf') for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float('inf') for row in grid for spot in row}
    f_score[start] = h(start.get_pos(),end.get_pos())
    came_from = {}
    reserverTrack = []
    open_set.put((0,count,start))
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        checking_list.remove(current)
        if current == end: 
            makePath(came_from,end,draw)
            end.make_end()
            start.make_start()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current]+1
            if(temp_g_score < g_score[neighbor]):
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor.get_pos(),end.get_pos())
                if neighbor not in checking_list:
                    count += 1
                    open_set.put((f_score[neighbor],count,neighbor))
                    checking_list.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start and current != end:
            current.make_closed()
    
    return False


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
    for row in grid:
        for spot in row:
            spot.draw(win)
    make_and_draw_grid(win,rows,width)
    pygame.display.update()

def getMouse_inPos(pos,rows,width):
    gap = width // rows
    y,x = pos
    row = y // gap
    col = x // gap
    return row,col

def execute(win,width):
    GRIDS = 70
    grid = make_and_draw_grid(win,GRIDS,WIDTH)
    s,e = False,False
    start = None
    end = None
    run = True
    started = False
    pygame.key.set_repeat(1,0)
    while run:
        draw(win,grid,GRIDS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: run = False
            if started: continue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z : 
                    pos = pygame.mouse.get_pos()
                    row,col = getMouse_inPos(pos,GRIDS,width)
                    spot = grid[row][col]
                    if(spot.color == WHITE):  spot.make_barrier()
                if event.key == pygame.K_x and not s: 
                    pos = pygame.mouse.get_pos()
                    row,col = getMouse_inPos(pos,GRIDS,width)
                    spot = grid[row][col]
                    if(spot.color == WHITE):
                        s = True
                        start = spot
                        start.make_start()
                if event.key == pygame.K_c and not e: 
                    pos = pygame.mouse.get_pos()
                    row,col = getMouse_inPos(pos,GRIDS,width)
                    spot = grid[row][col]
                    if(spot.color == WHITE):
                        e = True 
                        end = spot
                        end.make_end()   
                if event.key == pygame.K_d: #delete modified element
                    pos = pygame.mouse.get_pos()
                    row,col = getMouse_inPos(pos,GRIDS,width)
                    spot = grid[row][col]
                    spot.reset()
                    if spot == start: 
                        start = None
                        s = False
                    if spot == end: 
                        end = None
                        e = False
                if event.key == pygame.K_SPACE and e and s and not started: #load and start the algor
                    started = True
                    for row in grid:
                        for ele in row:
                            ele.updateNeighbor(grid)
                    aStar(lambda: draw(win,grid,GRIDS,width),grid,start,end)
    pygame.quit()


execute(WIN,WIDTH)





