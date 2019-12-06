import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import pygame
import random
from Dino import *
from Cactus import *
from Ptera import *
from Ground import *
from Cloud import *
from Scoreboard import *
from sound import *
from pygame import *
from load import *

font = pygame.font.Font(None, 32)
pygame.init()

scr_size = (width, height) = (600, 350)
FPS = 60
gravity = 0.6

black = (0, 0, 0)
white = (255, 255, 255)
background_col = (235, 235, 235)

high_score = 0
jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')


screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Run ")


def disp_gameOver_msg(retbutton_image, gameover_image):
    retbutton_rect = retbutton_image.get_rect()
    retbutton_rect.centerx = width / 2
    retbutton_rect.top = height * 0.52

    gameover_rect = gameover_image.get_rect()
    gameover_rect.centerx = width / 2
    gameover_rect.centery = height * 0.35

    screen.blit(retbutton_image, retbutton_rect)
    screen.blit(gameover_image, gameover_rect)


def introscreen():
    temp_dino = Dino(44, 47)
    temp_dino.isBlinking = True
    gameStart = False

    temp_ground, temp_ground_rect = load_sprite_sheet('ground.png', 15, 1, -1, -1, -1)
    temp_ground_rect.left = width / 20
    temp_ground_rect.bottom = height

    logo, logo_rect = load_image('logo.png', 300, 140, -1)
    logo_rect.centerx = width * 0.6
    logo_rect.centery = height * 0.6
    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        temp_dino.isJumping = True
                        temp_dino.isBlinking = False
                        temp_dino.movement[1] = -1 * temp_dino.jumpSpeed

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)
            screen.blit(temp_ground[0], temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo, logo_rect)
            temp_dino.draw()

            pygame.display.update()

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True


def gameplay():
    global high_score
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    playerDino = Dino(44, 47, width/5, height,'dino.png','dino_ducking1.png', 'thang')
    playerDino1 = Dino(44, 47, width/20, height,'dino1.png','dino_ducking.png', 'eric')

    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    retbutton_image, retbutton_rect = load_image('replay_button.png', 35, 31, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 190, 11, -1)

    temp_images, temp_rect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
    HI_image = pygame.Surface((22, int(11 * 6 / 5)))
    HI_rect = HI_image.get_rect()
    HI_image.fill(background_col)
    HI_image.blit(temp_images[10], temp_rect)
    temp_rect.left += temp_rect.width
    HI_image.blit(temp_images[11], temp_rect)
    HI_rect.top = height * 0.1
    HI_rect.left = width * 0.73

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True
                    # player 1
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if playerDino.rect.bottom == int(0.98 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                    #player 2
                    # if event.type == pygame.KEYDOWN:
                    #     if event.key == pygame.K_w:
                    #         if playerDino1.rect.bottom == int(0.98 * height):
                    #             playerDino1.isJumping = True
                    #             if pygame.mixer.get_init() != None:
                    #                 jump_sound.play()
                    #             playerDino1.movement[1] = -1 * playerDino1.jumpSpeed
                    #
                    #     if event.key == pygame.K_s:
                    #         if not (playerDino1.isJumping and playerDino1.isDead):
                    #             playerDino1.isDucking = True
                    #
                    # if event.type == pygame.KEYUP:
                    #     if event.key == 115:
                    #         playerDino1.isDucking = False


            for c in cacti:
                c.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(playerDino, c):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()
                # if pygame.sprite.collide_mask(playerDino1, c):
                #     playerDino1.isDead = True
                #     if pygame.mixer.get_init() != None:
                #         die_sound.play()

            for p in pteras:
                p.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(playerDino, p):
                    playerDino.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()
                # if pygame.sprite.collide_mask(playerDino1, p):
                #     playerDino1.isDead = True
                #     if pygame.mixer.get_init() != None:
                #         die_sound.play()
            if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed, 40, 40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

            if len(pteras) == 0 and random.randrange(0, 200) == 10 and counter > 500:
                for l in last_obstacle:
                    if l.rect.right < width * 0.8:
                        last_obstacle.empty()
                        last_obstacle.add(Ptera(gamespeed, 46, 40))

            if len(clouds) < 5 and random.randrange(0, 300) == 10:
                Cloud(width, random.randrange(height / 5, height / 2))

            playerDino.update()
            # playerDino1.update()
            cacti.update()
            pteras.update()
            clouds.update()
            new_ground.update()
            scb.update(playerDino.score)
            highsc.update(high_score)

            if pygame.display.get_surface() != None:
                screen.fill(background_col)
                new_ground.draw()
                clouds.draw(screen)
                scb.draw()
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                cacti.draw(screen)
                pteras.draw(screen)
                playerDino.draw()
                # playerDino1.draw()

                pygame.display.update()
            clock.tick(FPS)

            if playerDino.isDead:
                gameOver = True
                text = font.render(playerDino1.getName() + " Win!", True, black, background_col)
                textRect = text.get_rect()
                # set the center of the rectangular object.
                textRect.center = (width // 2, height // 2 - 100)
                screen.blit(text, textRect)
                if playerDino.score > high_score:
                    high_score = playerDino.score
            # if playerDino1.isDead:
            #     gameOver = True
            #     text = font.render(playerDino.getName() + " Win!", True, black, background_col)
            #     textRect = text.get_rect()
            #     textRect.center = (width // 2, height // 2 - 100)
            #     screen.blit(text, textRect)
            #     if playerDino1.score > high_score:
            #         high_score = playerDino.score

            if counter % 700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameplay()
            highsc.update(high_score)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(retbutton_image, gameover_image)
                if high_score != 0:
                    highsc.draw()
                    screen.blit(HI_image, HI_rect)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


def main():
    isGameQuit = introscreen()
    if not isGameQuit:
        gameplay()


if __name__ == "__main__":
    main()
