import pygame
import random
from dataclasses import dataclass
import math
import os

# Set working dir to path of currently running file
os.chdir(os.path.dirname(__file__))

pygame.init()

# Set up screen and game constants
screen = pygame.display.set_mode((1280, 720))
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
dt = 0
frameCounter = 0
iFrameCounter = 0
cooldownCounter = 0
score = 0

# Import font file
font = pygame.freetype.Font("Xolonium-Regular.ttf", 40)

# Define classes
@dataclass
class Player():
    pos: pygame.Vector2
    radius: int
    lives: int
    colour: str
    hitbox: pygame.Rect

@dataclass
class Spike:
    pos: pygame.Vector2
    radius: int
    hitbox: pygame.Rect

@dataclass
class Bullet:
    pos: pygame.Vector2
    hitbox: pygame.Rect

# Initialise game entities
player = Player(pos = pygame.Vector2(width/ 2, height/ 2), radius = 40, lives = 3, colour = "blue", hitbox = None)
spikes = []
bullets = []


def playerController(player, dt, width, height):
    keys = pygame.key.get_pressed()
    speed = 300 * dt

    if keys[pygame.K_w]:
        player.pos.y -= speed
    if keys[pygame.K_s]:
        player.pos.y += speed
    if keys[pygame.K_a]:
        player.pos.x -= speed
    if keys[pygame.K_d]:
        player.pos.x += speed

    player.pos.x = max(player.radius, min(width - player.radius, player.pos.x))
    player.pos.y = max(player.radius, min(height - player.radius, player.pos.y))

    player.hitbox = pygame.Rect(player.pos.x - 28, player.pos.y - 28, 56, 56)
    pygame.draw.circle(screen, player.colour, player.pos, 40)
    return player


def SpikeController(spikes, Spike, dt, height, width, score):
    if random.randint(1,8) == 1:
        spikes.append(Spike(pygame.Vector2(random.randint(0, width), 0), random.randint(20,80), None))

    spikes_to_remove = []

    for spike in spikes:
        spike.pos.y += 200 * dt

        size = spike.radius*(math.sqrt(2))
        spike.hitbox = pygame.Rect(spike.pos.x - size/2, spike.pos.y - size/2, size, size)

        pygame.draw.circle(screen, "red", spike.pos, spike.radius)

        if spike.pos.y > height or spike.radius < 20:
            spikes_to_remove.append(spike)
            score += 10 if spike.radius < 20 else 0

    spikes = [spike for spike in spikes if spike not in spikes_to_remove]

    return spikes, score


def hitDetection(player, spikes, iFrameCounter):
    iFrameCounter += 1
    #pygame.draw.rect(screen, "yellow", player.hitbox)
    for Spike in spikes:
        #pygame.draw.rect(screen, "yellow", Spike.hitbox)
        if iFrameCounter >= 180:
            player.colour = "blue"
            if pygame.Rect.colliderect(player.hitbox, Spike.hitbox):
                screen.fill("pink")
                player.colour = "pink"
                player.lives -= 1
                iFrameCounter = 0
    return player, iFrameCounter


def BulletController(bullets, Bullet, dt, cooldownCounter, player, spikes):
    cooldownCounter += 1
    keys = pygame.key.get_pressed()

    if pygame.event.peek(pygame.KEYDOWN) and pygame.KEYDOWN.key == pygame.K_SPACE and cooldownCounter > 15:
        bullets.append(Bullet(pygame.Vector2(player.pos.x - 10, player.pos.y - player.radius), 0))
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


    spikes, score = SpikeController(spikes, Spike, dt, height, width, score)

    player = playerController(player, dt, width, height)
    player, iFrameCounter = hitDetection(player, spikes, iFrameCounter)

    bullets, cooldownCounter, spikes = BulletController(bullets, Bullet, dt, cooldownCounter, player, spikes)

    
    font.render_to(screen, (20, height - 50), str(f"Lives: {player.lives}"))
    font. render_to(screen, (20, 20), str(f"Score: {score}"))


    pygame.display.flip()


pygame.quit()