import pygame
import time
#this is used for display, not for the array
class case:
    def __init__(self, x, y, width, height):
        self.color = (255,255,255)
        self.state = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.locked = False

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
    def draw(self):
        # this is responsible for changing the square to cross and circle
        if self.state == 0:
            pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height), 0)
        elif self.state == 1:
            pygame.draw.polygon(screen, (255,0,0), ((self.x + self.width - 20,self.y + 5),(self.x + self.width - 5,self.y + 20),(self.x + 20,self.y + self.height - 5),(self.x + 5,self.y + self.height - 20)))
            pygame.draw.polygon(screen, (255,0,0), ((self.x + 20,self.y + 5),(self.x + self.width - 5,self.y + self.height - 20),(self.x + self.width - 20,self.y + self.height - 5),(self.x + 5,self.y + 20)))
        elif self.state == 2:
            pygame.draw.circle(screen, (0,0,255), (self.x + self.width/2,self.y + self.height/2), self.width/2 - 5, 10)

def score(grid):
    score = 0
    win = False
    if(grid[0][0] == 1): 
        if (grid[0][1] == 1 and grid[0][2] == 1):
            win = True
            score += 1
        if (grid[1][0] == 1 and grid[2][0] == 1):
            win = True
            score += 1
        if (grid[1][1] == 1 and grid[2][2] == 1):
            win = True
            score += 1
    
    elif(grid[0][0] == 2): 
        if (grid[0][1] == 2 and grid[0][2] == 2):
            win = True
            score -= 1
        if (grid[1][0] == 2 and grid[2][0] == 2):
            win = True
            score -= 1
        if (grid[1][1] == 2 and grid[2][2] == 2):
            win = True
            score -= 1

    if(grid[1][1] == 1):
        if(grid[0][2] == 1 and grid[2][0] == 1):
            win = True
            score += 1
        if(grid[0][1] == 1 and grid[2][1] == 1):
            win = True
            score += 1
        if(grid[1][0] == 1 and grid[1][2] == 1):
            win = True
            score += 1
    elif(grid[1][1] == 2):
        if(grid[0][2] == 2 and grid[2][0] == 2):
            win = True
            score -= 1
        if(grid[0][1] == 2 and grid[2][1] == 2):
            win = True
            score -= 1
        if(grid[1][0] == 2 and grid[1][2] == 2):
            win = True
            score -= 1


    if grid[2][2] == 1:
        if(grid[1][2] == 1 and grid[0][2] == 1):
            win = True
            score += 1
        if(grid[2][0] == 1 and grid[2][1] == 1):
            win = True
            score += 1
    
    elif grid[2][2] == 2:
        if(grid[1][2] == 2 and grid[0][2] == 2):
            win = True
            score -= 1
        if(grid[2][0] == 2 and grid[2][1] == 2):
            win = True
            score -= 1
    


 

    return score, win    

def recursion(grid, yourTurn, depth):
    num_lines = 0
    num_col = 0
    isdone = True
    array_of_score = []
    temp_score = 0

    win = False
    depth += 1
    temp_depth = depth
    #goes throw the array of array
    for lines in grid:
        num_col = 0
        for case in lines:
            #test any empty space
            if case == 0:
                isdone = False
                if yourTurn:
                    grid[num_lines][num_col] = 1
                else:
                    grid[num_lines][num_col] = 2

                temp_score, win = score(grid)
                
                if(win):
                    grid[num_lines][num_col] = 0
                    return temp_score, depth
                else:
                    temp_score, temp_depth = recursion(grid, not yourTurn,depth)
                    array_of_score.append(temp_score)
                grid[num_lines][num_col] = 0

                
        
                
            num_col += 1

        num_lines += 1
    depth = temp_depth
    #check if the whole grid is full
    if isdone:
        temp_score,win = score(grid) 
        return temp_score, depth
    else:
        #if its the turn of the AI, take the one that maximise its score, otherwise, take the one that minimasis it
        if yourTurn:
            return max(array_of_score), depth
        else:
            return min(array_of_score), depth

#initiate the screen
screen = pygame.display.set_mode([300, 300])
running = True
screen.fill((255,255,255))

#this is the grid responsible for diplay, not for the minimax algo
grid_points = [[0,0,0],
               [0,0,0],
               [0,0,0]]
grid = []
for y in range(3):
    for x in range(3):
        grid.append(case((x*100)+10, (y*100)+10,80,80))

PlayerPlaying = True

#start the game loop
while running:
    #test for event
    
    for event in pygame.event.get():
        
        #quit when closed
        if event.type == pygame.QUIT:
            running = False
        pos = pygame.mouse.get_pos()


        if event.type == pygame.MOUSEBUTTONDOWN:
            #check is the a case is clicked on
            num_of_col = 0
            num_of_lines = 0
            num_l = 0
            array_moves = []
            array_x = []
            array_y = []
            score_number = 0
            depth = 0
            array_depth = []
            #this is where the magic happens
            for case in grid:
                #test if it clicked on a case
                if case.isOver(pos) and case.locked == False:
                    grid_points[num_of_lines][num_of_col] = 2
                    num_l = 0
                    #start the recursive
                    for lines in grid_points:
                        num_c = 0
                        for cases in lines:
                            if cases == 0:
                                grid_points[num_l][num_c] = 1
                                score_number, depth = recursion(grid_points,  False, 0)
                                array_moves.append(score_number)
                                array_depth.append(depth)
                                array_x.append(num_c)
                                array_y.append(num_l)
                                grid_points[num_l][num_c] = 0
                                
                            num_c += 1
                        num_l += 1
                    place_holder = -100000
                    to_be_x = 0
                    to_be_y = 0
                    pos_of_other_good_numbers = 0
                    array_of_good_numbers = []
                    closest_to_win = 0
                    #get the maximum of the list to see which is the best move
                    for numbers in array_moves:
                        if numbers > place_holder:
                            place_holder = numbers
                            to_be_x = to_be_y
                        to_be_y += 1
                    grid_points[array_y[to_be_x]][array_x[to_be_x]] = 1
                num_of_col += 1
                if num_of_col == 3:
                    num_of_lines += 1
                    num_of_col = 0

        #turn green when hovered over
        if event.type == pygame.MOUSEMOTION:
            for case in grid:
                if case.isOver(pos):
                    case.color = (0,127,0)
                else:
                    case.color = (255,255,255)

    # Fill the background with white
    screen.fill((255, 255, 255))

    #draw the grid
    pygame.draw.rect(screen, (127,127,127), (-10,0,20,500))
    pygame.draw.rect(screen, (127,127,127), (90,0,20,500))
    pygame.draw.rect(screen, (127,127,127), (190,0,20,500))
    pygame.draw.rect(screen, (127,127,127), (290,0,20,500))
    pygame.draw.rect(screen, (127,127,127), (0,-10,500,20))
    pygame.draw.rect(screen, (127,127,127), (0,90,500,20))
    pygame.draw.rect(screen, (127,127,127), (0,190,500,20))
    pygame.draw.rect(screen, (127,127,127), (0,290,500,20))
    num_to_get_display = 0
    #this makes the grid_point display
    for lines3 in grid_points:
        for case3 in lines3:
            grid[num_to_get_display].state = case3
            if (grid[num_to_get_display].state != 0):
                grid[num_to_get_display].locked = True
            
            num_to_get_display += 1
    

    #draw the cross and circles
    for case in grid:
        case.draw()
    #this stops the program if someone won
    useless, score_win = score(grid_points)
    if(score_win == True):
        pygame.display.flip()
        time.sleep(3)
        break

    # Flip the display
    pygame.display.flip()
# Done! Time to quit.
pygame.quit()