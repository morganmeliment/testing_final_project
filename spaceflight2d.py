"""
spaceshooter.py
Author: vinzentmoesch
Credit: Liam
http://freegameassets.blogspot.com/2013/09/asteroids-and-planets-if-you-needed-to.html
Assignment:
Write and submit a program that implements the spacewar game:
https://github.com/HHS-IntroProgramming/Spacewar
"""
"""
tutorial4.py
by E. Dennison
"""


"""
WASD = movement
R = relode
P = panic stop button
points only count when you're moving
"""
from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame
from ggame import App, Sprite, ImageAsset, Frame
from ggame import SoundAsset, Sound, TextAsset, Color
import math
from time import time
import random

# zufallszahl
def zufaellig(stellen, komma):
    zufaelligout = round((random.random())*(10**stellen), komma)
    return zufaelligout

#Hintergrund
class Stars(Sprite):

    asset = ImageAsset("images/starswithoutspacesmall.jpg")
    width = 7485
    height = 4930
 
    def __init__(self, position):
        super().__init__(Stars.asset, position)
        self.scale = 0.23
         
class astroid(Sprite):
    asset = ImageAsset("images/asteroid1.png", 
    Frame(5,5,62,62), 4, 'vertical')
    
    def __init__(self, position, width, height):
        super().__init__(astroid.asset, position)    
        self.avx = 0
        self.widthscreen = width
        self.heightscreen = height
        self.avy = 0
        self.avr = 0.05
        self.circularCollisionModel()
        

        self.randomx = 0
        self.randomy = 0
        self.fxcenter = self.fycenter = 0.5
        self.randomxn = 0
        self.randomyn = 0
        
        self.boom = 0
        self.slope = 0
        self.bslope = 0
        self.angle1 = 0
        self.angle2 = 0

        
        self.randomx = zufaellig(0, 3)
        self.randomy = zufaellig(0, 3)
        self.randomxn = zufaellig(0,1)
        self.randomyn = zufaellig(0, 1)
        #self.avx = (self.randomx*-1)*6
        #self.avy = (self.randomy*-1)*6
        self.avy = 8
        self.avx = 5
        
    def step(self):
        # abfrage
        if self.x > self.widthscreen-30:
            self.avx = self.avx*-1
        elif self.x < 30:
            self.avx = self.avx*-1
        elif self.y < 30:
            self.avy = self.avy*-1
        elif self.y > self.heightscreen-30:
            self.avy = self.avy*-1
            
            
        self.rotation += self.avr
        self.x += self.avx
        self.y += self.avy

        clw = self.collidingWithSprites(astroid)
        if len(clw) > 0:
            #print("da")
            ospr = clw[0]
            self.slope = (self.y-ospr.y)/(self.x-ospr.x)
            self.bslope=(1/self.slope)*-1
            print(self.bslope)
            self.angle1 = math.atan((self.y-ospr.y)/(self.x-ospr.x))
            print(self.angle1)
            self.angle2 = math.atan((self.avy)/(self.avx))
            """if self.vy < 0:
                if self.vx < 0:
                    self.angle2 = self.angle2 +2*math.pi
            """
            print(self.angle2)
            self.avy = 0
            self.avx = 0

class SpaceShip(Sprite):
    """
    Animated space ship
    """
    asset = ImageAsset("images/UFO2.png", 
        Frame(0,0,485,490), 6, 'vertical')
     
 
    def __init__(self, position, width, height):
        super().__init__(SpaceShip.asset, position)
        self.scale = 0.15
        self.widthscreen = width
        self.heightscreen = height
        self.vx = 0
        self.vy = 0
        self.vr = 0
        self.thrustL = 0
        self.thrustR = 0
        self.thrustU = 0
        self.thrustD = 0
        self.panic = 0
        self.thrustframe = 1
        self.imagenumber = 0
        self.boom = 0
        self.counterstep = 0
        self.countersecond = 0
        self.circularCollisionModel()
        
        SpaceGame.listenKeyEvent("keydown", "left arrow", self.thrustLOn)
        SpaceGame.listenKeyEvent("keyup", "left arrow", self.thrustLOff)
        SpaceGame.listenKeyEvent("keydown", "right arrow", self.thrustROn)
        SpaceGame.listenKeyEvent("keyup", "right arrow", self.thrustROff)
        SpaceGame.listenKeyEvent("keydown", "p", self.panicOn)
        SpaceGame.listenKeyEvent("keyup", "p", self.panicOff)
        SpaceGame.listenKeyEvent("keydown", "up arrow", self.thrustUOn)
        SpaceGame.listenKeyEvent("keyup", "up arrow", self.thrustUOff)
        SpaceGame.listenKeyEvent("keydown", "down arrow", self.thrustDOn)
        SpaceGame.listenKeyEvent("keyup", "down arrow", self.thrustDOff)
        SpaceGame.listenKeyEvent("keydown", "r", self.explosionOff)
        SpaceGame.listenKeyEvent("keyup", "r", self.explosionOff)
        

        self.fxcenter = self.fycenter = 0.5
 
    def step(self):
        if self.thrustL == 1:
            self.vx -= 0.08
        if self.thrustR == 1:
            self.vx += 0.08
        if self.thrustU == 1:
            self.vy -= 0.08
        if self.thrustD == 1:
            self.vy += 0.08
        if self.panic == 1:
            self.vx = 0
            self.vy = 0
            self.panic = 0
        if self.panic == -1:
            self.vx = 0
            self.vy = 0
            self.panic = 0
        self.x += self.vx
        self.y += self.vy
        self.rotation += self.vr
        if self.thrustL == 1 or self.thrustR == 1 or self.thrustU == 1 or self.thrustD == 1 or self.panic == 1:
            self.setImage(self.thrustframe)
            self.imagenumber += 1
            if self.imagenumber == 9:
                self.thrustframe += 1
                if self.thrustframe >= 6:
                    self.thrustframe = 2
                self.imagenumber = 0
        else:
            self.setImage(0)
            
        if self.x > self.widthscreen-30:
            self.vx = self.vx*-1
        elif self.x < 30:
            self.vx = self.vx*-1
        elif self.y < 30:
            self.vy = self.vy*-1
        elif self.y > self.heightscreen-30:
            self.vy = self.vy*-1
        
        collidingwith = self.collidingWithSprites(astroid)
        if len(collidingwith) > 0:
            self.boom = 1
            self.explosionOn(self.x, self.y)
            
        if self.boom == 0:
            if self.vx != 0 or self.vy != 0:
                self.counterstep += 1
                if self.counterstep == 20:
                    self.countersecond += 1
                    print(self.countersecond)
                    self.counterstep = 0
                
 
        
        
    def thrustLOn(self, event):
        self.thrustL = 1
 
    def thrustLOff(self, event):
        self.thrustL = -1
     
    def thrustROn(self, event):
        self.thrustR = 1
         
    def thrustROff(self, event):
        self.thrustR = -1
 
    def thrustUOn(self, event):
        self.thrustU = 1
 
    def thrustUOff(self, event):
        self.thrustU = -1
         
    def thrustDOn(self, event):
        self.thrustD = 1
     
    def thrustDOff(self, event):
        self.thrustD = -1
     
    def panicOn(self, event):
        self.panic = 1
         
    def panicOff(self, event):
        self.panic = -1
     
     
    def explosionOn(self, x, y):
        self.visible = False
        self.panic = 1
        
    def explosionOff(self, event):
        self.visible = True
        self.boom = 0
        self.panic = -1
        self.countersecond = 0
 
class SpaceGame(App):
    """
    Tutorial4 space game example.
    """
    def __init__(self, width, height):
        super().__init__(width, height)
        Stars((0,0))
        SpaceShip((700,500), self.width, self.height)
        astroid((234,423), self.width, self.height)
        astroid((572,245), self.width, self.height)
        #astroid((424,523), self.width, self.height)
        #astroid((234,240), self.width, self.height)
        #astroid((234,423), self.width, self.height)
        #astroid((572,245), self.width, self.height)

  
    def step(self):
        for ship in self.getSpritesbyClass(SpaceShip):
            ship.step()
        for Bstroid in self.getSpritesbyClass(astroid):
            Bstroid.step()
        
        #punktestand

 
             
myapp = SpaceGame(0, 0)
myapp.run() 