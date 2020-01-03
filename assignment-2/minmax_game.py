import pygame
import random

class NIM:

    '''
    state : this value stores the present number
    player : -1 represents computer ( MIN player )
             +1 represents user ( MAX player )
    '''
    def __init__(self, n):
        self.n = n

    def startState(self):
        return self.n

    def isTerminalState(self, state):
        return state == 0

    def possible_moves(self, state):
        if state >= 3:
            return [1,2,3]
        return range(1, state+1)

    def make_move(self, state, move):
        if move > state:
            return 0
        return state - move

    def evaluate(self, state, player):
        prev_player = -1*player  
        if state == 0:
            if prev_player == -1:   #if computer brought the state to 0
                return -10
            else:
                return 10   #if player brought the state to 0

def bestMove(game, state, player):
   
    def minimax(state, player):

        if game.isTerminalState(state) == True:
            return (game.evaluate(state, player), None)

        if (state, player) in memoize_table:
            return memoize_table[(state, player)]

        moves = []
        for action in game.possible_moves(state):
            moves.append( ( minimax(game.make_move(state, action), -1*player)[0], action) )

        if player == +1:
            best_val_move = max(moves)
        else:
            best_val_move = min(moves)

        memoize_table[(state, player)] = best_val_move
        return best_val_move
    
    value, move = minimax(state, player)
    return (value, move)

memoize_table = {}


def drawUI(DISPLAYSURFACE, width, height, posx = 0, posy = 0):
    myfont = pygame.font.SysFont("monospace", 75)
    w = int(width/4)
    for i in range(1,4):
        COLOR = (255,255,0)
        label =  myfont.render(str(i),1,(0,0,0))
        if posx <= i*w + 50 and posx >= i*w - 50 and posy >= height - 200 and posy <= height - 100:
            COLOR = (0,0,255)
        pygame.draw.circle(DISPLAYSURFACE, COLOR,(int(i*width/4), height - 150),50)
        DISPLAYSURFACE.blit(label, (int(i*width/4)-20, height-190))

def draw_game(DISPLAYSURFACE, width, height, state, posx = 0, posy = 0):
    DISPLAYSURFACE.fill((0,0,0)) 
    myfont = pygame.font.SysFont("monospace", 125)
    label = myfont.render(str(state).zfill(2), 1, (0,0,0))
    pygame.draw.circle(DISPLAYSURFACE, (0,255,0), (int(width/2),int(height/2)-50),100)
    DISPLAYSURFACE.blit(label, (width/2-75, height/2-125))
    drawUI(DISPLAYSURFACE, width, height, posx, posy)

def mouse_input(posx , posy, width, height):
    w = int(width/4)
    if not (posy >= height - 200 and posy <= height - 100):
        return 0
    for i in range(1,4):
        if posx <= i*w + 50 and posx >= i*w - 50:
            return i
    return 0

if __name__ == "__main__":
    
    game = NIM(random.randint(12,50))

    pygame.init()
    
    width = 900
    height = 650
    DISPLAYSURFACE = pygame.display.set_mode((width, height))
    pygame.display.update()
    
    myfont = pygame.font.SysFont("monospace", 90)
    state = game.startState()
    
    players = [-1, 1]
    turn = random.choice(players)
    flag = 0
    
    while (state > 0):
        posx = 0
        posy = 0
        for event in pygame.event.get():
            
            # For Game exiting
            if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
                state = 0
                import sys
                pygame.quit()
                sys.exit()

            # if event.type == pygame.QUIT:
            #     state = 0
            #     sys.exit()
            
            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                posy = event.pos[1]
                drawUI(DISPLAYSURFACE, width, height, posx, posy)

            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if turn == 1:   #players turn
                    action = 0
                    posx = event.pos[0]
                    posy = event.pos[1]
                    action = mouse_input(posx, posy, width, height)
                    if action in [1,2,3] or state - action < 0:
                        state -= action
                        turn = -turn
                if state == 0:
                    flag=1
                    DISPLAYSURFACE.fill((0,0,0))
                    label = myfont.render("Player wins", 1, (0,255,0))
                    pygame.display.update()
                    DISPLAYSURFACE.blit(label, (width/5-70,200))
                    
            draw_game(DISPLAYSURFACE, width, height, state, posx, posy)
            pygame.display.update()

        if turn == -1 and state > 0:    #Computer turn
            pygame.display.update()
            label = myfont.render("CPU's turn", 1, (255,0,0))
            DISPLAYSURFACE.blit(label, (width/5,50))
            pygame.display.update()
            pygame.time.wait(500)
            val, act = bestMove(game, state, 1)
            state -= act

            if state == 0:
                flag=0
                DISPLAYSURFACE.fill((0,0,0))
                label = myfont.render("CPU wins!!", 1, (255,0,0))
                DISPLAYSURFACE.blit(label, (width/5,200))
            turn = -turn
        pygame.display.update()
    
    if state == 0:
        if flag==1:
            DISPLAYSURFACE.fill((0,0,0))
            label = myfont.render("Player wins!!", 1, (0,255,0))
            DISPLAYSURFACE.blit(label, (width/5-70,200))
        else:
            DISPLAYSURFACE.fill((0,0,0))
            label = myfont.render("CPU wins!!", 1, (255,0,0))
            DISPLAYSURFACE.blit(label, (width/5,200))
        pygame.display.update()