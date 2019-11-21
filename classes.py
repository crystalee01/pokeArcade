import pygame
import os
# class representing the player, subclasses Pygame Sprite module
class Player(pygame.sprite.Sprite):
    @staticmethod
    def init():
        Player.image = pygame.image.load(os.path.join('images', 'bubble.png')).convert_alpha()
        # image from http://pixelartmaker.com/art/f8e497226ce8084.png 
        w, h = Player.image.get_size() #returns w, h coordinates of image
        Player.image = pygame.transform.scale(Player.image, (w//6, h//6))

    def __init__(self, row, col, cellSize):
        super(Player, self).__init__()
        self.row, self.col, self.image = row, col, Player.image
        self.cellSize = cellSize
        self.droppedAttacks = pygame.sprite.Group()
        self.attackStrength = 1
        #self.health = 20
        self.updateRect()

    # update the rect around the player
    def updateRect(self):
        cy = self.row * self.cellSize
        cx = self.col * self.cellSize
        self.rect = pygame.Rect(cx, cy, self.cellSize, self.cellSize)
        #print("pokemon rect", self.rect)

    # moves the player to new location based on row, col coordinates
    def move(self, newRow, newCol):
        self.row = newRow
        self.col = newCol

# class representing an Attack, subclasses Pygame Sprite module
class Attack(pygame.sprite.Sprite):
    @staticmethod
    def init():
        Attack.image = pygame.image.load('images/fire.png').convert_alpha()
        # image from http://pixelartmaker.com/art/da234f98a2c9c22.png
        w, h = Attack.image.get_size() #returns w, h coordinates of image
        Attack.image = pygame.transform.scale(Attack.image, (w//6, h//6))
    
    def __init__(self, row, col, cellSize, timeMade):
        super(Attack, self).__init__()
        self.row, self.col, self.cellSize = row, col, cellSize
        self.image = Attack.image
        self.timeMade = timeMade
        self.called = False
        self.updateRect()

    def updateRect(self):
        cy = self.row * self.cellSize
        cx = self.col * self.cellSize
        self.rect = pygame.Rect(cx, cy, self.cellSize, self.cellSize)

# class representing an Attack's splash path, subclasses Pygame Sprite module
class AttackSplash(pygame.sprite.Sprite):
    @staticmethod
    def init():
        Attack.splashImage = pygame.image.load('images/firesplash.png')
        # image from https://art.pixilart.com/d9c96e37cb7541c.png
        sw, sh = Attack.splashImage.get_size() #returns w, h coordinates of image
        Attack.splashImage = pygame.transform.scale(Attack.splashImage, (sw//15, sh//15))

    def __init__(self, row, col, cellSize):
        super(AttackSplash, self).__init__()
        self.row, self.col, self.cellSize = row, col, cellSize
        self.image = Attack.splashImage
        self.updateRect()

    def updateRect(self):
        cy = self.row * self.cellSize
        cx = self.col * self.cellSize
        self.rect = pygame.Rect(cx, cy, self.cellSize, self.cellSize)

# class representing a Block sprite, subclasses Pygame Block module
class Block(pygame.sprite.Sprite):
    @staticmethod
    def init():
        Block.image = pygame.image.load('images/block.png')
        w, h = Block.image.get_size()
        Block.image = pygame.transform.scale(Block.image, (w//25, h//25))

    def __init__(self, row, col, cellSize):
        super(Block, self).__init__()
        self.row, self.col, self.cellSize = row, col, cellSize
        self.image = Block.image
        self.updateRect()

    def updateRect(self):
        cy = self.row * self.cellSize
        cx = self.col * self.cellSize
        self.rect = pygame.Rect(cx, cy, self.cellSize, self.cellSize)

