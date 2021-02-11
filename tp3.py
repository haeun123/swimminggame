############################################
# Haeun Bang (haeunb) 15-112 Section H
# TP
###########################################

import math, string, copy, random, decimal
from tkinter import *

def roundHalfUp(d): #from 15-112 notes: Check1 Practice
   # Round to nearest with ties going away from zero.
   rounding = decimal.ROUND_HALF_UP
   return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

def rgbString(red, green, blue): #from 15-112 notes on graphics
    return "#%02x%02x%02x" % (red, green, blue)

def boundsIntersect(boundsA, boundsB): #from 15-112 side scroller demo code
    # return l2<=r1 and t2<=b1 and l1<=r2 and t1<=b2
    (ax0, ay0, ax1, ay1) = boundsA
    (bx0, by0, bx1, by1) = boundsB
    return ((ax1 >= bx0) and (bx1 >= ax0) and
            (ay1 >= by0) and (by1 >= ay0))

class Coral(object):
    def __init__(self, x0, y0):
        self.x0 = x0
        self.y0 = y0
        i = random.randint(0,10)
        coralColors = ["violetRed1","deep pink", "coral", "red2", "purple", 
        "chocolate1", "maroon", "orchid1", "plum2", "olive drab", 
        "dark sea green"]
        self.color = coralColors[i]
        self.size = random.randint(10, 30) # ?????
        self.width = random.randint(1, 4) #?????
        self.level = 5
    
    @staticmethod
    def getRandomCoralFromRight(data):
        if data.corals != []: #if there is a previous coral, remember to space
            lastCoral = data.corals[-1]
            if lastCoral.coralOnScreen(data): 
            #if the last coral is the last one in view
            #(IF THERE ISNT CORAL (IN LIST) OUTSIDE OF RIGHT EDGE OF VIEW;
             # NEW CORAL IS NEEDED)
                newCoralx0 = lastCoral.x0 + data.coralSpacing
                data.corals.append(Coral(newCoralx0, data.height))
        else: #first coral of the game
            data.corals.append(Coral(data.width, data.height))
    
    @staticmethod # COMBINE WITH PREVIOUS FUNCTION?
    def getRandomCoralFromLeft(data):  
        if data.corals != []: #if there is a previous coral, remember to space
            lastCoral = data.corals[0]
            if lastCoral.coralOnScreen(data): 
            #if the last coral is the last one in view
            #(IF THERE ISNT CORAL (IN LIST) OUTSIDE OF RIGHT EDGE OF VIEW;
             # NEW CORAL IS NEEDED)
                newCoralx0 = lastCoral.x0 - data.coralSpacing
                data.corals.insert(0,Coral(newCoralx0, data.height))
    
    @staticmethod
    def drawCorals(canvas, data):
        sx = data.scrollX
        drawRight = 50 #so that part of coral doesnt appear suddenly
        for coral in data.corals:
            # optimize by only drawing corals that are on the screen
            if coral.coralOnScreen(data): #if on screen,
                Coral.drawCoral(canvas,coral.x0-sx+drawRight,coral.y0,coral.size,
                    coral.level, coral.color, coral.width)
     
    def coralOnScreen(self, data): 
    # USE THIS FUNCTION TO ACCOMPLISH:
    #   - IN LIST OF CORALS, ONLY DRAW ONES IN VIEW.
    #   - ONLY CREATE CORALS IF THE LAST CORAL IN LIST IS ON SCREEN
        if ((self.x0-data.scrollX+100) <= 0 or (self.x0-data.scrollX) > 
               data.width): 
            return False
        return True
    
    @staticmethod
    def deleteCoralsOffScreen(data): # to reduce length of coral list
        for coral in data.corals:
            if not coral.coralOnScreen(data):
                data.corals.remove(coral)
    
    @staticmethod
    def drawCoral(canvas,x,y,size,level,color,width,angle=90): #fractal
        x1 = x + (size*math.cos(angle*(math.pi/180)))
        y1 = y - (size*math.sin(angle*(math.pi/180)))
        if level >= 0:
            canvas.create_line(x, y, x1, y1, fill=color,width=width)
            Coral.drawCoral(canvas,x1,y1,size,level-1,color,width,angle-30)
            Coral.drawCoral(canvas,x1,y1,size,level-1,color,width,angle+30)

class User(object):
    def __init__(self, userX, userY, health = 20, ability = 1):
        self.userX = userX #x0 of bounding box
        self.userY = userY #y0 of bounding box
        self.health = health
        self.diverImage = PhotoImage(file="diver.gif")
        self.userHeight = self.diverImage.height() - 5
        self.userWidth = self.diverImage.width()
        self.ability = ability
        self.abilityPoints = 0 #every 6 points adds ability; max ability is 3
    
    def updateAbility(self, data): #TIME BASED
        if self.abilityPoints >= 6:
            self.ability += 1 
            #3 is the max ability level, so u can keep increasing 
            # ability after 3 but it wont change anything.
            self.abilityPoints = 0
    
    def drawUser(self, canvas, data):
        sx = data.scrollX #abbreviation as "sx" from side scroll demo
       # sy = data.scrollY
        #15-112 animations, images demo
       # canvas.create_oval(self.userX-sx, self.userY, self.userX + 
        #     self.userWidth -sx, self.userY + self.userHeight, fill="white", 
         #                                                  outline = "white")
        #canvas.create_rectangle(self.userX-sx, self.userY, 
         #self.userX+self.userWidth-sx,self.userY+self.userHeight,fill="white")
        canvas.create_image(self.userX-sx, self.userY,anchor=NW,
              image=self.diverImage)
    
    @staticmethod
    def moveUser(data):
        ## add scrollY features--> abyss or out of water? design thing??
        ## DONT ALLOW TO MOVE IF OUT OF WATER
        data.user.userX +=  data.velocityX
        data.user.userY += data.velocityY
        # 15-112 side scroller demo - a bit adapted
        #if reach right scroll margin, SCROLL forwards
        if (data.user.userX > (data.scrollX + data.width - 
               data.scrollMarginRight)):
            data.scrollX = data.user.userX - data.width + data.scrollMarginRight
            Coral.getRandomCoralFromRight(data)
        if data.user.userX < (data.scrollX + data.scrollMarginLeft):
            if data.scrollX > 0:
                data.scrollX = data.user.userX - data.scrollMarginLeft
                Coral.getRandomCoralFromLeft(data)
        if data.user.userY < 0:
            data.user.userY -= data.velocityY
        elif data.user.userY > data.height:
            data.mode = "Game Over"
            data.mode = "Game Over"
        Coral.deleteCoralsOffScreen(data)
        calculatePhase(data)
        if data.scrollX < 0:
            data.mode = "Game Over"
            data.prevMode = "Game Over"
        

class Fish(object): #early level basic fishes, less threatening
    def __init__(self, fishX, fishY, speedX=0, speedY=0, infected=False): 
        self.fishX = fishX
        self.fishY = fishY
        self.speedX = speedX
        self.speedY = speedY
        self.infected = infected
        fishImages = [PhotoImage(file="goldfishArt.gif"),
              PhotoImage(file="infectedFishArt.gif")]
        if self.infected == False:
            self.fishColor = rgbString(255, random.randrange(140,255), 0)
            self.fishImage = fishImages[0]
        elif self.infected == True:
            self.fishColor = "gray"
            self.fishImage = fishImages[1] #CHANGE TO OTHER PIC LATER
        self.fishWidth = self.fishImage.width()
        self.fishHeight = self.fishImage.height()
        
    @staticmethod
    def getRandomFish(data, infected = False):
        randomHeight = random.randint(0, data.height)
        data.fishList.append(Fish(data.width+data.scrollX,
                         randomHeight,infected=infected))
            
    def moveFishLegal(self, data): #fish shouldnt swim out of water
        topMargin = 10
        if self.fishY < topMargin or self.fishY > data.height:
            return False
        return True
        
    @staticmethod
    def moveFishes(data): #backtrack?
        for fish in data.fishList:
            moved = False
            while moved==False:
                moveX = random.randint(10,20)
                moveY = random.randint(-15,15)
                fish.fishX -= moveX ### DIFFERENT MOVEMENTS FOR HARDER FISH
                fish.fishY -= moveY 
                if not fish.moveFishLegal(data):
                    fish.fishX += moveX
                    fish.fishY += moveY
                moved = True
                
    def fishOnScreen(self, data):  
        if ((self.fishX-data.scrollX) < 0 or 
                 (self.fishX-data.scrollX)>data.width): 
            #is 0 to width the view????????????
            return False
        return True
        
    @staticmethod
    def drawFishes(canvas, data): #grammar "fishes"
        sx = data.scrollX #INSTEAD OF RADIUS I DREW AS BOX BC I WILL REPLACE W 
                                                         # IMAGE LATER ON
        for fish in data.fishList:
            if fish.fishOnScreen(data):
                #canvas.create_oval(fish.fishX-sx, fish.fishY, fish.fishX + 
                #fish.fishWidth-sx, fish.fishY + fish.fishWidth, 
                 #          fill=fish.fishColor, outline=fish.fishColor)
                canvas.create_image(fish.fishX-sx, fish.fishY, anchor=NW, image=fish.fishImage)
                                                    
    @staticmethod
    def removeFishOffGame(data): #ATTEMPT TO SAVE SPACE/INCREASE SPEED
        
        if data.fishList!= []:
            firstFish = data.fishList[0]
            if firstFish.fishX+firstFish.fishWidth < data.scrollX:
                data.fishList.pop(0)

class ShooterFish(Fish):
    pass

class Bubble(object): #user shoots bubbles, fish shoot venom
    def __init__(self,x0,y0,powerLevel):
        self.x0 = x0
        self.y0 = y0
        self.powerLevel = powerLevel #user's ability
        self.moved = 0
        self.speed = 30
        if self.powerLevel == 1:
            self.color = "light cyan"
            self.width = 10
            self.damage = 1
            self.distanceLimit = 300 #????????????????
        elif self.powerLevel == 2:
            self.width = 15
            self.color = "yellow"
            self.damage = 1
            self.distanceLimit = 600
        elif self.powerLevel >= 3:
            self.color = "red"
            self.width = 20
            self.damage = 3 #HOW MUCH DAMAGE IT CAN DEAL
            self.distanceLimit = 1200
        self.powerLeft = self.damage
    
    def moveBubble(self,data):
        self.x0 += self.speed
        self.moved += self.speed
    
    @staticmethod
    def moveBubbles(data): #TIMER FIRED!!!!
        for bubble in data.bubbles:
            if not bubble.inView(data):
                data.bubbles.remove(bubble) #IF IT GOES OFF VIEW, delete
            bubble.moveBubble(data)
            bubble.width = bubble.width - 0.5
            if (bubble.distanceLimit != None and bubble.moved >= 
                 bubble.distanceLimit and bubble in data.bubbles):
                data.bubbles.remove(bubble) # IF IT HAS WENT LONG ENOUGH
            hit = bubble.updateBubbleHit(data)
            if hit != False: #IF HIT A FISH
                print("HIT")
                fishIndex = hit
                hitFish = data.fishList[fishIndex] #update health, etc since hit
                if hitFish.infected == True: #if the fish hit is infected
                    if data.user.health < 20:
                        data.user.health += 2 # +1 health for every infected hit
                    else: #if health is full,
                        data.user.abilityPoints += 1
                elif hitFish.infected == False:
                    data.timeLeft += 50
                    data.timeLeft = min(data.timeLeft, data.timeAllotted)
                elif isinstance(hitFish, ShooterFish):  
                    if data.user.health < 20:
                        data.user.health += 3
                    else:
                        data.user.abilityPoints += 2
                if bubble in data.bubbles:
                    bubble.powerLeft -= 1
                    if bubble.powerLeft <= 0:
                        data.bubbles.remove(bubble) #bubble pops after hit
                data.fishList.remove(hitFish) # fish gets killed since bubble hit
                
    @staticmethod
    def drawBubbles(canvas, data):
        sx = data.scrollX
        for bubble in data.bubbles:
            color = bubble.color
            x0, y0, width = bubble.x0,bubble.y0,bubble.width
            canvas.create_oval(x0-sx,y0,x0+width-sx,y0+width,fill=color)
                
    def updateBubbleHit(self,data): 
        # checks if the bubble hit any of the fish in fish list, 
        # returns index of fish that bubble touches
        bubbleBounds = (self.x0,self.y0,self.x0+self.width,self.y0+self.width)
        for fishIndex in range(len(data.fishList)):
            fish = data.fishList[fishIndex]
            fishBounds = (fish.fishX, fish.fishY, fish.fishX+fish.fishWidth, 
                                                    fish.fishY+fish.fishHeight)
            if boundsIntersect(bubbleBounds, fishBounds):
                return fishIndex
        return False #bubble not hitting any of the fish

    def inView(self, data):  
        if ((self.x0) < data.scrollX or (self.x0)>data.scrollX+data.width): 
            return False
        return True
    
    @staticmethod
    def bubblesInView(data):
        count = 0
        for bubble in data.bubbles:
            if bubble.inView(data):
                count += 1
        return count
    

"""
class Venom(data):
    def __init__(
"""
    
        

## Animation barebones/structure from 15-112 event based animations notes: 
#                                                    events-example0.py
## side scrolling feature adapted from 15-112 side scroller demo

## different functions for different modes structure is from 15-112 mode demo


def init(data):
    data.timerDelay = 70 # to make it a little smoother; in milliseconds
    data.timeAllotted = 12000 #1200000 milliseconds (20 minutes)//100, timer
    data.mode = "splashScreen"
    data.prevMode = "splashScreen"
    data.timeLeft = data.timeAllotted
    data.level = 0
    data.scrollX = 0
    data.scrollMarginLeft = 10
    data.scrollMarginRight = (data.width*3)//4
    data.user = User(data.scrollMarginLeft, data.height//2)
    data.fishList = []
    data.fishImages = []
    data.backgroundImages = [PhotoImage(file="underwater.gif"), PhotoImage(
        file="underwaterdarker1.gif"),PhotoImage(file="underwaterdarker2.gif"),
        PhotoImage(file="underwaterdarker3.gif"),
        PhotoImage(file="underwaterdarker4.gif"),
        PhotoImage(file="underwaterdarker5.gif")]
    data.backgroundImage = data.backgroundImages[0]
    data.colorSections = 100
    data.velocityX = 0
    data.velocityY = 0
    data.drag = 1
    data.gravity = 2 #arbitrary values for now
    data.swimforce = 20
    data.fishSpacer = 0
    data.fishDensity = 20
    data.infectedFishSpacer = 0
    data.infectedFishDensity = 40
    data.shooterFish = False
    data.shooterFishDensity = 40
    data.shooterFishSpacer = 0
    #use vertically changing bars instead?
    data.corals = []
    data.coralSpacing = 100 #arbitrary spacing of each coral
    initializeCorals(data)
    data.pathLength = 100000 #max width of pixels of entire path of game
    data.phases = 6
    data.phase = 1 #max level is 6, when reach 7 --> win
    data.bubbles = [] #from user's attack
    data.venoms = [] #from fishes' attack
    data.bubblesLimit = 5 # number of bubbles allowed on screen at a time
    data.bubblesInView = 0

def initializeCorals(data):
    data.corals.append(Coral(data.scrollX,data.height))
    for coral in range(0, data.width//data.coralSpacing):
        Coral.getRandomCoralFromRight(data)
    
def mousePressed(event, data):
    if data.mode == "splashScreen": splashScreenMousePressed(event, data)
    elif data.mode == "help": helpMousePressed(event,data)
    elif data.mode == "Game Over": gameOverMousePressed(event, data)
    elif data.mode == "underwater": underwaterMousePressed(event, data)
    elif data.mode == "win": winMousePressed(event, data)

def keyPressed(event, data):
    if data.mode == "splashScreen": splashScreenKeyPressed(event, data)
    elif data.mode == "help": helpKeyPressed(event,data)
    elif data.mode == "Game Over": gameOverKeyPressed(event, data)
    elif data.mode == "underwater": underwaterKeyPressed(event, data)
    elif data.mode == "win": winKeyPressed(event, data)

def timerFired(data):
    if data.mode == "splashScreen": splashScreenTimerFired(data)
    elif data.mode == "help": helpTimerFired(data)
    elif data.mode == "Game Over": gameOverTimerFired(data)
    elif data.mode == "underwater": underwaterTimerFired(data)
    elif data.mode == "win": winTimerFired(data)

def redrawAll(canvas, data):
    if data.mode == "splashScreen": splashScreenRedrawAll(canvas, data)
    elif data.mode == "help": helpRedrawAll(canvas, data)
    elif data.mode == "Game Over": gameOverRedrawAll(canvas, data)
    elif data.mode == "underwater": underwaterRedrawAll(canvas, data)
    elif data.mode == "win": winRedrawAll(canvas, data)

### Splash screen mode functions

def splashScreenMousePressed(event, data):
    pass

def splashScreenKeyPressed(event, data):
    if event.keysym == "r":
        data.fishList= []
        data.fishSpacer = 0
        data.fishDensity = 10
        data.infectedFishSpacer = 0
        data.infectedFishDensity = 15
        data.mode = "underwater"
        data.prevMode = "underwater"
    elif event.keysym == "h":
        data.mode = "help"

def splashScreenTimerFired(data):
    data.fishSpacer += 2
    if data.fishSpacer == data.fishDensity:
        data.fishSpacer = 0
        Fish.getRandomFish(data, infected = False)
    data.infectedFishSpacer += 1
    if data.infectedFishSpacer == data.infectedFishDensity:
        data.infectedFishSpacer = 0
        Fish.getRandomFish(data, infected = True)
    Fish.moveFishes(data)
    Fish.removeFishOffGame(data)

def splashScreenRedrawAll(canvas, data):
    drawBackground(canvas, data)
    canvas.create_text(data.width//2+10, data.height//2+10, 
         text="Underwater Adventure",fill="dark sea green",font=
                    "Courier 35 bold")
    canvas.create_text(data.width//2, data.height//2, 
       text="Underwater Adventure",fill = "ivory2", font= "Courier 35 bold")
    canvas.create_text(data.width//2, (data.height*2)//3, 
      text = "Press 'r' to play, 'h' for help", fill="white",
          font="Courier 15 bold")
    Fish.drawFishes(canvas,data)                

### Underwater mode functions

def underwaterMousePressed(event, data):
    pass


def underwaterKeyPressed(event, data):
    #figure out how to do double key press features like pygame
    # IMPORTANT!!!!!!!!!!! MAKE SMOOOTH!!!!!!!
    if event.keysym == "Left":
        if data.scrollX > 0:
            data.velocityX = -1*data.swimforce
            #data.velocityX += 1 #accelerating 
        #data.velocityY = 0 #fricition from swimming horizontally??
        #friction of water keeping swimmer up
    if event.keysym == "Right": 
        data.velocityX = data.swimforce
        #if data.user.userX < data.scrolledX + 
         #   data.velocityX += 1 #accelerating
        #data.velocityY -= 1 #friction from swimming horizontally??NO
    if event.keysym == "Up": 
        data.velocityY = -10
        #data.velocityY -= 1
    if event.keysym == "Down": 
        data.velocityY = 8 #????
        data.velocityY += 1
    elif event.keysym == "h":
        data.mode = "help"    
    elif event.keysym == "space":
        if data.bubblesLimit > data.bubblesInView:
            data.bubbles.append(Bubble(data.user.userX+data.user.userWidth, 
                data.user.userY+(data.user.userHeight//2), data.user.ability))
                

    elif event.keysym == "d": #for debugging/video
        data.user.ability = data.user.ability%3
        data.user.ability += 1
    elif event.keysym == "n":  #FOR DEBUGGING/TESTING
    #skip/advance to next phase or level (simply changing location of userX)??
        data.phase += 1
        data.user.userX = (data.phase-1)*(data.pathLength//data.phases)
        data.scrollX = (data.phase-1)*(data.pathLength//data.phases)
        data.corals = []
        initializeCorals(data)
        


    
def updatePhase(data):
    data.backgroundImage = data.backgroundImages[data.phase-1]
    if data.phase >= 2:
        data.fishDensity = 15
        data.infectedFishDensity = 35
    if data.phase >= 3:
        data.fishDensity = 15
        data.infectedFishDensity = 30
    if data.phase >= 4: #shooting fish introduced 
        #data.shooterFish = True
        data.fishDensity = 10
        data.infectedFishDensity = 25
        #data.shooterFishDensity = 40
    if data.phase >= 5:
        data.fishDensity = 7
        data.infectedFishDensity = 20
    if data.phase == 6: 
        data.fishDensity = 5
        data.infectedFishDensity = 12
       # data.shooterFishDensity = 30
        

def calculatePhase(data): #"phases" are like levels of the journey that
                                # depend on the location of the user
    phaseIncrement = data.pathLength//data.phases
    rightEdgeX = data.scrollX + data.width
    data.phase = (rightEdgeX // phaseIncrement) + 1
    if data.phase == 7:
        data.phase = 1
        data.mode = "win"

def collidesWithFish(data):
    userBounds = (data.user.userX,data.user.userY,data.user.userX+
                  data.user.userWidth, data.user.userY+data.user.userHeight)
    for fishIndex in range(len(data.fishList)):
        fish = data.fishList[fishIndex]
        fishBounds = (fish.fishX, fish.fishY, fish.fishX+fish.fishWidth, 
                                                    fish.fishY+fish.fishHeight)
        if boundsIntersect(userBounds, fishBounds):
            return fishIndex
            ### is it better to return a count just in case there are multiple
            ##  collisions in one timer fire???? TEST OUT;...
    return False


def underwaterTimerFired(data):
    if data.timeLeft <= 0 or data.user.health <= 0:
        data.mode = "Game Over" #should not be the only criteria for game over
        data.mode = "Game Over"
    # if level or score is max: data.mode == "Win"
    data.timeLeft -= 1 #OXYGEN TANK DECREASING
    if data.velocityY < 5: #cant sink too quickly
        data.velocityY += data.gravity
    if abs(data.velocityX) > 0:
        if data.velocityX < 0: #drifting backwards
            data.velocityX += data.drag
        elif data.velocityX > 0:
            data.velocityX -= data.drag
    # exponential function usage
    data.fishSpacer += 1 #way for the timer to create a random fish every 
    # specific number of times that it fires instead of at every fire
    if data.fishSpacer == data.fishDensity:
        data.fishSpacer = 0
        Fish.getRandomFish(data, infected = False)
    data.infectedFishSpacer += 1
    if data.infectedFishSpacer == data.infectedFishDensity:
        data.infectedFishSpacer = 0
        Fish.getRandomFish(data, infected = True)
    """
    if data.shooterFish == True:
        data.shooterFishSpacer += 1
        # FINISH MAKING SHOOTER FISH CLASS!!!!!!!!!!!!, append to fishList
        if data.shooterFishSpacer == data.shooterFishDensity:
            # get random shooter fish!!!!!!!!!!
            data.shooterFishSpacer = 0
    """
    Fish.moveFishes(data)
    User.moveUser(data) #since there is sinkage, movement should be timer based.
    data.user.updateAbility(data)
    # for every fish that the user collides with, health decreases.
    collide = collidesWithFish(data)
    if collide != False:
        collidedFish = data.fishList[collide]
        if collidedFish.infected == True:
            data.user.health -= 1
        else:
            data.timeLeft -= 100
        data.fishList.pop(collide)
    Fish.removeFishOffGame(data) 
    if data.scrollX + data.width == data.pathLength:
        data.mode = "win"
    updatePhase(data)
    data.user.health = min(20, data.user.health) #should not be >20
    Bubble.moveBubbles(data)
    data.bubblesInView = Bubble.bubblesInView(data)
    
    
def drawBackground(canvas, data):
    canvas.create_image(0,0,anchor=NW,image = data.backgroundImage)
    

def drawTimer(canvas, data): #change later maybe
    margin = 40
    x0, y0 = 10, data.height-10
    barWidth, barHeight = data.width-60, 5
    canvas.create_rectangle(x0+margin,y0,x0+barWidth+margin,y0+barHeight,
            fill="red")
    timeWidth = (data.timeLeft/data.timeAllotted)*(barWidth-2)
    canvas.create_rectangle(x0+margin,y0,x0+timeWidth+margin,y0+barHeight,
             fill = "green")
    canvas.create_text(10,data.height-10,text="TANK",anchor=W,fill="white",
              font= "Courier 10 bold")

def drawHealthBar(canvas, data):
    # FIX STYLE AFTER
    canvas.create_rectangle(10,data.height-40,(data.width//3)-10, 
                   data.height-20, fill="black")
    canvas.create_text(25,370,text="H",fill="white",font="Courier 15 bold")
    cellWidth = 7
    margin = 40 # from left  
    for rect in range(1, 21):
        if rect <= data.user.health:
            color = "red"
        elif rect > data.user.health:
             color = "white"
        x0, y0 = margin+cellWidth*rect, data.height-35
        x1, y1 = x0+cellWidth, data.height-25
        canvas.create_rectangle(x0,y0,x1,y1,fill=color,width=2)
    
        
        
def drawMap(canvas, data):
    x0 = (data.width//3)+10
    y0 = data.height-30
    barWidth = (data.width//3)-20
    barHeight = 10
    cellWidth = barWidth//data.phases

    canvas.create_rectangle(x0,y0,x0+barWidth,y0+barHeight, fill="gray")
    for phase in range(0, data.phases): #  0, 1, 2, 3, 4, 5; 
        canvas.create_line(x0+(phase*cellWidth),y0,
                    x0+(phase*cellWidth),y0+barHeight,fill="orange",width=3)
    canvas.create_line(x0+barWidth,y0,x0+barWidth,y0+barHeight,
                   fill="red",width=3)
    canvas.create_text(x0,y0,text="PATH",anchor=SW,fill="white",
                     font="Courier 10 bold")
                     
    #pin bar thing 
    rightEdgeView = data.scrollX+data.width
    pinX0 = x0 + ((rightEdgeView/data.pathLength) * barWidth)
    canvas.create_line(pinX0,y0,pinX0,y0+barHeight,width = 3)

def drawAbilityTracker(canvas,data):
    x0, y0 = (data.width*2)//3, data.height-40
    barWidth, barHeight = 60, 20
    margin = 20
    # FIX STYLE AFTER
    canvas.create_rectangle(x0,y0,x0+barWidth,y0+barHeight, fill="black")
    abilities = ["light cyan", "yellow", "red"]
    abilityColor = abilities[data.user.ability-1]
    canvas.create_oval(x0+2,y0+2,x0+margin-2,y0+margin-2,fill=abilityColor)
    canvas.create_text(x0+margin+5,y0+barHeight//2,
                    text=str(data.user.abilityPoints),fill="white",
                       font= "Helvetica 10 bold")
    canvas.create_text(x0+margin+20,y0+barHeight//2,text="/6",fill="white",
                                           font = "Helvetica 10 bold")
    
    
                     
def underwaterRedrawAll(canvas, data):
    drawBackground(canvas, data)
    Coral.drawCorals(canvas, data)
    Fish.drawFishes(canvas,data)
    data.user.drawUser(canvas, data)
    Bubble.drawBubbles(canvas, data)
    drawTimer(canvas, data)
    drawHealthBar(canvas, data)
    drawMap(canvas, data)
    drawAbilityTracker(canvas,data)
    
    


## Game Over mode functions

def gameOverMousePressed(event,data):
    pass

def gameOverKeyPressed(event, data):
    if event.keysym == "r":
        init(data)

def gameOverTimerFired(data):
    pass

def gameOverRedrawAll(canvas, data):
    canvas.create_rectangle(0,0,data.width,data.height,fill="black")
    canvas.create_text(data.width//2, data.height//2, 
            text="Game Over :(", fill="white", font="Courier 40 bold")
    canvas.create_text(data.width//2, data.height*3//4, text="r to replay",
                                fill = "white", font= "Courier 20 bold")



## Win mode functions

def winMousePressed(event, data):
    pass

def winKeyPressed(event, data):
    if event.keysym == "r":
        init(data)

def winTimerFired(data):
    data.fishSpacer += 2
    if data.fishSpacer == data.fishDensity:
        data.fishSpacer = 0
        Fish.getRandomFish(data, infected = False)
    data.infectedFishSpacer += 1
    if data.infectedFishSpacer == data.infectedFishDensity:
        data.infectedFishSpacer = 0
        Fish.getRandomFish(data, infected = True)
    Fish.moveFishes(data)
    Fish.removeFishOffGame(data)
        
    
def winRedrawAll(canvas, data):
    red, green, blue = 0, 206, 255
    createWaterBackground(canvas, data, 0, 0, data.width, 
               data.height//data.colorSections, red, green, blue)
    canvas.create_text(data.width//2,data.height//2,text= "YOU WON",
                fill = "white", font= "Courier 35 bold")
    canvas.create_text(data.width//2, (2*data.height)//3,
          text="Press 'r' to replay", fill="white", font="Courier 15 bold")
    Fish.drawFishes(canvas,data)
    
    #draw cute moving fractals in start screen and win screen.
    
    
def createWaterBackground(canvas, data, x0,y0,x1,y1,red,green,blue):
    rgb = rgbString(red, green, blue)
    if y0 >= (data.height-(data.height//data.colorSections)):
        canvas.create_rectangle(x0, y0, x1, y1, fill=rgb, outline = rgb )
    else:
        rectHeight = data.height//data.colorSections
        canvas.create_rectangle(x0,y0,x1,y1,fill=rgb,outline = rgb)
        red -= roundHalfUp(red/data.colorSections)
        blue -= roundHalfUp(blue/data.colorSections)
        green -= roundHalfUp(green/data.colorSections)
        return createWaterBackground(canvas, data, x0, y0+rectHeight,
                                 x1, y1+rectHeight, red, green, blue)
                                 


## HELP MODE FUNCTIONS

def helpKeyPressed(event, data): # allows user to pause during game too
    if event.keysym == "h":
        data.mode = data.prevMode

def helpTimerFired(data):
    pass

def helpRedrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill="black")
    canvas.create_text(data.width//2, data.height//2, text= "help screen...",
           fill = "white", font="Courier 40 bold")
    canvas.create_rectangle(50, 50, 50+32, 50+32, fill="white")
    

######################################################################
## run function from 15-112 events-example0.py event-based animations barebones
######################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    init(data)
    # create the root and the canvas
    root = Toplevel() #from stack overflow !!!!!!!!!!!!!!!!!!!
     # http://stackoverflow.com/questions/23224574/tkinter-create-
     # image-function-error-pyimage1-does-not-exist
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


##############################################
# testAll and main
##############################################
root = Tk()
run(600, 400)

