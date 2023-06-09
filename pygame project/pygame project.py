#made by Joel, this is the program code for the car game named "super ultra car"


#  license info for the font used:

#  The FontStruction “Last Ninja 2 (Amstrad)”
#  (https://fontstruct.com/fontstructions/show/2304420) by Patrick H. Lauke is
#  licensed under a Creative Commons Attribution license
#  (http://creativecommons.org/licenses/by/3.0/).
#  “Last Ninja 2 (Amstrad)” was originally cloned (copied) from the
#  FontStruction “Dizzy III - Fantasy World Dizzy”
#  (https://fontstruct.com/fontstructions/show/1413198) by Patrick H. Lauke, which
#  is licensed under a Creative Commons Attribution license
#  (http://creativecommons.org/licenses/by/3.0/).




# controls:
# A and D for steering the car
# W for acceleration (speeds up the car)


import pygame, sys, math, time, random;

pygame.init()


width = 1200
height = 700
gameClock = pygame.time.Clock();#initialises the game clock

win = pygame.display.set_mode((width,height))
pygame.display.set_caption("game")


playerImage = pygame.image.load("assets/player.png")
pygame.display.set_icon(playerImage)

pygame.mixer.music.load("assets/bits_and_bytes.wav")








###########################################################################################################
def MenuLoop():
    inMenuLoop = True
    while inMenuLoop:
        win.fill((255,255,255))


        titleBG = pygame.image.load("assets/TitleScreen.png")#loads the road image
        titleBG = pygame.transform.scale(titleBG, (width, height) )#sets the scale of the road image
        win.blit(titleBG,(0,0))
        
        
        
        


        #menu buttons:

        #play button
        playButton = button(-450, -60, 200, 65, "Play", (0,255,0))
        playButton.draw();
        if (playButton.IsPressed()):
            inMenuLoop = False

        #quit button
        QuitButton = button(-450, -180, 170, 50, "Quit", (255,0,0))
        QuitButton.draw();
        if (QuitButton.IsPressed()):
            inMenuLoop = False
            pygame.quit()
            sys.exit()
        


        pygame.display.update()
        # exit handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inMenuLoop = False
                pygame.quit()
                sys.exit()
    gameLoop()
###########################################################################################################
def textObjects(text, font, colour = (0,0,0)):
    textObjSurface = font.render(text, True, colour)
    return textObjSurface,textObjSurface.get_rect()

###########################################################################################################
class button:# i made the button into a class instead. This way the implementation is more modular.
    def __init__(self,x=0,y=0,buttonWidth=200,buttonHeight=65,text="Text",colour=(0,255,0),textSize=30):
        self.x = x
        self.y = y
        self.buttonWidth = buttonWidth
        self.buttonHeight = buttonHeight
        self.textSize = textSize
        self.text = text
        self.colour = colour

    def draw(self, colourHighlight = False):
        if colourHighlight:

            pygame.draw.rect(win, (self.colour[0], self.colour[1], self.colour[2]), (width/2+self.x-self.buttonWidth*0.5, height/2-self.y-self.buttonHeight*0.5, self.buttonWidth, self.buttonHeight))
        else:
            pygame.draw.rect(win, (self.colour[0]*0.5, self.colour[1]*0.5, self.colour[2]*0.5), (width/2+self.x-self.buttonWidth*0.5, height/2-self.y-self.buttonHeight*0.5, self.buttonWidth, self.buttonHeight))
        textSurface, textRect = textObjects(self.text, pygame.font.Font("assets/last-ninja-2-amstrad/last-ninja-2-amstrad.ttf",self.textSize),(255,255,255))
        textRect.center = (width/2+self.x, height/2-self.y)
        win.blit(textSurface, textRect)
    def IsPressed(self):
        isHoveringOver = (pygame.mouse.get_pos()[0] < width/2+self.x+self.buttonWidth*0.5 and\
                pygame.mouse.get_pos()[0] > width/2+self.x-self.buttonWidth*0.5 and\
                pygame.mouse.get_pos()[1] < height/2-self.y+self.buttonHeight*0.5 and\
                pygame.mouse.get_pos()[1] > height/2-self.y-self.buttonHeight*0.5)
        self.draw(isHoveringOver)#this causes the button to 'glow' when the cursor hovers over them
        return isHoveringOver and pygame.mouse.get_pressed()[0]

###########################################################################################################

def lerp(a,b,v):
    return a+(b-a)*max(min(v,1),0)
###########################################################################################################
def rot_center(image, rect, rotation):
        rectCenter = rect.center
        rotatedImage = pygame.transform.rotate(image, rotation)
        rotatedRect = rotatedImage.get_rect(center=rectCenter)
        return rotatedImage,rotatedRect

###########################################################################################################

def rotatePoint(point=[0,0], rotationAngle=0, pivotPoint=[0,0]):


    rotationRadians = -(rotationAngle/180)*3.1415926

    #sets the new rotatedPoint variable to the position of the point and then translates it so that the center of rotation (the pivotPoint) is at the origin
    rotatedPoint = [point[0]-pivotPoint[0],point[1]-pivotPoint[1]]

    newCoords = [0,0]
    #applies rotation transform
    newCoords[0] = rotatedPoint[0] * math.cos(rotationRadians) - rotatedPoint[1] * math.sin(rotationRadians)
    newCoords[1] = rotatedPoint[0] * math.sin(rotationRadians) + rotatedPoint[1] * math.cos(rotationRadians)


    #translates the now rotated point back to match its original offset from the pivotPoint
    rotatedPoint[0] = newCoords[0] + pivotPoint[0]
    rotatedPoint[1] = newCoords[1] + pivotPoint[1]


    return rotatedPoint


###########################################################################################################
class obstacle():
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
    def drawObstacle(self,screenScroll):
        obstacleImage = pygame.image.load("assets/obstacle.png")
        obstacleImage = pygame.transform.scale(obstacleImage, (150, 150))
        obstacleRect = pygame.Rect( self.xPos-75, self.yPos-75+screenScroll, 150, 150)
        #obstacleImage, obstacleRect = rot_center(obstacleImage,obstacleRect, 0)
        win.blit(obstacleImage,obstacleRect)

###########################################################################################################
class pickUp():
    def __init__(self):
        self.xPos = 0
        self.yPos = 0
    def drawpickUp(self,screenScroll):
        obstacleImage = pygame.image.load("assets/jerryCan.png")
        obstacleImage = pygame.transform.scale(obstacleImage, (150, 150))
        obstacleRect = pygame.Rect( self.xPos-75, self.yPos-75+screenScroll, 150, 150)
        #obstacleImage, obstacleRect = rot_center(obstacleImage,obstacleRect, 0)
        win.blit(obstacleImage,obstacleRect)




def createPickUp():
    global pickUpList,height,width,playerPosition
    pickUpList.append(pickUp())
    pickUpList[len(pickUpList)-1].yPos -= random.randrange(height+100,height*3+100)+playerPosition[1]#return the fuel pick up to above the screen (with some randomness in the height to create variation)
    pickUpList[len(pickUpList)-1].xPos = random.randrange(0,width)#randomise fuel pick up position

def createObstacle():
    global obstacleList,height,width,playerPosition
    obstacleList.append(obstacle())
    obstacleList[len(obstacleList)-1].yPos -= random.randrange(height+100,height*2+100)+playerPosition[1]#return the obstacle to above the screen (with some randomness in the height to create variation)
    obstacleList[len(obstacleList)-1].xPos = random.randrange(0,width)#randomise obstacle position
###########################################################################################################
        
def resetVariables():
    global oldScore,playerVelocity,debugMode,fuelLevel,playerPosition,pickUpList,drift,boost,roadscroll,deltaTime,escapeInputLimiter,playerSmoothAngle,playerAngle,score,inGameLoop,carSpeed,obstacleList

    debugMode = False# make this true to visualise collisions
    oldScore =  0
    playerPosition = [width/2,0]
    playerVelocity = [0,0]
    startCarSpeed = 0.5
    drift = 0
    fuelLevel = 100
    boost=1
    playerAngle = 0
    playerSmoothAngle = 0
    score = 0
    carSpeed = startCarSpeed
    inGameLoop = True
    deltaTime = 0.001;
    escapeInputLimiter = False
    roadscroll = 0
    obstacleList = []
    i=0
    for i in range(2):
        createObstacle()
    pickUpList = []
    createPickUp()# create a fuel pickup at the start of the game

resetVariables()

###########################################################################################################
def crash(didFuelRunOut = False):
    global playerAngle,fuelLevel,playerSmoothAngle,playerPosition, score, carSpeed,deltaTime, startCarSpeed

    #game over text
    if didFuelRunOut:
        textSurface, textRect = textObjects("No Fuel Remaining", pygame.font.Font("assets/last-ninja-2-amstrad/last-ninja-2-amstrad.ttf",30),(255,255,255))
        textRect.center = (width/2, height/2-200)
        win.blit(textSurface, textRect)
    else:
        textSurface, textRect = textObjects("Game Over", pygame.font.Font("assets/last-ninja-2-amstrad/last-ninja-2-amstrad.ttf",30),(255,255,255))
        textRect.center = (width/2, height/2-200)
        win.blit(textSurface, textRect)

    #final score text
    textSurface, textRect = textObjects("Score: " + str(score), pygame.font.Font("assets/last-ninja-2-amstrad/last-ninja-2-amstrad.ttf",30),(255,255,255))
    textRect.center = (width/2, height/2-100)
    win.blit(textSurface, textRect)
    
    pygame.display.update()
    crash_sound = pygame.mixer.Sound("assets/car_brake_crash.mp3")
    crash_sound.set_volume(0.2)
    crash_sound.play()
    pygame.mixer.music.stop()
    time.sleep(1)
    while(True):
        
        #Retry button
        playButton = button(0, -60, 300, 65, "Retry", (0,255,0))
        playButton.draw()
        if (playButton.IsPressed()):
            resetVariables()
            gameLoop()

        #back button
        playButton = button(0, -190, 150, 65, "Back", (255,0,0))
        playButton.draw()
        if (playButton.IsPressed()):
            inGameLoop = False
            resetVariables()
            MenuLoop()
            
            
        #exit handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inGameLoop = False
                pygame.quit()
                sys.exit()
        gameClock.tick(30)
        pygame.display.update()



###########################################################################################################
def pause():#pause screen
    global escapeInputLimiter,inGameLoop,deltaTime
    paused = True

    while paused:

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            if not escapeInputLimiter:
                paused = False

            escapeInputLimiter = True
        else:
            escapeInputLimiter = False

        win.fill((255,255,255))
        textSurface, textRect = textObjects("game paused", pygame.font.Font("assets/last-ninja-2-amstrad/last-ninja-2-amstrad.ttf",55),(0,0,0))
        textRect.center = (width/2, 40)
        win.blit(textSurface, textRect)

        #continue button
        playButton = button(0, -60, 300, 65, "Continue", (0,255,0))
        playButton.draw()
        if (playButton.IsPressed()):
            paused = False

        #quit button
        playButton = button(0, -190, 150, 65, "Quit", (255,0,0))
        playButton.draw()
        if (playButton.IsPressed()):
            inGameLoop = False
            resetVariables()
            MenuLoop()

        #exit handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inGameLoop = False
                pygame.quit()
                sys.exit()
        gameClock.tick(30)
        pygame.display.update()

###########################################################################################################
def fuelPickUpCollision(carCollisionCheckPoints):
        # collision detection for fuel pickups
        global fuelLevel, score
        pickUpColliderSize = [68,88]
        for i in range(len(pickUpList)):
            pickUpScreenPosition = playerPosition[1]+pickUpList[i].yPos
            if (pickUpScreenPosition>height):
                    pickUpList[i].yPos -= random.randrange(height+100,height*2+100)#return the fuel pick up to above the screen (with some randomness in the height to create variation)
                    
                    pickUpList[i].xPos = random.randrange(0,width)#randomise fuel pick up position
            pickUpList[i].drawpickUp(playerPosition[1])
            for ii in range(len(carCollisionCheckPoints)):#for each player collision point (there are 8 in total)
                pos = [playerPosition[0]+carCollisionCheckPoints[ii][0],height*0.6+75+carCollisionCheckPoints[ii][1]]

                xAxisCollision = abs(pos[0]-(pickUpList[i].xPos))<pickUpColliderSize[0]*0.5
                yAxisCollision = abs(pos[1]-(pickUpList[i].yPos+playerPosition[1]))<pickUpColliderSize[1]*0.5
                if (xAxisCollision and yAxisCollision):
                    fuelLevel+=50
                    score+= 250
                    pickUpList[i].yPos -= random.randrange(height+100,height*3+100)#return the fuel pick up to above the screen (with some randomness in the height to create variation)
                    
                    pickUpList[i].xPos = random.randrange(0,width)#randomise fuel pick up position
                    
                if (debugMode):
                    pygame.draw.rect(win, (255,0,255),(pickUpList[i].xPos-pickUpColliderSize[0]*0.5,pickUpScreenPosition-pickUpColliderSize[1]*0.5,pickUpColliderSize[0],pickUpColliderSize[1]))
###########################################################################################################

def obstacleCollision(carCollisionCheckPoints):
        global score
        obstacleColliderSize = [[85,55],[40,70]]# this defines the dimensions of the bounding boxes that make up each obstacle.
        obstacleColliderOffset = [[0,15],[0,0]]#  this defines the bounding box offset from the center of the obstacle sprite.
        i=0
        for i in range(len(obstacleList)):
            obstacleScreenPosition = playerPosition[1]+obstacleList[i].yPos
            obstacleList[i].drawObstacle(playerPosition[1])
            if (obstacleScreenPosition>height):
                    obstacleList[i].yPos -= random.randrange(height+100,height*2+100)#return the obstacle to above the screen (with some randomness in the height to create variation)
                    score+=1000#the player earns 1000 points for every obstacle avoided.
                    obstacleList[i].xPos = random.randrange(0,width)#randomise obstacle position
            if (abs(obstacleScreenPosition-(height*0.6+75))<130 and abs(obstacleList[i].xPos-playerPosition[0])<130):# this culls thee collision of any objects far away from the car
                
            
                iii = 0
                for iii in range(2):# for ech collision shape that makes up the obstacle (there are two for each obstacle)
                    ii=0
                    for ii in range(len(carCollisionCheckPoints)):#for each player collision point (there are 8 in total)
                        pos = [playerPosition[0]+carCollisionCheckPoints[ii][0],height*0.6+75+carCollisionCheckPoints[ii][1]]

                        xAxisCollision = abs(pos[0]-(obstacleList[i].xPos+obstacleColliderOffset[iii][0]))<obstacleColliderSize[iii][0]*0.5
                        yAxisCollision = abs(pos[1]-(obstacleList[i].yPos+playerPosition[1]+obstacleColliderOffset[iii][1]))<obstacleColliderSize[iii][1]*0.5
                        if (xAxisCollision and yAxisCollision):
                            crash()#the player has hit the obstacle

                        #if debug mode is active, this will draw the collision boundaries in the game.
                        if (debugMode):
                            pygame.draw.rect(win, (255,0,255),
                            (obstacleList[i].xPos-obstacleColliderSize[iii][0]*0.5+obstacleColliderOffset[iii][0],# this is the calculated x component of the obstacle position
                            (obstacleList[i].yPos+playerPosition[1])-obstacleColliderSize[iii][1]*0.5+obstacleColliderOffset[iii][1],# this calculates the y component of the obstacle position
                            obstacleColliderSize[iii][0], obstacleColliderSize[iii][1]))# this calculates the width and height of the obstacle position

                            pygame.draw.rect(win, (255,0,255), (pos[0]-4, pos[1]-4, 8, 8))

###########################################################################################################
def rotationToVector(rotationAngle=0.0):
    return [math.cos(((rotationAngle)/180)*3.14159),math.sin(((rotationAngle)/180)*3.14159)]
###########################################################################################################

def gameLoop():
    global oldScore,playerVelocity,fuelLevel,playerPosition,drift,boost,roadscroll,deltaTime,escapeInputLimiter,playerSmoothAngle,playerAngle,score,inGameLoop,carSpeed,pickUpList
    pygame.mixer.music.play(-1)
    pygame.display.update()
    gameClock.tick(30)
    while inGameLoop:
        win.fill((128,128,128))



        deltaTime = 1/30


        carSpeed+=deltaTime*0.01
        
        if not (score == oldScore) and round(score*0.0001)>round(oldScore*0.0001):# every 10000 points, a new obstacle is created to make the game harder
            createObstacle()
            
        oldScore = score
        #user input
        keys = pygame.key.get_pressed()


        if keys[pygame.K_w]:
            boost = lerp(boost,2,deltaTime*2)
        else:
            boost = lerp(boost,1,deltaTime*2)



        if keys[pygame.K_a]:
            playerAngle += deltaTime*230#rotates the car
            drift = lerp(drift,-1,deltaTime*2)#controls the direction and magnitude of the drift force applied to the player car

        if keys[pygame.K_d]:
            playerAngle -= deltaTime*230#rotates the car
            drift = lerp(drift,1,deltaTime*2)#controls the direction and magnitude of the drift force applied to the player car

        if not keys[pygame.K_d] and not keys[pygame.K_a]:
            drift = lerp(drift,0,deltaTime*4)

        #the playerSmoothAngle slowly moves to match the playerAngle resulting in a more natural transition
        playerSmoothAngle = lerp(playerSmoothAngle,playerAngle,deltaTime*8)

        #adds a forward force to the player in the direction they are facing to simulate the cars movement.
        playerVelocity[0] += (math.cos(((playerSmoothAngle+90)/180)*3.1415926)*deltaTime*24*carSpeed) * boost
        playerVelocity[1] += (math.sin(((playerSmoothAngle+90)/180)*3.1415926)*deltaTime*24*carSpeed) * boost

        #adds a side force to simulate drift.
        playerVelocity[0] += (math.sin(((playerSmoothAngle+90)/180)*3.1415926)*deltaTime*8) * -drift
        playerVelocity[1] += (math.cos(((playerSmoothAngle+90)/180)*3.1415926)*deltaTime*8) * drift


        # here playerVelocity is normalised and then the carSpeed and boost multipliers are applied.
        velocityMagnitude = math.sqrt(pow(playerVelocity[0],2) + pow(playerVelocity[1],2))
        playerVelocity[0] = ( playerVelocity[0] / velocityMagnitude) * carSpeed*boost
        playerVelocity[1] = ( playerVelocity[1] / velocityMagnitude) * carSpeed*boost

        #the position of the player is incremented using delta time to produce a consistant speed across different frame rates.
        playerPosition[0] += playerVelocity[0]*deltaTime*500
        playerPosition[1] += playerVelocity[1]*deltaTime*500





       
        roadscroll = playerPosition[1] % (width / 2)#this code calculates the position and scroll of the road
        roadImage = pygame.image.load("assets/road.png")#loads the road image
        roadImage = pygame.transform.scale(roadImage, (width * 2, width / 2) )#sets the scale of the road image

        
        i = 0
        while (i<4):#the road is made of 4 repeated segments that are displayed in series
            imageRect = pygame.Rect( -width / 2, (width / 2) * (i - 1) + roadscroll, 1, 1)
            win.blit(roadImage,imageRect)
            i+=1



        #drawing the car #####################################
        playerImage = pygame.image.load("assets/player.png")
        playerImage = pygame.transform.scale(playerImage, (150, 150))



        imageRect = pygame.Rect( (playerPosition[0])-75, height*0.6, 150 , 150)
        playerImage, imageRect = rot_center(playerImage,imageRect, playerSmoothAngle)
        win.blit(playerImage,imageRect)
        ######################################################







        carRotationVector = rotationToVector(playerSmoothAngle+90)# this represents a 2d vector containing the normalized direction of the car


        carCollisionSize = [25,60]#this is a list containinig the width and height of the car in pixel units


        #this is a value that stores the x component of the location in space (relative to the center of the car sprite) of
        #the furthest corner of the bounding box of the car after rotation has been applied.
        carWidthXComponent = abs(carCollisionSize[0]*carRotationVector[1])+abs(carCollisionSize[1]*carRotationVector[0])




        #this checks if the player is outside of the boundries of the map (the left and right walls)
        if (abs(playerPosition[0]-width/2)>width/2-carWidthXComponent):
            crash()




        #generate collision data

        

                # this defines 8 points around the perimeter of the car which are used to check collisions. We use points rather than a bounding box becuase you cant rotate a bounding box, but you can rotate points.
                #when any of these points is inside the bounding box of an obstacle, then the car has collided with that obstacle. turn on debug mode to see the points in the game. 
        carCollisionCheckPoints = [rotatePoint( [-carCollisionSize[0], carCollisionSize[1]],playerSmoothAngle,[0,0]),
                                    rotatePoint([ carCollisionSize[0], carCollisionSize[1]],playerSmoothAngle,[0,0]),
                                    rotatePoint([ 0                  ,-carCollisionSize[1]],playerSmoothAngle,[0,0]),
                                    rotatePoint([ 0                  , carCollisionSize[1]],playerSmoothAngle,[0,0]),
                                    rotatePoint([ carCollisionSize[0],-carCollisionSize[1]],playerSmoothAngle,[0,0]),
                                    rotatePoint([-carCollisionSize[0],-carCollisionSize[1]],playerSmoothAngle,[0,0]),
                                    rotatePoint([-carCollisionSize[0], 0                  ],playerSmoothAngle,[0,0]),
                                    rotatePoint([ carCollisionSize[0], 0                  ],playerSmoothAngle,[0,0])]
        

        #collision detection for obstacles and fuel
        obstacleCollision(carCollisionCheckPoints)
        fuelPickUpCollision(carCollisionCheckPoints)



        fuelLevel -= deltaTime*5
        fuelLevel = min(fuelLevel,100)
        if (fuelLevel<=0):
            crash(True)

        #car fuel bar
        fuelTextSurface, fuelTextRect = textObjects("fuel", pygame.font.Font("assets/last-ninja-2-amstrad/last-ninja-2-amstrad.ttf",15),(255,255,255))#fuel text
        fuelTextRect.center = (40, height/2-220)
        win.blit(fuelTextSurface, fuelTextRect)
        pygame.draw.rect(win, (10,10,10), (25, height/2-205, 20, 410))#fuel bar border
        pygame.draw.rect(win, (0,255,0), (30, height/2-fuelLevel*4+200, 10, 4*fuelLevel))#fuel bar fill 
        

        #pause button
        playButton = button(0, 300, 60, 60, "II", (120,120,120),25)
        playButton.draw();
        if (playButton.IsPressed()):
            pause()

        if keys[pygame.K_ESCAPE]:
            if not escapeInputLimiter:
                escapeInputLimiter = True
                pause()
            escapeInputLimiter = True
        else:
            escapeInputLimiter = False


        #draws the score text

        pygame.draw.rect(win, (80,0,0), (100, 4, 200+20*(len(str(score))), 40))
        scoreSurface, scoreRect = textObjects("score:"+str(score), pygame.font.Font("assets/last-ninja-2-amstrad/last-ninja-2-amstrad.ttf",20),(255,255,255))
        scoreRect.center = (200+10*(len(str(score))), 25)
        win.blit(scoreSurface, scoreRect)


        #exit handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                inGameLoop = False
                pygame.quit()
                sys.exit()
        gameClock.tick(30)
        pygame.display.update()


MenuLoop()
pygame.quit()
