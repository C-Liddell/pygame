import pygame
import random
from dataclasses import dataclass
import math


pygame.init()


screen = pygame.display.set_mode((1280, 720))
width = screen.get_width()
height = screen.get_height()

clock = pygame.time.Clock()
dt = 0

font = pygame.freetype.Font("Xolonium-Regular.ttf", 40)


@dataclass
class player():
    pos = pygame.Vector2(width/ 2, height/ 2)
    radius = 40
    next_hit_time = 0
    lives = 3

@dataclass
class spike:
    pos: int
    radius: int
spikes = []


def playerController(player, dt, width, height):
    player = movementController(player, dt, width, height)
    pygame.draw.circle(screen, "blue", player.pos, 40)
    return player

def movementController(player, dt, width, height):
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

    return player


def spikeSpawner(spikes, width):
    if random.randint(1,8) == 1:
        spikes.append(spike(pygame.Vector2(random.randint(0, width), 0), random.randint(20,80)))
    return spikes

def spikeController(spikes, dt, height):
    for spike in spikes:
        spike.pos.y += 200 * dt
        pygame.draw.circle(screen, "red", spike.pos, spike.radius)
        if spike.pos.y > height:
            spikes.remove(spike)
    return spikes


def hitDetection(player, spikes):
    player_hitbox = pygame.Rect(player.pos.x - 28, player.pos.y - 28, 56, 56)
    #pygame.draw.rect(screen, "yellow", player_hitbox)
    for spike in spikes:
        size = spike.radius*(math.sqrt(2))
        spike_hitbox = pygame.Rect(spike.pos.x - size/2, spike.pos.y - size/2, size, size)
        #pygame.draw.rect(screen, "yellow", spike_hitbox)
        if pygame.Rect.colliderect(player_hitbox, spike_hitbox):
            if pygame.time.get_ticks() > player.next_hit_time:
                screen.fill("pink")
                player.lives -= 1
                player.next_hit_time = pygame.time.get_ticks() + 1000
    return player




while player.lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()


    dt = clock.tick(60) / 1000
    screen.fill("purple")


    spikes = spikeSpawner(spikes, width)
    spikes = spikeController(spikes, dt, height)

    player = playerController(player, dt, width, height)
    player = hitDetection(player, spikes)

    
    font.render_to(screen, (20, height - 50), str(f"Lives: {player.lives}"))


    pygame.display.flip()


pygame.quit()