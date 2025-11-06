import sys
import pygame
import random

pygame.init()

width = 800
height = 600
size = (width, height)
black = (0, 0, 0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chicken Click Game")

chicken = pygame.image.load("images/yui.png")
chicken = pygame.transform.scale(chicken, (80, 80))

iterator = 0
numofchickens = 5
startX = []
startY = []
speed = []

while iterator < numofchickens:
    startX.append(random.randint(0, width - chicken.get_width() + 1))
    startY.append (0 - random.randint(chicken.get_height(), chicken.get_height() * 2))
    speed.append(random.uniform(0.05, 0.15))
    iterator += 1

replayscreen = False

#Setting up game stuff
bigfont = pygame.font.SysFont(None, 200)
playagaintext = bigfont.render("Play Again?", True, (0, 200, 0))
pax = width/2 - playagaintext.get_rect().width/2

smallfont = pygame.font.SysFont(None, 100)
yestext = smallfont.render("YES", True, (0, 200, 0))
yesx = width/4 - yestext.get_rect().width/2
notext = smallfont.render("NO", True, (0, 200, 0))
nox = width - width/4 - yestext.get_rect().width/2

#Game Loop

gameover = False

while gameover == False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True

    #Clicking on the Chickens
    if pygame.mouse.get_pressed()[0]:
        coords = pygame.mouse.get_pos()
        if replayscreen == False:
            iterator = 0
            while iterator < numofchickens:
                if (coords[0] >= startX[iterator] and coords[0] <= startX[iterator] + chicken.get_width() and coords[1] > startY[iterator] 
                and coords[1] < startY[iterator] + chicken.get_height()):
                    startX[iterator] = random.randint(0, width - chicken.get_width() + 1)
                    startY[iterator] = 0 - random.randint(chicken.get_height(), chicken.get_height() * 2)
                    speed[iterator] = random.uniform(0.05, 0.15) + 0.01
                    break
                iterator += 1
        else:
            if (coords[0] > yesx and coords[0] < yesx + yestext.get_rect().width and coords[1] > 450 and
             coords[1] < 450 + yestext.get_rect().height):
                iterator = 0
                while iterator < numofchickens:
                    startX[iterator] = random.randint(0, width - chicken.get_width() + 1)
                    startY[iterator] = 0 - random.randint(chicken.get_height(), chicken.get_height() * 2)
                    speed[iterator] = random.uniform(0.05, 0.15) + 0.01
                    iterator += 1
                replayscreen = False
            
            if (coords[0] > nox and coords[0] < nox + notext.get_rect().width and coords[1] > 450 and
             coords[1] < 450 + notext.get_rect().height):
                gameover = True


    #Updating
    if replayscreen == False:
        iterator = 0
        while iterator < numofchickens:
            if startY[iterator] + chicken.get_height() > height:
                replayscreen = True
                break
            startY[iterator] += speed[iterator]
            iterator += 1

    #Drawning
    if replayscreen == False:
        screen.fill(black)
        iterator = 0
        while iterator < numofchickens:
            screen.blit(chicken, (startX[iterator], startY[iterator]))
            iterator += 1

        iterator = 0

    #Game over screen
    else:
        screen.fill((200, 0 ,0))

        screen.blit(playagaintext, (pax, 150))
        screen.blit(yestext, [yesx, 450])
        screen.blit(notext, (nox, 450))

    pygame.display.flip()

pygame.display.quit()