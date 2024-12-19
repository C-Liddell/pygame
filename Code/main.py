import pygame
import random
from dataclasses import dataclass
import math
import os

# To prevent error when running build
from pygame import freetype

# Set working dir to path of currently running file
os.chdir(os.path.dirname(__file__))

pygame.init()

# Set up screen and game constants
screen = pygame.display.set_mode((1280, 720))
width = screen.get_width()
height = screen.get_height()
clock = pygame.time.Clock()
dt = 0
score = 0
difficulty = 0

timers = {
    "score": 0,
    "hit": 0,
    "shot": 0
}

# Import font file
font = pygame.freetype.Font("files/Xolonium-Regular.ttf", 40)

# Define classes
@dataclass
class Player():
    pos: pygame.Vector2
    radius: int
    lives: int
    colour: str
    hitbox: pygame.Rect

    def getHitbox(self):
        size = self.radius*(math.sqrt(2))
        self.hitbox = pygame.Rect(self.pos.x - size/2, self.pos.y - size/2, size, size)
        return self.hitbox

@dataclass
class Spike:
    pos: pygame.Vector2
    radius: int
    hitbox: pygame.Rect
    
    def getHitbox(self):
        size = self.radius*(math.sqrt(2))
        self.hitbox = pygame.Rect(self.pos.x - size/2, self.pos.y - size/2, size, size)
        return self.hitbox

@dataclass
class Bullet:
    pos: pygame.Vector2
    hitbox: pygame.Rect

# Initialise game entities
player = Player(pos = pygame.Vector2(width/ 2, height/ 2), radius = 40, lives = 3, colour = "blue", hitbox = None)
spikes = []
bullets = []


def playerController(player, dt):
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

    player.getHitbox()
    pygame.draw.circle(screen, player.colour, player.pos, 40)
    return player


def SpikeController(spikes, score, dt):
    spikes_to_remove = []

    for spike in spikes:
        spike.pos.y += 200 * dt

        spike.getHitbox()

        pygame.draw.circle(screen, "red", spike.pos, spike.radius)

        if spike.pos.y > height or spike.radius < 20:
            spikes_to_remove.append(spike)
            score += 10 if spike.radius < 20 else 0

    spikes = [spike for spike in spikes if spike not in spikes_to_remove]
    return spikes, score


def spikeSpawner(spikes, difficulty):
    if random.randint(1,8) == 1:
        spikes.append(Spike(pygame.Vector2(random.randint(0, width), 0), random.randint(20,50), None))
    elif random.randint(1, 20) == 1:
        spikes.append(Spike(pygame.Vector2(random.randint(0, width), 0), random.randint(50,80), None))
    return spikes


def BulletController(bullets, spikes, dt, timers):
    timers["shot"] += 1
    bullets_to_remove = []

    for bullet in bullets:
        bullet.pos.y -= 200 * dt
        bullet.hitbox = pygame.Rect(bullet.pos.x, bullet.pos.y, 20, 30)
        pygame.draw.rect(screen, "yellow", bullet.hitbox)

        for spike in spikes:
            if pygame.Rect.colliderect(bullet.hitbox, spike.hitbox) or bullet.pos.y < 0:
                bullets_to_remove.append(bullet)
                spike.radius -= 10 if pygame.Rect.colliderect(bullet.hitbox, spike.hitbox) else 0
            
    bullets = [bullet for bullet in bullets if bullet not in bullets_to_remove]
    return bullets, spikes, timers


def hitDetection(player, spikes, timers):
    timers["hit"] += 1
    for spike in spikes:
        if timers["hit"] >= 180:
            player.colour = "blue"
            if pygame.Rect.colliderect(player.hitbox, spike.hitbox):
                screen.fill("pink")
                player.colour = "pink"
                player.lives -= 1
                resetTimer(timers, "hit")
    return player, timers


def resetTimer(timers, timer):
    timers[timer] = 0
    return timers

def debug(player, spikes, difficulty):
    pygame.draw.rect(screen, "yellow", player.hitbox)
    for spike in spikes:
        pygame.draw.rect(screen, "yellow", spike.hitbox)
    font.render_to(screen, (20, 75), str(f"Difficulty: {difficulty}"))

while player.lives > 0:

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and timers["shot"] > 15:    
            bullets.append(Bullet(pygame.Vector2(player.pos.x - 10, player.pos.y - player.radius), 0))
            resetTimer(timers, "shot")

    dt = clock.tick(60) / 1000
    screen.fill("purple")

    # Increses score
    timers["score"] += 1
    if timers["score"] >= 60:
        score += 1
        difficulty += 1
        resetTimer(timers, "score")


    player = playerController(player, dt)

    spikes = spikeSpawner(spikes, difficulty)
    spikes, score = SpikeController(spikes, score, dt)
    
    bullets, spikes, timers = BulletController(bullets, spikes, dt, timers)
    player, timers = hitDetection(player, spikes, timers)


    #debug(player, spikes, difficulty)


    font.render_to(screen, (20, height - 50), str(f"Lives: {player.lives}"))
    font.render_to(screen, (20, 20), str(f"Score: {score}"))


    pygame.display.flip()

print(f"Game Over! You scored {score} points.")
pygame.quit()