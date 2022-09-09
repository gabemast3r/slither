import pygame
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)
blue = (0,0,255)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

img = pygame.image.load('snakehead.png')
appleimg = pygame.image.load('apple.png')

clock = pygame.time.Clock()

block_size = 20
AppleThickness = 30
FPS = 15

smallfont = pygame.font.SysFont(None, 25)
medfont = pygame.font.SysFont(None, 50)
largefont = pygame.font.SysFont(None, 80)

highest = 0



def game_intro():
    intro = True

    while intro:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome to Slither",
                          green,
                          -100,
                          "large")
        message_to_screen("The objective of the game is to eat red apples.",
                          black,
                          -30)
        message_to_screen("The more apples you eat the longer you get.",
                          black,
                          10)
        message_to_screen("Don't run into yourself or the edges of the screen!",
                          black,
                          50)
        message_to_screen("Press C to play, P to pause or Q to quit",
                          black,
                          180)
        pygame.display.update()
        clock.tick(10)

def snake(block_size, snakelist):

    if direction == "right":
        head = pygame.transform.rotate(img, 270)
    if direction == "left":
        head = pygame.transform.rotate(img, 90)
    if direction == "up":
        head = img
    if direction == "down":
        head = pygame.transform.rotate(img, 180)

    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text, colour, size):
    if size == "small":
        textSurf = smallfont.render(text, True, colour)
    elif size == "medium":
        textSurf = medfont.render(text, True, colour)
    elif size == "large":
        textSurf = largefont.render(text, True, colour)
    return textSurf, textSurf.get_rect()

def message_to_screen(msg,colour, y_displace=0, size = "small"):
    textSurf, textRect = text_objects(msg, colour, size)
    textRect.center = (display_width/2), (display_height /2)+y_displace
    gameDisplay.blit(textSurf, textRect)

def pause():

    paused = True
    gameDisplay.fill(white)
    message_to_screen("Paused",
                     black,
                        -100,
                        "large")
    message_to_screen("Press C to continue or Q to quit",black,25, "medium")
    pygame.display.update()

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    GameExit=True
                    pygame.quit()
                    quit()


        clock.tick(10)

def score(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [10,10])

def highscore(highest):
    text = smallfont.render("Highscore: "+str(highest), True, black)
    gameDisplay.blit(text, [10,30])    

def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-AppleThickness))#/10.0)*10
    randAppleY = round(random.randrange(0, display_height-AppleThickness))#/10.0)*10
    return randAppleX, randAppleY


def gameLoop():
    global direction
    global highest
    direction = "right"
    
    gameExit = False
    gameOver = False
    
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = block_size
    lead_y_change = 0

    snakeList = []
    snakeLength = 1

    randAppleX, randAppleY = randAppleGen()

    while not gameExit:

        if gameOver == True:
            
            gameDisplay.fill(white)
            if snakeLength-1 > highest:
                message_to_screen("New Highscore!", red, y_displace = -50, size = "large")
                highest = snakeLength-1
            else:
                message_to_screen("Game over", red, y_displace= -50, size="large")
            score(snakeLength-1)
            highscore(highest)
            message_to_screen("Press C to play again or Q to quit", black, 50, "medium")
            pygame.display.update()
        
        while gameOver == True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if direction != "right":
                        direction = "left"
                        lead_x_change = -block_size
                        lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    if direction != "left":
                        direction = "right"
                        lead_x_change = block_size
                        lead_y_change = 0
                    
                elif event.key == pygame.K_UP:
                    if direction != "down":
                        direction = "up"
                        lead_y_change = -block_size
                        lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    if direction != "up":
                        direction = "down"
                        lead_y_change = block_size
                        lead_x_change = 0

                elif event.key == pygame.K_p:
                    pause()

        lead_x += lead_x_change
        lead_y += lead_y_change

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True
                    
        gameDisplay.fill(white)

         gameDisplay.blit(appleimg, (randAppleX, randAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
            
        snake(block_size, snakeList)

        score(snakeLength-1)
        
        pygame.display.update()
        
##use when block_size == Applethickness:
##        if lead_x == randAppleX and lead_y == randAppleY:
##            randAppleX = round(random.randrange(0, display_width-block_size)/10.0)*10
##            randAppleY = round(random.randrange(0, display_height-block_size)/10.0)*10
##            snakeLength += 1
    
##use when block_size > Applethickness:       
##        if lead_x >= randAppleX and lead_x <= randAppleX + AppleThickness:
##            if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
##                randAppleX = round(random.randrange(0, display_width-block_size))#/10.0)*10
##                randAppleY = round(random.randrange(0, display_height-block_size))#/10.0)*10
##                snakeLength += 1

##use when block_size < Applethickness:
        if lead_x >= randAppleX and lead_x <= randAppleX + AppleThickness or lead_x + block_size >= randAppleX and lead_x + block_size <= randAppleX + AppleThickness:
            if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness or lead_y + block_size >= randAppleY and lead_y + block_size <= randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        clock.tick(FPS)

    pygame.quit()
    quit()

game_intro()
gameLoop()
