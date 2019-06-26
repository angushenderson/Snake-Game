import pygame, time, random
pygame.init()

WIDTH = 500
HEIGHT = 500
SQUARECOUNT = 17
SQUARESIZE = int(round(WIDTH / SQUARECOUNT))
WIDTH = SQUARESIZE * SQUARECOUNT
HEIGHT = WIDTH
window = pygame.display.set_mode((WIDTH,HEIGHT))
lastscore = 0
file = open('highscore.txt','r')
highscore = int(file.read())
file.close()
snake = [(9,4),(9,3),(9,2)]    # location(y,x) 
apple = (9,12)

def newapple(apple,snake):    # gnerate new apple location not on snake
    valid = False
    apple = (random.randint(0,SQUARECOUNT-1),random.randint(0,SQUARECOUNT-1))   # y,x
    while not valid:
        if all([s != apple for s in snake]):
            valid = True
        else:
            apple = (random.randint(0,SQUARECOUNT-1),random.randint(0,SQUARECOUNT-1))   # y,x
    return apple

def gameover(lastscore,highscore,apple,snake):
    text = font.render(('GAME OVER!'),True,(255,0,0))
    textRect = text.get_rect()
    textRect.center = (WIDTH // 2, HEIGHT // 2) 
    window.blit(text,textRect)
    lastscore = len(snake) - 3
    if lastscore > highscore:   
        highscore = lastscore
        text = font.render(('New High Score!'),True,(255,255,0))
        window.blit(text,(20,20))
    pygame.display.update()
    time.sleep(3)
    apple = (9,12)      # reset snake and apple location
    snake = [(9,4),(9,3),(9,2)]    # y,x form
    return lastscore, highscore, apple, snake

def redrawGameWindow():
    pygame.draw.rect(window,(0,0,0),(0,0,WIDTH,HEIGHT))
    for y,x in snake:        
        pygame.draw.rect(window,(255,255,0),(SQUARESIZE * x,SQUARESIZE * y,SQUARESIZE,SQUARESIZE))
    pygame.draw.rect(window,(255,0,0),(apple[1] * SQUARESIZE,apple[0] * SQUARESIZE,SQUARESIZE,SQUARESIZE))
    text = font.render(str(len(snake) - 3),True,(255,0,0))
    window.blit(text,(WIDTH - 100,25))
    pygame.display.update()        

font = pygame.font.Font('freesansbold.ttf',32)
clock = pygame.time.Clock()
movementTime = 0
direction = 'R'
oldDirection = 'R'  # to prevent illigal moves in opposite direction
redrawGameWindow()
run = True
start = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if start:           # start menu
        movementTime = 0
        expand = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            direction = 'R'
            start = False
        elif keys[pygame.K_UP]:
            direction = 'U'
            start = False
        elif keys[pygame.K_DOWN]:
            direction = 'D'
            start = False
        text = font.render(('Press an arrow key to begin'),True,(255,0,0))
        textRect = text.get_rect()
        textRect.center = (WIDTH // 2, HEIGHT // 2) 
        window.blit(text,textRect)
        text = font.render(('High Score: ' + str(highscore)),True,(255,255,0))
        window.blit(text,(25,25))
        text = font.render(('Last Score: ' + str(lastscore)),True,(255,0,0))
        window.blit(text,(25,70))
        pygame.display.update()
        
    else:
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_LEFT]:
            if direction != 'R' and oldDirection != 'R':
                direction = 'L'
        elif keys[pygame.K_RIGHT]:
            if direction != 'L' and oldDirection != 'L':
                direction = 'R'
        elif keys[pygame.K_UP]:
            if direction != 'D' and oldDirection != 'D':
                direction = 'U'
        elif keys[pygame.K_DOWN]:
            if direction != 'U' and oldDirection != 'U':
                direction = 'D'

        movementTime += clock.tick()
        if movementTime >= 110:     # change to increace/decreace move speed of snake
            oldDirection = direction
            if direction == 'L':
                snake.insert(0,(snake[0][0],snake[0][1] - 1))   # index, value
            elif direction == 'R':
                snake.insert(0,(snake[0][0],snake[0][1] + 1))
            elif direction == 'U':
                snake.insert(0,(snake[0][0] - 1,snake[0][1]))
            elif direction == 'D':
                snake.insert(0,(snake[0][0] + 1,snake[0][1]))

            # death colision detect
            if expand:
                expand = False
            else:
                snake.pop(-1)

            if snake[0][0] >= SQUARECOUNT or snake[0][0] < 0 or snake[0][1] >= SQUARECOUNT or snake[0][1] < 0:
                start = True
                lastscore, highscore, apple, snake = gameover(lastscore,highscore,apple,snake)
            for s in snake[1:]:     # coliding with self
                if s == snake[0]:
                    start = True
                    lastscore, highscore, apple, snake = gameover(lastscore,highscore,apple,snake)

            # check for colision with apple and therefore snake expantion
            if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
                apple = newapple(apple,snake)
                expand = True
                
            movementTime = 0
        redrawGameWindow()

file = open('highscore.txt','w')
file.write(str(highscore))
file.close()
pygame.quit()
