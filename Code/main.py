import pygame
import random
from dataclasses import dataclass
import math

pygame.init()


screen = pygame.display.set_mode((1280, 720))
width = screen.get_width()
height = screen.get_height()

clock = pygame.time.Clock()
running = True
dt = 0


player_pos = pygame.Vector2(width/ 2, height/ 2)


@dataclass
class spike:
    pos: int
    radius: int
    

spikes = []


def movementController(player_pos, dt, width, height):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    while player_pos.x - 40 < 0:
        player_pos.x += 1
    while player_pos.x + 40 > width:
        player_pos.x -= 1
    while player_pos.y - 40 < 0:
        player_pos.y += 1
    while player_pos.y + 40 > height:
        player_pos.y -= 1

    return player_pos


def playerController(player_pos, dt, width, height):
    player_pos = movementController(player_pos, dt, width, height)
    pygame.draw.circle(screen, "blue", player_pos, 40)
    return player_pos


def spikeController(spikes, dt, height):
    for spike in spikes:
        spike.pos.y += 200 * dt
        pygame.draw.circle(screen, "red", spike.pos, spike.radius)
        if spike.pos.y > height:
            spikes.remove(spike)
    return spikes


def hitDetection(player_pos, spikes):
    player_hitbox = pygame.Rect(player_pos.x - 28, player_pos.y - 28, 56, 56)
    #pygame.draw.rect(screen, "yellow", player_hitbox)
    for spike in spikes:
        size = spike.radius*(math.sqrt(2))
        spike_hitbox = pygame.Rect(spike.pos.x - size/2, spike.pos.y - size/2, size, size)
        #pygame.draw.rect(screen, "yellow", spike_hitbox)
        if pygame.Rect.colliderect(player_hitbox, spike_hitbox):
            screen.fill("pink")


while running:


    dt = clock.tick(60) / 1000
    screen.fill("purple")


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    if random.randint(1,8) == 1:
        spikes.append(spike(pygame.Vector2(random.randint(0, width), 0), random.randint(20,80)))


    player_pos = playerController(player_pos, dt, width, height)
    spikes = spikeController(spikes, dt, height)


    hitDetection(player_pos, spikes)


    pygame.display.flip()

pygame.quit()