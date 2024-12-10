import pygame
import random
from dataclasses import dataclass
import math
from pygame import freetype


pygame.init()


screen = pygame.display.set_mode((1280, 720))
width = screen.get_width()
height = screen.get_height()

clock = pygame.time.Clock()
dt = 0
frameCounter = 0
iFrameCounter = 0
cooldownCounter = 0

score = 0

font = pygame.freetype.Font("Xolonium-Regular.ttf", 40)


@dataclass
class player():
    pos = pygame.Vector2(width/ 2, height/ 2)
    radius = 40
    lives = 3
    colour = "blue"
    hitbox = 0

@dataclass
class spike:
    pos: int
    radius: int
    hitbox: int
spikes = []

@dataclass
class bullet:
    pos: int
    hitbox: int
bullets = []


def playerController(player, dt, width, height):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player.pos.y += 300 * dt
    if keys[pygame.K_a]:
        player.pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player.pos.x += 300 * dt

    while player.pos.x - player.radius < 0:
        player.pos.x += 1
    while player.pos.x + player.radius > width:
        player.pos.x -= 1
    while player.pos.y - player.radius < 0:
        player.pos.y += 1
    while player.pos.y + player.radius > height:
        player.pos.y -= 1

    player.hitbox = pygame.Rect(player.pos.x - 28, player.pos.y - 28, 56, 56)
    pygame.draw.circle(screen, player.colour, player.pos, 40)
    return player


def spikeController(spikes, spike, dt, height, width, score):
    if random.randint(1,8) == 1:
        spikes.append(spike(pygame.Vector2(random.randint(0, width), 0), random.randint(20,80), 0))

    for spike in spikes:
        size = spike.radius*(math.sqrt(2))
        spike.pos.y += 200 * dt
        spike.hitbox = pygame.Rect(spike.pos.x - size/2, spike.pos.y - size/2, size, size)
        pygame.draw.circle(screen, "red", spike.pos, spike.radius)
        if spike.pos.y > height:
            spikes.remove(spike)
        if spike.radius < 20:
            spikes.remove(spike)
            score += 10
    return spikes, score


def hitDetection(player, spikes, iFrameCounter):
    iFrameCounter += 1
    #pygame.draw.rect(screen, "yellow", player.hitbox)
    for spike in spikes:
        #pygame.draw.rect(screen, "yellow", spike.hitbox)
        if iFrameCounter >= 180:
            player.colour = "blue"
            if pygame.Rect.colliderect(player.hitbox, spike.hitbox):
                screen.fill("pink")
                player.colour = "pink"
                player.lives -= 1
                iFrameCounter = 0
    return player, iFrameCounter


def bulletController(bullets, bullet, dt, cooldownCounter, player, spikes):
    cooldownCounter += 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and cooldownCounter >= 15:
        bullets.append(bullet(pygame.Vector2(player.pos.x - 10, player.pos.y - player.radius), 0))
        cooldownCounter = 0
    for bullet in bullets:
        bullet.pos.y -= 200 * dt
        bullet.hitbox = pygame.Rect(bullet.pos.x, bullet.pos.y, 20, 30)
        pygame.draw.rect(screen, "yellow", bullet.hitbox)
        for spike in spikes:
            if pygame.Rect.colliderect(bullet.hitbox, spike.hitbox):
                spike.radius -= 10
            if pygame.Rect.colliderect(bullet.hitbox, spike.hitbox) or bullet.pos.y < 0:
                try:
                    bullets.remove(bullet)
                except:
                    pass
    return bullets, cooldownCounter, spikes


while player.lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    dt = clock.tick(60) / 1000
    screen.fill("purple")

    frameCounter += 1
    if frameCounter == 60:
        score += 1
        frameCounter = 0


    spikes, score = spikeController(spikes, spike, dt, height, width, score)

    player = playerController(player, dt, width, height)
    player, iFrameCounter = hitDetection(player, spikes, iFrameCounter)

    bullets, cooldownCounter, spikes = bulletController(bullets, bullet, dt, cooldownCounter, player, spikes)

    
    font.render_to(screen, (20, height - 50), str(f"Lives: {player.lives}"))
    font. render_to(screen, (20, 20), str(f"Score: {score}"))


    pygame.display.flip()


pygame.quit()