import pygame
from pygamegame import *
from classes import *
import math, copy, random

# class that represents the opening screen, subclasses PygameGame  
class HomeScreenMode(PygameGame):
    def init(self):
        pass

    def redrawAll(self, screen):
        pass
    
    # performs responses based on keypresses
    def keyPresses(self):
        if self.isKeyPressed(pygame.K_SPACE):
            playGame = GameMode()
            playGame.run()

    # running the "game loop"
    def timerFired(self, dt):
        self.keyPresses()

# class that represents the game screen, subclasses PygameGame        
class GameMode(PygameGame):
    # initializes game components
    def init(self):
        self.initGameGrid()
        self.initPlayer()
        self.playerGroup = pygame.sprite.Group(self.player) # store the player in a sprite group to check for collisions
        self.attackSplashes = pygame.sprite.Group()

    # initializes game components for player
    def initPlayer(self):
        while True:
            randRow = random.randint(0, self.rows - 1)
            randCol = random.randint(0, self.cols - 1)
            if self.board[(randRow, randCol)][0] == False:
                Player.init()
                self.player = Player(randRow, randCol, self.cellSize)
                break

    # initializes the game grid
    def initGameGrid(self):
        self.blocks = pygame.sprite.Group()
        self.board = dict() #stores everything on the game grid
        self.rows, self.cols = 10, 10
        self.cellSize = self.width / self.rows
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[(row, col)] = [False, False] # [hasBlock, hasAttack, hasItem]
        numBlocks = 25
        for i in range(numBlocks):
            randRow = random.randint(0, self.rows - 1)
            randCol = random.randint(0, self.cols - 1)
            self.board[(randRow, randCol)] = [True, False]
            Block.init()
            self.blocks.add(Block(randRow, randCol, self.cellSize))

    # checks if the user can make a desired move            
    def checkIfLegalMove(self, drow, dcol):
        newRow = self.player.row + drow
        newCol = self.player.col + dcol
        if newRow >= self.rows or newRow < 0 or newCol >= self.cols or newCol < 0:
            return False
        cellState = self.board[(newRow, newCol)]
        if cellState[0] == True or cellState[1] == True:
            return False
        self.player.move(newRow, newCol)

    # drop an attack
    def dropAttack(self, user):
        Attack.init()
        attack = Attack(user.row, user.col, self.cellSize, pygame.time.get_ticks()) #new sprite
        user.droppedAttacks.add(attack) #add sprite attack to sprite group
        self.board[(user.row, user.col)][1] = True

    # creates the "splashing" effect when an attack goes off
    def attackSplash(self, startRow, startCol):
        cs = self.cellSize
        i = 0
        isSplashLeft, isSplashUp, isSplashRight, isSplashDown = True, True, True, True
        while i < self.player.attackStrength:   
            i += 1
            AttackSplash.init()
            if isSplashLeft:
                splashLeft = AttackSplash(startRow, startCol - i, cs)
                self.attackSplashes.add(splashLeft)
            if isSplashUp: 
                splashUp = AttackSplash(startRow - i, startCol, cs)
                self.attackSplashes.add(splashUp)
            if isSplashRight:
                splashRight= AttackSplash(startRow, startCol + i, cs)
                self.attackSplashes.add(splashRight)
            if isSplashDown:
                splashDown = AttackSplash(startRow + i, startCol, cs)
                self.attackSplashes.add(splashDown) 
            collided = self.checkAttackBlockCollisions()
            if collided != None:
                for (row, col) in collided:
                    if col < startCol: 
                        isSplashLeft = False
                    elif col > startCol: 
                        isSplashRight = False
                    if row < startRow: 
                        isSplashUp = False
                    elif row > startRow: 
                        isSplashDown = False 

    # checks if an attack's splash paths collide with any surrounding blocks
    # if so, remove the block
    def checkAttackBlockCollisions(self):
        collided = set()
        attackBlockCollisions = pygame.sprite.groupcollide(self.blocks, self.attackSplashes, True, True)
        for collidedBlock in attackBlockCollisions:
            row, col = collidedBlock.row, collidedBlock.col
            collided.add((row, col))
            self.board[(row, col)][0] = False
        if len(collided) > 0: return collided
        else: return None

    # performs responses based on keypresses
    def keyPresses(self):
        if self.isKeyPressed(pygame.K_LEFT):
            self.checkIfLegalMove(0, -1)
        if self.isKeyPressed(pygame.K_RIGHT):
            self.checkIfLegalMove(0, +1)
        if self.isKeyPressed(pygame.K_UP):
            self.checkIfLegalMove(-1, 0)
        if self.isKeyPressed(pygame.K_DOWN):
            self.checkIfLegalMove(+1, 0)
        if self.isKeyPressed(pygame.K_SPACE): #create a bubble object at the player's position and should be in their own sprite group
            self.dropAttack(self.player)
        self.player.updateRect()

    # running the "game loop"
    def timerFired(self, dt):
        self.keyPresses()
        self.droppedAttacksCopy = self.player.droppedAttacks.copy()
        self.playerGroup.update(self.isKeyPressed, self.width, self.height)
        for attack in self.player.droppedAttacks:
            print(len(self.player.droppedAttacks))
            if pygame.time.get_ticks() - attack.timeMade > 3000:
                print(f'{attack.called}')
                if not attack.called:
                    attack.called = True
                    self.attackSplash(attack.row, attack.col)
                    self.droppedAttacksCopy.remove(attack)
                    self.board[(attack.row, attack.col)][1] = False
        self.player.droppedAttacks = self.droppedAttacksCopy

    # draws the game grid on the screen
    def drawGameGrid(self, screen):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = pygame.Rect(col * self.cellSize, row * self.cellSize, self.cellSize, self.cellSize) 
                fill = pygame.Color(100, 100, 100)
                pygame.draw.rect(screen, fill, cell)

    # updating the game screen  
    def redrawAll(self, screen):
        self.drawGameGrid(screen)
        self.blocks.draw(screen)
        self.playerGroup.draw(screen) # screen (from pygamegame) is our game Surface
        self.player.droppedAttacks.draw(screen)
        self.attackSplashes.draw(screen)
        self.attackSplashes.empty()

HomeScreenMode().run() # play game

