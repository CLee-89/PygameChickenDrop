import sys
import pygame
import random

pygame.init()

#Need for delta time
clock = pygame.time.Clock()

#Window settings
width = 800
height = 600
size = (width, height)
black = (0, 0, 0)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Chicken Click Game")

chicken = pygame.image.load("images/yui.png")
chicken = pygame.transform.scale(chicken, (80, 80))
score = 0

iterator = 0
numofchickens = 5
startX = []
startY = []
speed = []

#Speed settings
dspeedmin = 1
dspeedmax = 2
speedmin = dspeedmin
speedmax = dspeedmax
speedinc = .02

#Creates the chickens at the start
while iterator < numofchickens:
    startX.append(random.randint(0, width - chicken.get_width() + 1))
    startY.append (0 - random.randint(chicken.get_height(), chicken.get_height() * 2))
    speed.append(random.uniform(speedmin, speedmax))
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

smallerfont = pygame.font.SysFont(None, 25)
scoretext = smallerfont.render(("Yuis clicked : " + str(score)), True, (255, 255, 255))
scoretext.set_alpha(100)
scorex = 1

#Powerup image, powerup dictionary, powerup data
pimage = pygame.transform.scale(pygame.image.load("images/guitar.png"), (80, 80))

powerup = {
    "image" : pimage,
    "spawned" : False,
    "active_timer" : 0,
    "duration" : 3,
    "active" : False,
    "speed" : dspeedmin,
    "slow_speed" : dspeedmin * .75,
    "data" : {"x" : 0, "y" : 0}
}

data_x = random.randint(0, width - pimage.get_width() + 1)
data_y = 0 - random.randint(pimage.get_height() + 300, (pimage.get_height() * 2) + random.randint(300, 900))
powerup["data"]["x"] = data_x
powerup["data"]["y"] = data_y


gameover = False
#Game Loop
while gameover == False:
    #Convert milliseconds to seconds
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            gameover = True
            
        #Checks if mouse button 1 is pressed
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            coords = event.pos
            if replayscreen == False:
                iterator = 0
                #Checks if any chickens were clicked 
                while iterator < numofchickens:
                    if (coords[0] >= startX[iterator] and coords[0] <= startX[iterator] + chicken.get_width() and coords[1] >= startY[iterator] 
                    and coords[1] <= startY[iterator] + chicken.get_height()):
                        if powerup.get("active") == False:
                            speedmin += speedinc
                            speedmax += speedinc
                        startX[iterator] = random.randint(0, width - chicken.get_width() + 1)
                        startY[iterator] = 0 - random.randint(chicken.get_height(), chicken.get_height() * 2)
                        speed[iterator] = random.uniform(speedmin, speedmax)  
                        score += 1             
                        break
                    iterator += 1

                #Check if bonus is clicked
                if (coords[0] >= powerup.get("data", {}).get("x") and coords[0] <= powerup.get("data", {}).get("x") + powerup.get("image").get_width() and coords[1] >= powerup.get("data", {}).get("y")
                and coords[1] <= powerup.get("data", {}).get("y") + powerup.get("image").get_height()):
                    data_x = random.randint(0, width - pimage.get_width() + 1)
                    data_y = 0 - random.randint(pimage.get_height() + 300, (pimage.get_height() * 2) + random.randint(300, 900))
                    powerup["data"]["x"] = data_x
                    powerup["data"]["y"] = data_y
                    powerup["active"] = True
                    break
            #Checks if yes or no buttons were clicked
            else:
                if (coords[0] > yesx and coords[0] < yesx + yestext.get_rect().width and coords[1] > 450 and
                coords[1] < 450 + yestext.get_rect().height):
                    iterator = 0
                    speedmin = dspeedmin
                    speedmax = dspeedmax

                    while iterator < numofchickens:
                        startX[iterator] = random.randint(0, width - chicken.get_width() + 1)
                        startY[iterator] = 0 - random.randint(chicken.get_height(), chicken.get_height() * 2)
                        speed[iterator] = random.uniform(speedmin, speedmax)
                        iterator += 1
                    data_x = random.randint(0, width - pimage.get_width() + 1)
                    data_y = 0 - random.randint(pimage.get_height() + 300, (pimage.get_height() * 2) + random.randint(300, 900))
                    powerup["data"]["x"] = data_x
                    powerup["data"]["y"] = data_y
                    score = 0
                    replayscreen = False
                
                if (coords[0] > nox and coords[0] < nox + notext.get_rect().width and coords[1] > 450 and
                coords[1] < 450 + notext.get_rect().height):
                    gameover = True



    #Updating
    #Counts up to duration of powerup, turns powerup off if duration is reached
    if replayscreen == False:
        if powerup.get("active") == True:
            powerup["active_timer"] = powerup.get("active_timer", 0) + dt
            if powerup.get("active_timer") > powerup.get("duration"):
                powerup["active"] = False
                powerup["active_timer"] = 0

        iterator = 0
        #Checks if any chickens reached bottom of screen
        while iterator < numofchickens:
            if startY[iterator] + chicken.get_height() > height:
                replayscreen = True
                break

            #Checks speeds for chickens, slows them down if powerup is active  
            if powerup.get("active") == True:
                    startY[iterator] += powerup.get("slow_speed")
            else:
                startY[iterator] += speed[iterator]
            iterator += 1

        #Slows down powerup if powerup is active
        if powerup.get("active") == True:
            powerup["data"]["y"] += powerup.get("slow_speed")
        else:
            powerup["data"]["y"] += powerup.get("speed")

        scoretext = smallerfont.render(("Yuis clicked : " + str(score)), True, (255, 255, 255))


    #Drawning
    if replayscreen == False:
        screen.fill(black)

        iterator = 0
        while iterator < numofchickens:
            screen.blit(chicken, (startX[iterator], startY[iterator]))
            iterator += 1
        screen.blit(powerup.get("image"), (powerup.get("data", {}).get("x"), powerup.get("data", {}).get("y")))

    #Game over screen
    else:
        screen.fill((200, 0 ,0))

        screen.blit(playagaintext, (pax, 150))
        screen.blit(yestext, [yesx, 450])
        screen.blit(notext, (nox, 450))

    #Display score
    screen.blit(scoretext, (scorex, 5))

    pygame.display.flip()

pygame.display.quit()