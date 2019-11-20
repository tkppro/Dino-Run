import pygame
from pygame import *
from load import load_sprite_sheet
pygame.init()

scr_size = (width, height) = (600, 350)
gravity = 0.6
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')
screen = pygame.display.set_mode(scr_size)

class Dino():
    def __init__(self,sizex=-1,sizey=-1, widthD=0, heightD=0,dino='dino.png',dino_ducking='dino_ducking1.png', name='default'):
        self.images,self.rect = load_sprite_sheet(dino,5,1,sizex,sizey,-1)
        self.images1,self.rect1 = load_sprite_sheet(dino_ducking,2,1,59,sizey,-1)
        self.rect.bottom = int(0.98*heightD)
        self.rect.left = widthD
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0,0]
        self.jumpSpeed = 15.5
        self.name = name
        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image,self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98*height):
            self.rect.bottom = int(0.98*height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1)%2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1)%2

        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1)%2 + 2

        if self.isDead:
           self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index)%2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)

    def getName(self):
        return self.name
